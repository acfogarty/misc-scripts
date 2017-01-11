#Script for extracting and collating bibtex-format bibliographic records

#Reads a latex file containing citations
#Reads many bibtex files containing many bibliographic references
#Outputs a bibtex file containing only those bibliographic references which are cited in the latex file

#latex-format file which contains reference of the form \cite{key} or \cite{key1,key2,key3...}
texfile = 'psfi-lysozyme.tex'

#list of bibtex-format files which contain bibliographic records identified by key
#i.e. as supplied to \bibliography{} in .tex file
bibfilestring = 'solvation.bib,lysozyme.bib,techniques.bib,adres.bib'
bibfiles = bibfilestring.split(',')

#output bibtex file containing only the records used in texfile
newbibfile = 'Fogarty_Proteins_biblio.bib'

#read all the bibtex files and build a dictionary {key:record}
bibdict={}
for bibfile in bibfiles:

  bf = open(bibfile,'r')

  #initialize
  newrecord = False
  record=[]
  biblabel=''

  for line in bf:

    if '@article' in line.lower() or '@incollection' in line.lower() or '@misc' in line.lower():

      #found a new record

      #add the previous record to the dictionary
      bibdict[biblabel]=record
      print 'adding ',biblabel,' to dict'

      #start a new record
      record=[]
      newrecord=True
      biblabel=line[:-2]
      biblabel=biblabel.replace('@article','')
      biblabel=biblabel.replace('@Article','')
      biblabel=biblabel.replace('@ARTICLE','')
      biblabel=biblabel.replace('@incollection','')
      biblabel=biblabel.replace('@misc','')
      biblabel=biblabel.strip('{ ')
      print 'found ',biblabel

      #print a few warning for non-article records
      if '@incollection' in line.lower(): print 'Change ',line,' manually later to have @incollection instead of @article'
      if '@misc' in line.lower():  print 'Change ',line,' manually later to have @misc instead of @article'

    else:

      #continue adding to the previous record
      record.append(line)

  #add the final record from this file
  bibdict[biblabel]=record
  print 'adding ',biblabel,' to dict'

  bf.close()

#read the tex file
tf = open(texfile,'r')
raw = tf.read()

#localise all keys appearing in the context \cite{key1,key2,key3...}
biblabels = ''
i = 30 #skip start
#go through the text character by character
while i < len(raw)-100:
  if raw[i]=='c':
    #if the character c was found, build a string of 'c' + the following four characters
    check='c'
    for j in xrange(4): 
      i+=1
      check+=raw[i]
      if check=='cite{': #found citation
        nextc = raw[i+1]
        biblabel = ''
        #read the whole string appearing between \cite{ and }
        while nextc!='}':
          i+=1
          biblabel+=raw[i]
          nextc = raw[i+1]
        biblabels+=biblabel
        biblabels+=','
  else:
    i+=1
tf.close()

biblabellist = biblabels.split(',')
print '#list of all keys found in texfile:',biblabellist

#get all unique keys
biblabelset = set(biblabellist)
print '#set of all keys found in texfile:',biblabelset

#output new bibtex file containing all records whose keys are in biblabelset
of = open(newbibfile,'w')
for biblabel in biblabelset:
  of.write('@article{'+biblabel+',\n')
  for line in bibdict[biblabel]:
    of.write(line)
  of.write('\n')
of.close()

