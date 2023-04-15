program main

implicit none

character(80), parameter :: coefsfile = 'coefs.bin'
character(80), parameter :: outfile = 'intercept.bin'
character(80), parameter :: datafrmt = "('gremlin_conus2_inputs_batch',i2.2,'.bin')"

integer(4), parameter :: nfiles = 10

character(80) :: datafile

integer(4), parameter :: nparm = 2144
real(8) :: coefs(nparm)
integer(4) :: mparm

integer(4) :: nsamp_train
integer(8) :: ninputs
real(4), allocatable :: xtrain(:,:)
real(4), allocatable :: ytrain(:)

real(8) :: x(nparm)
real(8) :: y
integer(4) :: isamp, iparm, jparm
integer(4) :: i, j, k
real(8) :: stime, etime

real(8) :: cntx, sumx, sumy, psum
real(8) :: intercept

integer(4) :: ibatch
character(2) :: sbatch
integer(4) :: arglen

cntx = 0.0d0
sumx = 0.0d0
sumy = 0.0d0

open(unit=3,file=coefsfile,status='old',form='unformatted',access='stream')
read(3) mparm
if (mparm.ne.nparm) stop 'nparm error'
read(3) coefs
close(3)

do ibatch = 1, nfiles 

    write(datafile,datafrmt) ibatch
    print*,'datafile=',trim(datafile)

    open(unit=3,file=datafile,status='old',form='unformatted',access='stream')
    read(3) nsamp_train, ninputs
    print*,'nsamp_train,ninputs=',nsamp_train,ninputs
    if (allocated(xtrain)) then
        deallocate(xtrain)
        deallocate(ytrain)
    endif
    allocate(xtrain(ninputs,nsamp_train))
    allocate(ytrain(nsamp_train))
    read(3) xtrain
    read(3) ytrain
    close(3)

    call flush()

    call cpu_time(stime)
    do isamp = 1, nsamp_train

        if (modulo(isamp,1000000) .eq. 0) then
            call cpu_time(etime)
            print*,isamp,'seconds ellpased',(etime-stime)
            call flush()
            call cpu_time(stime)
        endif

        ! ----------------------------
        ! Linear model

        x = 0.0d0
        k = 1

        do i = 1, ninputs
            x(k) = xtrain(i,isamp)
            k = k + 1
        enddo !i

        do j = 1, ninputs
            do i = 1, j
                x(k) = xtrain(i,isamp) * xtrain(j,isamp)
                k = k + 1
            enddo !i
        enddo !j

        ! ----------------------------

        psum = 0.0d0
        do iparm = 1, nparm
            psum = psum + coefs(iparm) * x(iparm)
        enddo !iparm

        y = ytrain(isamp)

        cntx = cntx + 1
        sumy = sumy + y
        sumx = sumx + psum

    enddo !isamp

enddo !ibatch

print*,'cntx =',cntx

intercept = (sumy - sumx) / cntx
print*,'intercept=',intercept

open(unit=3,file=outfile,status='replace',form='unformatted',access='stream')
write(3) intercept
close(3)

end program main
