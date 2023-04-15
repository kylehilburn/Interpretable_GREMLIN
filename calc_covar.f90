program main

implicit none

character(80), parameter :: datafrmt = "('gremlin_conus2_inputs_batch',i2.2,'.bin')"
character(80), parameter :: outfrmt = "('covar_batch',i2.2,'.bin')"

character(80) :: datafile
integer(4) :: nsamp_train
integer(8) :: ninputs
real(4), allocatable :: xtrain(:,:)
real(4), allocatable :: ytrain(:)

character(80) :: outfile
integer(4), parameter :: nparm = 2144

real(8) :: wt
real(8) :: cntx
real(8) :: ex(nparm)
real(8) :: ey
real(8) :: exx(nparm,nparm)
real(8) :: eyx(nparm)

real(8) :: x(nparm), y
integer(4) :: isamp, iparm, jparm
integer(4) :: i, j, k
real(8) :: stime, etime

integer(4) :: ibatch
character(2) :: sbatch
integer(4) :: arglen

call get_command_argument(1,sbatch,arglen)
if (arglen.le.0) stop 'error reading command argument'
read(sbatch,'(i2.2)') ibatch
print*,'ibatch=',ibatch

write(datafile,datafrmt) ibatch
print*,'datafile=',trim(datafile)

write(outfile,outfrmt) ibatch
print*,'outfile=',trim(outfile)

cntx = 0.0d0
ex = 0.0d0
ey = 0.0d0
exx = 0.0d0
eyx = 0.0

open(unit=3,file=datafile,status='old',form='unformatted',access='stream')
read(3) nsamp_train, ninputs
print*,'nsamp_train,ninputs=',nsamp_train,ninputs
allocate(xtrain(ninputs,nsamp_train))
allocate(ytrain(nsamp_train))
read(3) xtrain
read(3) ytrain
close(3)

call flush()

call cpu_time(stime)
do isamp = 1, nsamp_train

    if (modulo(isamp,100000) .eq. 0) then
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

    y = ytrain(isamp)
    wt = exp(5.0*(y**5))

    cntx = cntx + wt
    ey = ey + y*wt
    do iparm = 1, nparm
        ex(iparm) = ex(iparm) + x(iparm)*wt
        eyx(iparm) = eyx(iparm) + x(iparm)*y*wt
        do jparm = 1, iparm
            exx(jparm,iparm) = exx(jparm,iparm) + x(jparm)*x(iparm)*wt
        enddo !jparm
    enddo !iparm

enddo !isamp

open(unit=3,file=outfile,status='replace',form='unformatted',access='stream')
write(3) nparm
write(3) cntx,ex,ey,exx,eyx
close(3)

end program main
