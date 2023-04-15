program main

implicit none

character(80) :: datafile
character(80), parameter :: outfile = 'covar.bin'
character(80), parameter :: datafrmt = "('covar_batch',i2.2,'.bin')"

integer(4), parameter :: nparm = 2144
integer(4), parameter :: nfiles = 10
integer(4) :: mparm

real(8) :: cntx
real(8) :: ex(nparm)
real(8) :: ey
real(8) :: exx(nparm,nparm)
real(8) :: eyx(nparm)

real(8) :: scntx
real(8) :: sex(nparm)
real(8) :: sey
real(8) :: sexx(nparm,nparm)
real(8) :: seyx(nparm)

real(8) :: covar(nparm,nparm)
real(8) :: cross(nparm)

integer(4) :: iparm, jparm
integer(4) :: ifile

scntx = 0.0d0
sex = 0.0d0
sey = 0.0d0
sexx = 0.0d0
seyx = 0.0d0

do ifile = 1, nfiles

    write(datafile,datafrmt) ifile
    print*,'datafile=',trim(datafile)

    open(unit=3,file=datafile,status='old',form='unformatted',access='stream')
    read(3) mparm
    if (mparm.ne.nparm) stop 'nparm error'
    read(3) cntx,ex,ey,exx,eyx
    close(3)

    scntx = scntx + cntx
    sex = sex + ex
    sey = sey + ey
    sexx = sexx + exx
    seyx = seyx + eyx

enddo !ifile

do iparm = 1, nparm
    do jparm = iparm+1, nparm
        if (sexx(jparm,iparm) .ne. 0) print*,'warning: nonzero value'
        if (sexx(iparm,jparm) .eq. 0) print*,'warning: zero value at iparm,jparm=',iparm,jparm
        sexx(jparm,iparm) = sexx(iparm,jparm)
    enddo !jparm

enddo !iparm

sey = sey / scntx
sex = sex / scntx
sexx = sexx / scntx
seyx = seyx / scntx

covar = 0.0d0
cross = 0.0d0
do jparm = 1, nparm
    cross(jparm) = seyx(jparm) - sey*sex(jparm)
    do iparm = 1, nparm
        covar(iparm,jparm) = sexx(iparm,jparm) - sex(iparm)*sex(jparm)
    enddo !iparm
enddo !jparm

open(unit=3,file=outfile,status='replace',form='unformatted',access='stream')
write(3) nparm
write(3) sey, cross, covar
close(3)

end program main
