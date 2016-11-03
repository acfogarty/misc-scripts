#Calculates error bars via block averaging using Student's t distribution, 95\% confidence interval
#Reads in list of datafile names from standard input, one for each block
#Column one (xcol) should be identical in all datafiles
#For each datapoint in column two (ycol), calculates average and st dev over all datafiles
#Calculates errorbars from st dev
#Outputs file containing columns: xcol, ycol average, ycol errorbar
#Usage python error_bars_datfile.py < list-of-datafile-names

import sys
import numpy as np

commentChar = '#' #lines in datafiles containing this character are skipped
outfilename = 'out.dat'
nblock = 0.0
xall = []
yall = []

def studentTError(std,nblock):
  '''convert standard deviation to confidence interval using Student's t distribution'''
  #student's t table, 95% confidence interval, two-tailed, key=d.o.f.
  tdist = {1:12.706,2:4.303,3:3.182,4:2.776,5:2.571,6:2.447,7:2.365,8:2.306}
  ndof = nblock - 1.0
  try:
    t = tdist[ndof]
  except KeyError:
    print 'Error! key ',ndof,' must be added to Student''s t table'
    quit()
  return std/np.sqrt(nblock)*t

#loop over datafiles
for line in sys.stdin:
  datafile = line.strip()
  ff = open(datafile,'r')
  x = []
  y = []
  #loop over lines in datafile
  for line2 in ff:
    if commentChar in line2: continue #skip comments
    line2 = line2.split()
    x.append(float(line2[0]))
    y.append(float(line2[1]))
  ff.close()
  #check all datafiles have same length
  if len(xall) != 0 and len(x) != len(xall[-1]):
    print 'File ',datafile,' has ',len(x),' lines of data and the previous file had ',len(xall[-1]),' lines! Error!'
    quit()
  xall.append(x)
  yall.append(y)
  nblock += 1.0

xall = np.asarray(xall)
yall = np.asarray(yall)

#check all files have same first column
for x in xall[1:]:
  if not np.array_equal(x,xall[0]):
    print 'Error! All files should have identical first columns'
    quit()

#calculate average, standard deviation, error
yaverages = np.mean(yall, axis=0)
ystdev = np.std(yall, axis=0, ddof=1) #use Bessel's correction
yerr = studentTError(ystdev, nblock)

#output
of = open(outfilename,'w')
print >> of,'# x y yerr; error is 95% confidence interval using student''s t distribution' 
for x,y,ye in zip(xall[0],yaverages,yerr):
  print >> of,x,y,ye
of.close()

