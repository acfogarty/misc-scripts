import sys
import numpy as np

#outputs mean and std of values in column in datafile

#usage

if (len(sys.argv) != 5):
  print "Average values in columns COL, skipping first SKIP lines, also skipping any lines starting with # or ;, COL numbered from 0"
  print "Usage: python ", sys.argv[0], "<filename of dat file> COL SKIP"
  quit()

# input

datafile=open(sys.argv[1],'r') #file to read
icol=int(sys.argv[2]) #column to average, numbered from 0
skip=int(sys.argv[3]) #no. lines to skip at start of file

# read file

i = 0
values = []
for line in datafile:
  i += 1
  if line.startswith('#') or line.startswith(';'):
    continue
  if (i < skip):
    continue
  llist = line.split()
  values.append(float(llist[icol]))

#output mean,std

values = np.asarray(values)
print 'nvalues: ',values.size
print 'mean: ',np.mean(values)
print 'stderr: ',np.std(values)
print np.mean(values),np.std(values)
