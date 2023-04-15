program main

implicit none

character(80), parameter :: datafile = 'gremlin_conus2_inputs_1d.bin'
character(80), parameter :: outfrmt = "('gremlin_conus2_inputs_batch',i2.2,'.bin')"
integer(4), parameter :: nfiles = 10

integer(8) :: nsamp_train, nsamp_test, ninputs
real(4), allocatable :: xtrain(:,:)
real(4), allocatable :: xtest(:,:)
real(4), allocatable :: ytrain(:)
real(4), allocatable :: ytest(:)

integer(4) :: dsamp, isamp1, isamp2, i
character(80) :: outfile

open(unit=3,file=datafile,status='old',form='unformatted',access='stream')
read(3) nsamp_train, nsamp_test, ninputs
print*,'nsamp_train,nsamp_test,ninputs=',nsamp_train,nsamp_test,ninputs
allocate(xtrain(ninputs,nsamp_train))
allocate(xtest(ninputs,nsamp_test))
allocate(ytrain(nsamp_train))
allocate(ytest(nsamp_test))
read(3) xtrain
read(3) xtest
deallocate(xtest)
read(3) ytrain
read(3) ytest
deallocate(ytest)
close(3)

dsamp = nsamp_train / nfiles 
print*,'dsamp=',dsamp

do i = 1, nfiles 

    isamp1 = 1 + dsamp*(i-1)
    isamp2 = dsamp*i
    print*,i,isamp1,isamp2

    write(outfile,outfrmt) i
    print*,'outfile=',trim(outfile)
    
    open(unit=3,file=outfile,status='replace',form='unformatted',access='stream')
    write(3) dsamp, ninputs
    write(3) xtrain(:,isamp1:isamp2)
    write(3) ytrain(isamp1:isamp2)
    close(3)

enddo !i

end program main
