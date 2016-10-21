#convert xyz format in Angstrom to gro format in nm
#usage ./xyz2gro-awk.sh filename.xyz filename.gro
#doesn't print box-size as last line of gro file, this must be added afterwards

xyz=$1
gro=$2

# .gro header
echo title > $gro
nlines=$(wc -l < "$xyz")
nlines=expr($nlines-2)
echo $nlines >> $gro

# main contents
tail -$nlines $xyz > temp1
awk '{printf "%5dSOL    %3s%5d%8.3f%8.3f%8.3f\n",(($1+2)/3),$2,$1,$3/10.0,$4/10.0,$5/10.0}' < temp1 >> $gro

echo Add box size at end of .gro file!
echo Warning: gro as input for espresso but maybe not gromacs
