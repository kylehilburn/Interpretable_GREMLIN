program main

implicit none

character(80), parameter :: inputs_file = 'gremlin_conus2_inputs_2d_nogamma.bin'
character(80), parameter :: predfrmt = "('predictions_',a,'_train_2d.bin')"
character(80), parameter :: outfrmt = "('bin_avgs_',a,'.bin')"

character(80) :: pred_file
character(80) :: outfile 

integer(4), parameter :: ninputs = 64

integer(4), parameter :: nbinsx = 101
real(4), parameter :: dbinsx = 0.02
real(4), parameter :: minx = -1.

integer(4) :: i
real(4), parameter :: xbins(nbinsx) = (/ (minx + i*dbinsx, i=1,nbinsx) /)

real(8) :: cnt1(ninputs,nbinsx) !note fortran index ordering!
real(8) :: tot1(ninputs,nbinsx) !note fortran index ordering!

real(8) :: cnt2(ninputs,ninputs,nbinsx,nbinsx) !note fortran index ordering!
real(8) :: tot2(ninputs,ninputs,nbinsx,nbinsx) !note fortran index ordering!

integer(8) :: nsamp_train
integer(8) :: nsamp_test
integer(8) :: ni
integer(8) :: nx, ny
integer(4) :: nsamp, nnx, nny

real(4), allocatable :: Xdata_train(:,:,:,:)
real(4), allocatable :: Xdata_test(:,:,:,:)
real(4), allocatable :: Ydata_train(:,:,:)
real(4), allocatable :: Ydata_test(:,:,:)

real(4), allocatable :: preds(:,:,:)

integer(4), parameter :: inunit = 8
integer(4), parameter :: outunit = 9

real(8) :: stime, etime

integer(4) :: isamp, ii, jj
integer(4) :: ilat, ilon

real(4) :: xval, yval
integer(4) :: ix, iy

character(7) :: ytype
integer(4) :: arglen

logical(4) :: isbad

!-----

call get_command_argument(1,ytype,arglen)
if (arglen.le.0) stop 'error reading command argument'
print*,'running bin avgs for',trim(ytype)

open(unit=inunit,file=inputs_file,status='old',form='unformatted',access='stream')
read(inunit) nsamp_train
read(inunit) nsamp_test
read(inunit) ny
read(inunit) nx
read(inunit) ni
if (ni .ne. ninputs) stop 'ni .ne. ninputs'
print*,'nsamp_train,nsamp_test=',nsamp_train,nsamp_test
allocate(Xdata_train(ninputs,nx,ny,nsamp_train)) !note fortran index ordering!
allocate(Xdata_test(ninputs,nx,ny,nsamp_test)) !note fortran index ordering!
allocate(Ydata_train(nx,ny,nsamp_train))
allocate(Ydata_test(nx,ny,nsamp_test))
read(inunit) Xdata_train
read(inunit) Xdata_test
read(inunit) Ydata_train
read(inunit) Ydata_test
close(inunit)

deallocate(Xdata_test)
deallocate(Ydata_test)

allocate(preds(nx,ny,nsamp_train))

if (trim(ytype).eq.'data') then
    preds = Ydata_train
else
    deallocate(Ydata_train)
    write(pred_file,predfrmt) trim(ytype)
    print*,'pred_file=',trim(pred_file)
    open(unit=inunit,file=pred_file,status='old',form='unformatted',access='stream')
    read(inunit) nsamp
    read(inunit) nny
    read(inunit) nnx
    read(inunit) preds
    close(inunit)
    where(preds.gt.-1.E30)
        preds = preds / 60.
    endwhere
endif

!-----

cnt1 = 0.0d0
tot1 = 0.0d0

cnt2 = 0.0d0
tot2 = 0.0d0

call cpu_time(stime)

do isamp = 1, nsamp_train

    call cpu_time(etime)
    print*,isamp,(etime-stime)
    call flush()
    call cpu_time(stime)

    do ilat = 1, ny
        do ilon = 1, nx

            yval = preds(ilon,ilat,isamp)
            if (yval.ne.yval) cycle  !NaN
            if (yval.lt.0) cycle

            isbad = .false.
            do ii = 1, ninputs
                xval = Xdata_train(ii,ilon,ilat,isamp)
                if (xval.ne.xval) then  !NaN
                    isbad = .true.
                    exit
                endif
            enddo !ii
            if (isbad) cycle

            do ii = 1, ninputs

                xval = Xdata_train(ii,ilon,ilat,isamp)
                !if (xval.ne.xval) cycle  !NaN
                ix = 1+int( (xval-minx)/dbinsx )
                if (ix.lt.1) ix=1
                if (ix.gt.nbinsx) ix=nbinsx

                cnt1(ii,ix) = cnt1(ii,ix) + 1
                tot1(ii,ix) = tot1(ii,ix) + yval

                do jj = 1, ii-1

                    xval = Xdata_train(jj,ilon,ilat,isamp)
                    !if (xval.ne.xval) cycle  !NaN
                    iy = 1+int( (xval-minx)/dbinsx )
                    if (iy.lt.1) iy=1
                    if (iy.gt.nbinsx) iy=nbinsx

                    cnt2(ii,jj,ix,iy) = cnt2(ii,jj,ix,iy) + 1
                    tot2(ii,jj,ix,iy) = tot2(ii,jj,ix,iy) + yval

                enddo !jj

            enddo !ii

        enddo !ix
    enddo !iy

enddo !isamp

!-----

write(outfile,outfrmt) trim(ytype)
print*,'outfile=',trim(outfile)

open(unit=outunit,file=outfile,status='replace',form='unformatted',access='stream')
write(outunit) ninputs
write(outunit) nbinsx
write(outunit) xbins
write(outunit) cnt1
write(outunit) tot1
write(outunit) cnt2
write(outunit) tot2
close(outunit)

end program main
