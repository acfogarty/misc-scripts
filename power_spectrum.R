#calculate power spectrum
#input data from file with columns: time,data(time), header '#time y'

#get input filename from commandline argument
args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 1) {
  stop("Usage: Rscript power_spectrum.R inputdatafilename", call.=FALSE)
}
inputfilename <- args[1]
outfilename <- "power_spectrum.dat"

data <- read.table(inputfilename, header=TRUE, sep="", comment.char="")

#fft of data with column header 'y'
FT <- Re(fft(data$y))^2
N <- length(FT)/2+1

#get sampling time and Nyquist freq from column with header '#time'
samplingTime <- data$X.time[2]-data$X.time[1]
scanFrequency <- 1.0/samplingTime
nyquistFrequency <- scanFrequency/2.0

frequencies <- seq(0,nyquistFrequency,length=N)

x <- data.frame('freq'=frequencies,'p(freq)'=head(FT,N))

#print # so file can be read with gnuplot etc.
cat('#', file=outfilename)

write.table(x, file=outfilename, row.names=FALSE, append=TRUE)

