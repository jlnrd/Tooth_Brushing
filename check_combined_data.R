# Check the combined teeth brushing data for new errors that might occur

# clean workspace
rm(list=ls())

# load required packages
packages <- c("dplyr")
lapply(packages, library, character.only = TRUE)

#read in combined_data
data<-read.csv("/Users/appollo_liu/Documents/workspace/changing_brain_lab/Tooth_Brushing/data/tooth_data_n44.csv", header=TRUE, sep = ",")

# Reorder the rows based on subject and date
data <- data[order(data$subject, as.Date(data$date, format="%m/%d/%Y")),]

# Check duplicate dates and skipped days
days_between <- as.Date(data$date, format="%m/%d/%Y") - as.Date(lag(data$date), format="%m/%d/%Y")
changing_subject <-data$subject - lag(data$subject)
data$date_error <- ifelse(days_between != 1 & changing_subject == 0, TRUE, FALSE)

# Remove the time_sleep data for days with a date_error
data$time_sleep_nonap <- ifelse(data$date_error, NA, data$time_sleep_nonap)
data$time_sleep <- ifelse(data$date_error, NA, data$time_sleep)

#write out csv
write.csv(data, "/Users/appollo_liu/Documents/workspace/changing_brain_lab/Tooth_Brushing/data/edited_tooth_data_n44.csv", row.names=FALSE)
