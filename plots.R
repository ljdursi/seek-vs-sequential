library(ggplot2)

getData <- function(files, dir)
{
  data <- data.frame()
  for (file in files) {
    filename <- paste0(dir,file,'.time')
    thisdata <- read.table(filename)
    thisdata['TYPE'] <- file
    data <- rbind(data,thisdata)
  }
  names(data) <- c('Fraction','Trial','NumRead','TotalTime','UserTime','SystemTime','Type')
  data$Type <- as.factor(data$Type)
  return(data)
}

dir <- './'
data <- getData( c('zcat-reservoir','cat-reservoir','uncomp-reservoir','uncomp-seek'), dir)
levels(data$Type) <- c('cat | Reservoir', 'Reservoir', 'Seek', 'zcat | Reservoir')
p <- ggplot(data, aes(Fraction, TotalTime, colour = Type)) + stat_smooth(method='loess',aes(fill=Type)) + scale_y_log10(breaks=c(10,25,50,100,250)) + scale_x_log10() + xlab('Fraction of File Read') + ylab('Elapsed Time (s)')
ggsave(p,file=paste0(dir,'uncompress-seek-vs-stream.png'))

gzipdata <- getData( c('reservoir','seek'), dir)
levels(gzipdata$Type) <- c('Reservoir: gzip', 'Seek: gzip')
p2 <- ggplot(gzipdata, aes(Fraction, TotalTime, colour = Type)) + stat_smooth(method='loess',aes(fill=Type)) + scale_y_log10() + scale_x_log10() + xlab('Fraction of File Read') + ylab('Elapsed Time (s)')
ggsave(p2,file=paste0(dir,'gzip-seek-vs-stream.png'))

