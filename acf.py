#calculates autocorrelation function of a timeseries

import sys
import numpy as np

filename = 'pincerangle_run123.dat'
icol     = 1 # in which column in datafile is the data
timestep = 0.25 # in ps, between datapoints
tdecorr  = 0.5 # in ps, decorrelation time
tmax     = 500 # in ps, max time for tcf

itdecorr = int(tdecorr/timestep)
ntmax    = int(tmax/timestep)

data = []
f = open(filename,'r')
for line in f:
  line = line.split()
  data.append(float(line[icol]))

data = np.asarray(data)
mean = np.mean(data)
variance = np.var(data)
data = data - mean
ndatapoints = data.size

timeoriginTimes = np.arange(0,ndatapoints,itdecorr)
timeoriginData  = data[timeoriginTimes]
timeorigins     = zip(timeoriginTimes,timeoriginData)

tcf  = np.zeros(ntmax)
norm = np.zeros(ntmax)

for time in xrange(ndatapoints):
  dx = data[time]
  for time0, dx0 in timeorigins:
     deltat = time - time0 
     if (deltat < 0) or (deltat >= ntmax): continue
     tcf[deltat] += dx0 * dx
     norm[deltat] += 1.0

tcf /= norm
tcf /= variance

for i in xrange(ntmax):
  print i*timestep,tcf[i]
