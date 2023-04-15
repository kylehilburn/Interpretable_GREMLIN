program main

implicit none

character(80), parameter :: datafile = 'gremlin_conus2_inputs_2d.bin'
character(80), parameter :: infile1 = 'coefs.bin'
character(80), parameter :: infile2 = 'intercept.bin'
character(80), parameter :: outfrmt = "('predictions_linear_',a,'_2d.bin')"
character(80) :: outfile

integer(4), parameter :: nparm = 2144
real(8) :: coefs(nparm)
real(8) :: intercept
integer(4) :: mparm

real(4), parameter :: fill_value = -1.E30

integer(8) :: nsamp_train
integer(8) :: nsamp_test
integer(8) :: ninputs
integer(8) :: ny, nx
real(4), allocatable :: Xdata_train(:,:,:,:)
real(4), allocatable :: Xdata_test(:,:,:,:)
real(4), allocatable :: Xdata(:,:,:,:)
integer(4) :: nsamp, nnx, nny

real(4), allocatable :: preds(:,:,:)

real(8) :: x(nparm)
integer(4) :: isamp, iparm, jparm
integer(4) :: i, j, k
real(8) :: psum
real(8) :: stime, etime
integer(4) :: ix, iy
logical(4) :: isbad

character(5) :: ads
integer(4) :: arglen

!-----

call get_command_argument(1,ads,arglen)
if (arglen.le.0) stop 'error reading command argument'
print*,'ads=',ads

!-----

open(unit=3,file=datafile,status='old',form='unformatted',access='stream')
read(3) nsamp_train
read(3) nsamp_test
read(3) ny
read(3) nx
read(3) ninputs
print*,'nsamp_train,nsamp_test,ninputs=',nsamp_train,nsamp_test,ninputs
print*,'ny,nx=',ny,nx
allocate(Xdata_train(ninputs,nx,ny,nsamp_train)) !note fortran index ordering!
allocate(Xdata_test(ninputs,nx,ny,nsamp_test)) !note fortran index ordering!
read(3) Xdata_train
read(3) Xdata_test
close(3)

if (ads.eq.'train') then 
    deallocate(Xdata_test) !don't need this anymore
    nsamp = nsamp_train
    allocate(Xdata(ninputs,nx,ny,nsamp))
    Xdata = Xdata_train
else
    deallocate(Xdata_train) !don't need this anymore
    nsamp = nsamp_test
    allocate(Xdata(ninputs,nx,ny,nsamp))
    Xdata = Xdata_test
endif
nnx = nx
nny = nx

call flush()

!-----

open(unit=3,file=infile1,status='old',form='unformatted',access='stream')
read(3) mparm
if (mparm.ne.nparm) stop 'nparm error'
read(3) coefs
close(3)

open(unit=3,file=infile2,status='old',form='unformatted',access='stream')
read(3) intercept
close(3)

!-----

allocate(preds(nx,ny,nsamp))

preds = fill_value

call cpu_time(stime)
do isamp = 1, nsamp

    call cpu_time(etime)
    print*,isamp,'seconds ellpased',(etime-stime)
    call flush()
    call cpu_time(stime)

    do iy = 1, ny
        do ix = 1, nx

            ! ----------------------------
            ! Linear model

            x = 0.0d0
            k = 1

            isbad = .false.
            do i = 1, ninputs
                if (Xdata(i,ix,iy,isamp).ne.Xdata(i,ix,iy,isamp)) then
                    isbad = .true.
                    exit
                endif
                x(k) = Xdata(i,ix,iy,isamp)
                k = k + 1
            enddo !i
            if (isbad) cycle

            do j = 1, ninputs
                do i = 1, j
                    x(k) = Xdata(i,ix,iy,isamp) * Xdata(j,ix,iy,isamp)
                    k = k + 1
                enddo !i
            enddo !j

            ! ----------------------------

            psum = 0.0d0
            do iparm = 1, nparm
                psum = psum + coefs(iparm) * x(iparm)
            enddo !iparm
            psum = 60.*( psum + intercept )
            if (psum.lt.0) psum = 0.

            preds(ix,iy,isamp) = psum

        enddo !ix
    enddo !iy

enddo !isamp

!-----

write(outfile,outfrmt) trim(ads)
print*,'outfile=',trim(outfile)

open(unit=3,file=outfile,status='replace',form='unformatted',access='stream')
write(3) nsamp
write(3) nny
write(3) nnx
write(3) preds
close(3)

end program main
