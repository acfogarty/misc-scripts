#get number of inodes used in each directory in CWD

workdir=$(pwd)
rm inodes-usage.dat
ls -d */ > list-of-directories

while read dirname
do
  cd $dirname
  echo Now in $dirname
  du --inodes > temp-inodes
  awk '{sum += $1} END {print sum}' < temp-inodes > temp-count
  read inodes < temp-count
  echo $inodes $dirname >> $workdir/inodes-usage.dat
  rm temp-count temp-inodes
  cd $workdir 
done < list-of-directories

rm list-of-directories

sort -n inodes-usage.dat > temp-file; mv temp-file inodes-usage.dat
