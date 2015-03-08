#install.packages("rmongodb")
#library(rmongodb)
library(plyr)
library(caret)
library(e1071)

setwd('/Users/snelson/projects/dfuzr')
data<-read.csv('data_for_modeling.csv', stringsAsFactors=FALSE, header=FALSE)
names(data)<-c("name", "prev_vsim_attempts", "dt", "vsim", "prev_prepU_scores")
maxdt<-max(data$dt)
data[data$dt==maxdt,]$vsim=NA


#first vsim score
#first<-read.csv('first_vsim.csv')
#first.1<-first[first["classname"]=='Boot Camp 2014',]
fit <- glm(vsim~prev_vsim_attempts+prev_prepU_scores,data=data,family=binomial())
summary(fit) # display results
new_data<-data[is.na(data$vsim),]
pred<-round(predict(fit, newdata=new_data, type="response")) # predicted values

confusionMatrix(data = data$vsim, pred, positive="1")

merged_data<-cbind(pred, data)

merged_data[merged_data]

