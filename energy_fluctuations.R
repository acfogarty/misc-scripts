#calculate ratio of total energy fluctuations to kinetic energy fluctuations
#uses several definitions of energy fluctuations
#Def 1: DeltaE = <[E-<E>]^2>^0.5 
#Def 2: DeltaE = <[E-E0]^2>^0.5 
#reads input file with columns "cutoff timestep filename", each datafile containing columns headed Ek and Etotal

#definition 1 of DelteE is simply the standard deviation (actually using Bessel's correction)

#definition 2:
calcDeltaE2 <- function(energies) {
  sqrt(sum((energies - energies[1])^2))
}

equiltime <- -1.0 #only calculate energy fluctuations after this time

inputfilename <- "list-esp-files"
datafiles <- read.table(inputfilename, header=TRUE, colClasses=c("numeric","numeric","character"))

print("#cutoff/nm timestep/ps DeltaEk(<E>) DeltaEtotal(<E>) DeltaEk(E0) DeltaEtotal(E0)")
for (i in 1:nrow(datafiles)) {
  data <- read.table(datafiles$filename[i], header=TRUE, sep="", comment.char="")
  equildata = subset(data, X.time>equiltime)
  print(sprintf("%f %f %f %f %f %f",datafiles$cutoff[i],datafiles$timestep[i],sd(equildata$Ek),sd(equildata$Etotal), calcDeltaE2(equildata$Ek), calcDeltaE2(equildata$Etotal)))
}
