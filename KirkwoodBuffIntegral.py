import sys
import numpy as np
import scipy.integrate as integrate

#calculate Kirkwood Buff Integral as a function of upper integration limit
#i.e kbi = 4*pi*int_{r=0}^{r=rmax}[(g(r)-1.0)*r*r]dr as a function of rmax

#input: datafile containing radial distn function with columns r,g(r)
#output: columns rmax,KBI(rmax)

if len(sys.argv) != 3:
  print "Usage: python ",sys.argv[0],"rdf-file-name outputfilename"
  quit()

#get input file, open, and read RDF
filename = sys.argv[1]
ff = open(filename,'r')
r = [] #distance
gr = [] #rdf
for line in ff:
  if ';' in line: continue
  line = line.split()
  r.append(float(line[0]))
  gr.append(float(line[1]))
r = np.asarray(r)
gr = np.asarray(gr)
ff.close()

#calculate KBI from RDF
kb = (gr - 1.0)*r*r
kbi = integrate.cumtrapz(kb,r,initial=0)
kbi *= 4.0*np.pi

#output
outputfilename = sys.argv[2]
of = open(outputfilename,'w')
of.write('#rmax,KBI(rmax)\n')
for rmax,kbir in zip(r,kbi):
  print >> of,rmax,kbir
of.close
