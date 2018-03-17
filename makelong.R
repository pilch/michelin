library(data.table)
library(dplyr)

setwd('/home/reid/Desktop/MichelinRestaurants')

d <- fread('output/michelinrestaurants.csv',header=TRUE)
d <- data.table(d)
d[,city:=sub('\n','',city)]
long = melt(d,id.vars=c('name','neighborhood','city'),variable.name='year',value.name='stars')
long[is.na(stars),stars := "None"]

write.csv(long,'longdata.csv',row.names=FALSE)
