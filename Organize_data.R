###########################################
##### merge teeth qualtrics data #########
###########################################


### CLEAN WORKSPACE ###
rm(list=ls())
# load and install binary packages

ipak <- function(pkg){
  new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
  if(length(new.pkg)) install.packages(new.pkg, dependencies = TRUE)
  sapply(pkg, require, character.only = TRUE)
}

packages <- c("ggplot2", "grid", "gridExtra", "ggthemes", "scales", "reshape2",  
              "data.table", "car", "lsmeans", "directlabels", "plyr", "multcomp",
              "RColorBrewer", "sandwich", "effects", "xtable", "coin", 
              "exactRankTests", "texreg", "optimx", "pwr", "WRS2", "dplyr","PerformanceAnalytics","rowr",
              "tidyr", "boot", "lsr","broom","knitr","papaja","apaTables","FSA","psych","data.table","stringr","lubridate")
ipak(packages)


#functions
completeFun <- function(d, desiredCols) {
  completeVec <- complete.cases(d[, desiredCols])
  return(d[completeVec, ])
}

time2decimal <- function(x) {
  x <- as.numeric(x)
  (x[1]+x[2]/60)
}

##################
## read in data ##
##################

#read in evening data 
evening<-read.csv("/Users/appollo_liu/Documents/workspace/changing_brain_lab/Tooth_Brushing/data/evening_031920.csv", header=TRUE, sep = ",")
# evening<-read.csv("/Users/julialeonard/Dropbox (Personal)/julia pc docs/Penn Post-doc/Teeth brushing/Data/Batch 3.19.20 data/evening_031920.csv",header = TRUE, sep = ",")


#rename columns
setnames(evening, old=c("Duration..in.seconds." ,"Did.your.child.nap.today.","How.long.did.your.child.nap.for..in.minutes..","What.time.was.your.child.s.last.meal.","How.much.did.your.child.eat.","What.was.your.child.s.mood.this.evening....1","What.was.your.mood.this.evening....1","What.was.your.stress.level.this.evening.","Are.there.any.other.things.going.on.today.that.might.affect.children.s.behavior..such.as.school.closure..sickness..special.holiday..traumatic.event..etc.","What.time.did.your.child.brush.their.teeth.tonight.", "What.time.did.your.child.go.to.bed.tonight.","Did.your.child.do.a.good.job.listening.and.focusing.today....1"  ), 
         new=c("duration", "nap","nap_length","time_last_meal","amount_eat","child_mood_pm","parent_mood_pm","parent_stress_pm","other_factors","teeth_time","bed_time","fussy_pm"))

#split "recorded date" into date column and time column --> https://www.r-bloggers.com/data-manipulation-with-tidyr/
eve<-evening %>% tidyr::separate(Recorded.Date, 
                c("date", "time_pm")," ")

## fix date based on time. If time is less than 12:00 --> minus one day for date!
eve$date<- as.Date(eve$date, "%m/%d/%Y")
eve$date<- str_replace(eve$date, "0020", "2020")
eve$prev_date<-as.character(ymd(eve$date)-days(1))
eve$time_dec<-sapply(strsplit(eve$time_pm,":"),
       function(x) {
         x <- as.numeric(x)
         x[1]+x[2]/60
       }
)
eve$date<-ifelse(eve$time_dec<12, eve$prev_date,eve$date)


#read in morning data and rename column names
morning<-read.csv("/Users/appollo_liu/Documents/workspace/changing_brain_lab/Tooth_Brushing/data/morning_031920.csv", header=TRUE, sep = ",")
# morning<-read.csv("/Users/julialeonard/Dropbox (Personal)/julia pc docs/Penn Post-doc/Teeth brushing/Data/Batch 3.19.20 data/morning_031920.csv",header = TRUE, sep = ",")

#rename columns
setnames(morning, old=c("What.time.did.your.child.wake.up.this.morning.","Did.your.child.wake.up.last.night.", "How.many.times.did.your.child.wake.up.last.night." ,"How.many.minutes.was.your.child.awake.last.night.","What.is.your.child.s.mood.this.morning....1","What.is.your.stress.level.right.now....Click.to.write.Choice.1" ), 
         new=c("wakeup_time", "wakeup_night","times_wakeup_night","minutes_wakeup_night","child_mood_am","parent_stress_am"))

#split "recorded date" into date column and time column
morn<-morning %>% tidyr::separate(Recorded.Date, 
                                 c("date", "time_am")," ")
morn$date<- as.Date(morn$date, "%m/%d/%Y")
morn$date<- str_replace(morn$date, "0020", "2020")

#just collect the data we want and merge
eve_dat<-eve%>%dplyr::select(subject,date,time_pm,nap, nap_length,time_last_meal,amount_eat, child_mood_pm, parent_mood_pm, parent_stress_pm, fussy_pm, other_factors, teeth_time, bed_time)
morn_dat<-morn%>%dplyr::select(subject, date, time_am, wakeup_time, wakeup_night, times_wakeup_night, minutes_wakeup_night, child_mood_am, parent_stress_am)

