PROGRAM hist

!calculates histogram from valmin to valmax using nbins bins
!output not normalised to probability of 1

implicit none

integer :: ndata,nbins,i,printzeros,iweightcolumn,idatacolumn,ncolumns,ic,nskip
real(kind=8) :: valmin,valmax
real(kind=8),dimension(:),allocatable :: datah,histogram,histcoord,weight,tempcol
character(len=100) :: datafile,outfile

read(*,*) ndata !no. of input datapoints
read(*,*) nbins
read(*,*) valmin
read(*,*) valmax
read(*,*) datafile !input file
read(*,*) outfile
read(*,*) nskip !lines to skip at start of datafile
read(*,*) ncolumns ! in datafile
read(*,*) idatacolumn ! which column contains data to be histogrammed, numbered from 1
read(*,*) iweightcolumn ! which column contains weights, numbered from 1, if = 0 then all weight are = 1.0
read(*,*) printzeros ! 1=print warning if datapoint=0.0 falls outside range, 0=don't

allocate(datah(ndata),weight(ndata),histogram(nbins),histcoord(nbins))
allocate(tempcol(ncolumns))

if (iweightcolumn.eq.0) weight = 1.0

!read data
open(unit=10,file=datafile,action='read')

do i=1,nskip
  read(10,*)
enddo

do i=1,ndata
  read(10,*) (tempcol(ic),ic=1,ncolumns)
  datah(i)=tempcol(idatacolumn)
  if (iweightcolumn.ne.0) weight(i)=tempcol(iweightcolumn)
enddo

close(10)

!calc histogram
call constr_hist(datah,ndata,nbins,valmin,valmax,histogram,histcoord,weight)

!write histogram
open(unit=11,file=outfile)

do i=1,nbins
  write(11,*) histcoord(i),histogram(i)
enddo

close(11)

contains

SUBROUTINE constr_hist(datah,ndata,nbins,tdistmin,tdistmax,hist,histcoord,weight)

! constructs histogram, weighted by population

integer,intent(in) :: ndata,nbins
real(kind=8),intent(in)       :: tdistmin,tdistmax
real(kind=8),dimension(ndata),intent(in) :: datah
real(kind=8),dimension(nbins),intent(out) :: hist
real(kind=8),dimension(nbins),intent(out) :: histcoord
real(kind=8),dimension(ndata),intent(in) :: weight

integer :: i,j,bin
real(kind=8) :: binwidth,halfbinwidth,sumhist

binwidth = (tdistmax-tdistmin)/float(nbins)
halfbinwidth = binwidth*0.5

hist=0.0
histcoord=0.0
sumhist=0.0

do i=1,nbins
  histcoord(i) = (i-1)*binwidth + halfbinwidth + tdistmin
enddo

do i=1,ndata
  bin = ceiling( (datah(i)-tdistmin)/binwidth )
  if ((bin.ge.1).and.(bin.le.nbins)) then
    hist(bin) = hist(bin) + weight(i)
    sumhist = sumhist + weight(i)
  else
    if (printzeros.eq.1) then
      write(*,*) 'Warning: for datapoint ',i,' data = ',datah(i),' which does not fall'
      write(*,*) ' within histogram range ',tdistmin,' to ',tdistmax,' ps'
    endif
  endif
enddo

hist = hist/sumhist

END SUBROUTINE constr_hist

END PROGRAM hist
