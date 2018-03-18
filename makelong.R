library(data.table)
library(dplyr)

setwd('/home/reid/Desktop/MichelinRestaurants')

d <- fread('output/michelinrestaurants.csv',header=TRUE)
d <- data.table(d)
d[,city:=sub('\n','',city)]
long = melt(d,id.vars=c('name','neighborhood','city'),variable.name='year',value.name='stars')
long[is.na(stars),stars := "None"]

write.csv(long,'longdata.csv',row.names=FALSE)

# Count number of Michelin starred restaurants by city by year
w1 <- long %>% filter(stars %in% c('1','2','3')) %>% group_by(city,year,stars) %>% summarize(ct=n())
w2 <- dcast(w1,city + year ~ stars, value.var='ct',fill=0)
names(w2)[3:5] <- c('onestar','twostars','threestars')
write.csv(w2,'starcountcity.csv',row.names=FALSE)
w2 <- data.table(w2)
w2[,totalstars := onestar + twostars + threestars]

w3 <- w2 %>% select(city,year,totalstars)
w4 <- dcast(w3,year ~ city,value.var="totalstars",fill=0)
write.csv(w4,'widedata.csv',row.names=FALSE)
