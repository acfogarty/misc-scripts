import sys
import os
import re

#Combine two xmgrace format files into one, renumbering sets as necessary
#Assumes each file contains only one graph each, i.e. all sets are G0.SX
#In cases of conflict, header info comes from the first file

if len(sys.argv) != 4:
  print "Usage: python ",sys.argv[0],"inputfile1 inputfile2 outputfile1"
  quit()

#files in .agr format to combine
agrfile1 = sys.argv[1]
agrfile2 = sys.argv[2]

#output file name
outfile = sys.argv[3]

#don't overwrite existing file
if os.path.exists(outfile):
  print outfile,' already exists, delete or rename!'
  quit()

#get number of sets in first file
af1 = open(agrfile1,'r')
sets = []
for line in af1:
  if '@target G0.S' in line:
    sets.append(line)
nSetsFile1 = int(sets[-1].strip()[-1]) + 1
af1.close()

#open/re-open all files
of = open(outfile,'a')
af1 = open(agrfile1,'r')
af2 = open(agrfile2,'r')

#write header of first file
line1 = ''
while True:
  line1 = af1.readline()
  if line1.startswith('@target'): break #TODO add eof to condition
  of.write(line1)

#append header of second file, renumbering sets
line2 = ''
while not line2.startswith('@target'):
  line2 = af2.readline()
  if re.match("@    s[0-9]", line2): #if line2 starts with '@    s' followed by digit
    m = re.search("\d", line2) #find first digit, which is the string number
    setNumber = int(line2[m.start()])
    line2 = line2[:m.start()] + str(setNumber + nSetsFile1) + line2[m.start()+1:]
    of.write(line2)

#append data from first file
while True:
  of.write(line1)
  line1 = af1.readline()
  if line1 == '': break

#append data from second file, renumbering sets
while True:
  if line2 == '': break
  if line2.startswith('@target'): #hack, only works for single-digit numbers, TODO
    setNumber = int(line2.strip()[-1])
    line2 = line2.strip()[:-1] + str(setNumber + nSetsFile1) + '\n'
  of.write(line2)
  line2 = af2.readline()

af1.close()
af2.close()
of.close()
