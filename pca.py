#!/people/thnfs/homes/wehnerj/python-virtual/bin/python
import MDAnalysis as MD
import MDAnalysis.core.log as MDlog
import numpy as np
from MDAnalysis.analysis.align import *
import numpy.linalg as lg
import sys
import argparse as ap

#calculate PCA of covariance matrix from Cartesian coordinates for a set of atoms
#uses MDAnalysis package for RMSD fit of coordinates

############################
# argument parser
############################

parser = ap.ArgumentParser(description="Calculates PCA for set of atoms. Requires: trj file (.gro), index file (.ndx)")
parser.add_argument('-t',"--trajectory", type=str, help="Trajectory .gro file of the structure")
parser.add_argument('-s',"--steps", type=int, default=0, help="n timesteps to skip at start of trajectory")
parser.add_argument('-n',"--index", type=str, default="index.ndx", help=".ndx file in gromacs format to specify atom groups")
parser.add_argument('-p',"--topology", type=str, help="CHARMM psf file containing topology")
parser.add_argument('-f',"--fileForRMSFit", type=str)
parser.add_argument('-st',"--startframe", type=int)
parser.add_argument('-en',"--endframe", type=int)
args = parser.parse_args()

eigenvalFilename = 'eigenvalues.dat' #output file
fileForRMSFit = args.fileForRMSFit #all frames are RMSD-fit to coordinates in this file
skipframe = 1 #only analyse every skipframe-th frame read
startframe = args.startframe #start analysis at startframe-th frame; slicing numbered from 0, although frames are numbered from 1
endframe = args.endframe #end analysis at endframe-th frame

############################
# set-up universe
############################

u = MD.Universe(args.topology,args.trajectory)
start = args.steps
x = u.trajectory.numframes
pm = MDlog.ProgressMeter(x, interval=10)
print "trajectory has {} frames.".format(x)

# select Calpha atoms
calphaSelectionString = "bynum 1:58 or bynum 243 or bynum 59:60 or bynum 261 or bynum 285 or bynum 61:103 or bynum 313 or bynum 104:125"
calpha = u.selectAtoms(calphaSelectionString)
nAtomsSelected = len(calpha)
nCoord = nAtomsSelected*3
print nAtomsSelected,' atoms selected'

# get reference for aligning whole trajectory
ref = MD.Universe(args.topology,fileForRMSFit)

ntimestep = (endframe - startframe) / skipframe
calpha_pos=np.ndarray(shape=(ntimestep,len(calpha),3))
boxcentre = [x*0.5 for x in u.trajectory.ts.dimensions[:3]]

############################
# calculate
############################

#get centred,wrapped and aligned Calpha coordinates
i=0
for ts in u.trajectory[startframe:endframe:skipframe]:
  vector = boxcentre - calpha.coordinates()[0]
  calpha.translate(vector)
  calpha.packIntoBox()
  print ts.frame
  alignto(u,ref,select=calphaSelectionString) #not mass weighted
  calpha_pos[i] = calpha.coordinates()
  i+=1

if (i!=ntimestep):
  print 'problem with value of ntimestep'
  print i,ntimestep
  quit()

ca = np.reshape(calpha_pos, (ntimestep, -1))
print 'Created coordinate matrix of shape ',ca.shape

# make covariance matrix
ca_mean = ca.mean(axis=0)
print 'Created <x> matrix of shape ',ca_mean.shape
delta_ca = ca - ca_mean
print 'Created deltax matrix of shape ',delta_ca.shape
ca_cov = np.zeros((nCoord,nCoord))
for ts in delta_ca:
  ca_cov += np.outer(ts, ts)
ca_cov /= ntimestep #TODO
print 'Created covariance matrix of shape ',ca_cov.shape

#eigenvalue decomposition of covariance matrix
eigenvalues, eigenvectors = lg.eig(ca_cov)
print 'Got eigenvalues matrix of shape ',eigenvalues.shape
print 'Got eigenvectors matrix of shape ',eigenvectors.shape

#sort and print eigenvalues
eigenvalues_sorted = np.sort(eigenvalues)
fo = open(eigenvalFilename,'w')
for i in range(len(eigenvalues_sorted)-1,-1,-1):
  print>>fo,eigenvalues_sorted[i]


