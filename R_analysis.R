#install.packages("rmongodb")
#library(rmongodb)
library(plyr)
library(caret)
library(e1071)

setwd('Documents/Gnip/2015-02-21_WK/pinpoint_analysis/')
data<-read.csv('data_4_R.csv', header=FALSE)
colnames(data)<-c("student_name", 
                  "vsim_counts", 
                  "vsim_date", 
                  "vsim_score", 
                  "prepU_counts", 
                  "prepU_median", 
                  "prepU_mean", 
                  "prepU_stdev", 
                  "prepU_lag1","prepU_lag2","prepU_lag3","prepU_lag4","prepU_lag5","prepU_lag6","prepU_lag7","prepU_lag8","prepU_lag9","prepU_lag10","prepU_lag11","prepU_lag12","prepU_lag13","prepU_lag14","prepU_lag15","prepU_lag16","prepU_lag17","prepU_lag18","prepU_lag19","prepU_lag20", 
                  "overall_ml_counts", 
                  "overall_ml_median", 
                  "overall_ml_mean", 
                  "overall_ml_stdev", 
                  "overall_ml_lag1","overall_ml_lag2","overall_ml_lag3","overall_ml_lag4","overall_ml_lag5","overall_ml_lag6","overall_ml_lag7","overall_ml_lag8","overall_ml_lag9","overall_ml_lag10","overall_ml_lag11","overall_ml_lag12","overall_ml_lag13","overall_ml_lag14","overall_ml_lag15","overall_ml_lag16","overall_ml_lag17","overall_ml_lag18","overall_ml_lag19","overall_ml_lag20")
data$student_name <- as.character(data$student_name)
data$vsim_date <- strptime(data$vsim_date, format = "%Y-%d-%m %H:%M:%S", tz = "GMT")
head(data)
summary(data)
class(data$overall_ml_lag20)
class(data$student_name)
class(data$vsim_date)

data[sapply(data, is.factor)] <- lapply(data[sapply(data, is.factor)], as.character)
class(data$overall_ml_lag20)
class(data$student_name)
class(data$vsim_date)
data$student_name <- as.factor(data$student_name)

data[sapply(data, is.character)] <- lapply(data[sapply(data, is.character)], as.numeric)
class(data$overall_ml_lag20)
class(data$student_name)
class(data$vsim_date)
data$student_name <- as.character(data$student_name)
summary(data)


#######
####### Scotty's work below
#######
data<-read.csv('data_4_R.csv', stripchartngsAsFactors=FALSE, header=FALSE)
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