data<-merge(eve_dat, morn_dat, by =c("subject","date"), all =TRUE)
#merge with day and date file
# day<- read.csv("/Users/julialeonard/Dropbox (Personal)/julia pc docs/Penn Post-doc/Teeth brushing/Data/Batch 3.19.20 data/dates_031920.csv",header = TRUE, sep = ",")
# day$date<-as.Date(day$date, "%m/%d/%Y")
# day$date<- str_replace(day$date, "0020", "2020")
# data<-merge(data, day, by =c("date"), all =TRUE)


### Calculate time sleeping!
# total sleep time without naps includes times kids got up at night
# total sleep includes nap time

data$wake<-as.difftime(as.character(data$wakeup_time), format = "%H:%M",units = "hours")
data$bed<-as.difftime(as.character(data$bed_time), format = "%H:%M",units = "hours")
data$min_up_night<-(as.numeric(data$minutes_wakeup_night)/60)
data$min_up_night[is.na(data$min_up_night)] <- 0
data$nap_length<-(as.numeric(data$nap_length)/60)
data$nap_length[is.na(data$nap_length)] <- 0

# Wake time syncs with previous day's bed time to calculate time sleep, so need to use lag
# When the bed_time is past midnight, need to calculate time_sleep_no_nap a little differently
data$time_sleep_nonap <- ifelse(lag(data$bed) > 3, 24-lag(data$bed)+data$wake-data$min_up_night, data$wake-lag(data$bed)-data$min_up_night)
data<-data %>%
  group_by(subject)

#add nap from THAT DAY
data$time_sleep<-data$time_sleep_nonap+data$nap_length

## calculate time since last meal
data$time_meal <- sapply(strsplit(as.character(data$time_last_meal),":"), time2decimal)
data$timebrush <- sapply(strsplit(as.character(data$teeth_time),":"), time2decimal)
data$time_since_meal<-data$timebrush -data$time_meal

##########################
## merge with vcode ########
##########################

# vcode<- read.csv("/Users/julialeonard/Dropbox (Personal)/julia pc docs/Penn Post-doc/Teeth brushing/Data/Batch 3.19.20 data/batch031920_vcode.csv",header = TRUE, sep = ",")


#rename columns
# setnames(vcode, old=c("SubjectID.Time","Date.Time","totalDuration.Time"), 
#          new=c("subject","date","time_brushing"))

#reformat date information
# vcode$date_int<-as.integer(vcode$date)
# vcode$date_1 <- sub("(.{1})(*)", "\\1/\\", vcode$date)
# vcode$date_reformat <- sub("(.{4})(*)", "\\1/\\", vcode$date_1)
# vcode$date_test<-as.Date(as.character(vcode$date_reformat), "%m/%d/%Y")
# vcode$date<- str_replace(vcode$date_test, "0020", "2020")
# vcode_data<-vcode%>%dplyr::select(subject,date, time_brushing,date)

#reformat data date
#data$date<- as.Date(data$date, "%m/%d/%Y")
#data$date<- str_replace(data$date, "0020", "2020")
# data<-merge(data, vcode_data, by =c("subject","date"), all =TRUE)

##merge with encouragement data
#enc<- read.csv("/Users/julialeonard/Dropbox (Personal)/julia pc docs/Penn Post-doc/Teeth brushing/Data/pilot4_data/pilot4_encouragement.csv",header = TRUE, sep = ",")

#reformat date information
#enc$date_test<-as.Date(as.character(enc$date), "%m/%d/%Y")
#enc$date<- str_replace(enc$date_test, "0019", "2019")
#enc_data<-enc%>%dplyr::select(subject, date, parent, total_utterances, bribe, direct_instruction, threat, pretend_play, cheering, praise, other, total_encouragement)

#reformate data date
#data$datet<- as.Date(data$date, "%m/%d/%Y")
#data$date<- str_replace(data$date, "0020", "2020")
#data<-merge(data, enc_data, by =c("subject","date"), all =TRUE)

# Automating checks
# Make sure wakeup_time is between 4:00-13:00
time_in_hour <- as.integer(format(strptime(data$wakeup_time, "%H:%M"), '%H'))
data$has_wakeup_time_error <- ifelse(time_in_hour > 4 & time_in_hour < 13, FALSE, TRUE)
# Make sure bed_time is between 18:00-3:00
time_in_hour <- as.integer(format(strptime(data$bed_time, "%H:%M"), '%H'))
data$has_bed_time_error <- ifelse(time_in_hour > 3 & time_in_hour < 18, FALSE, TRUE)
# Make sure sleep > 2
data$has_time_sleep_error <- ifelse(as.integer(data$time_sleep) > 2, FALSE, TRUE)


#write out csv
write.csv(data, "/Users/appollo_liu/Documents/workspace/changing_brain_lab/Tooth_Brushing/data/complete_day_031920.csv")
# write.csv(data,'/Users/julialeonard/Dropbox (Personal)/julia pc docs/Penn Post-doc/Teeth brushing/Data/Batch 3.19.20 data/teeth_merged_031920_all.csv')


#merge with older csv
##older<- read.csv("/Users/julialeonard/Dropbox (Personal)/julia pc docs/Penn Post-doc/Teeth brushing/Data/merged/pilot_041919_merged_n19.csv",header = TRUE, sep = ",")
#l <- list(data, older)
#test<-do.call(rbind.fill, l)
#write.csv(test,'/Users/julialeonard/Dropbox (Personal)/julia pc docs/Penn Post-doc/Teeth brushing/Data/merged/test.csv')
