# Rename video files of kids brushing their teeth for The Changing Brain

from datetime import datetime, timedelta
import os
import glob

# Open CSV file with new video names
import csv

# create an instance of the data in the csv
# TODO: make it read in any csv with "Teeth brushing evening" in  the beginning?
# Dr. Leonard's local = "/Volumes/Julia_HardDrive/Teeth brushing evening pilot v2 3.20.19_April 2, 2019_07.29.csv"
# Hunter's local development = "/Users/appollo_liu/Desktop/Teeth brushing evening pilot FOR HUNTER.csv"
teeth_brushing_csv = csv.DictReader(open("/Users/appollo_liu/Desktop/Teeth brushing evening pilot FOR HUNTER.csv"))

# set the path to the videos
# Dr. Leonard's local = "/Volumes/Julia_HardDrive/Q9/"
# Hunter's local development = "Users/appollo_liu/Desktop"
path_to_videos = "Users/appollo_liu/Desktop"

# For loop through each row of csv
for row in teeth_brushing_csv:
    # want to rename the video in the path_to_videos to: subject-month-date-year
    recorded_date = row['Recorded Date']
    # want to rename the video in the path_to_videos to :subject-month-date-year
    subject = row['subject']

    # set the video file name that needs to be changed
    current_file_name = row['ResponseId']
    old_file_name = glob.glob(path_to_videos+current_file_name+'*.MOV')

    # recorded_date can be either 6 or 7 characters long depending on if the
    # day in the year is greater than 9
    if recorded_date[4] == "/":
        # recorded_date day is greater than 9
        if int(recorded_date[-5:-3]) < 12:
            # submitted the day after the video was taken, so need to subtract one
            # from the day
            date_minus_1 = datetime(int(recorded_date[5:7])+2000, int(recorded_date[0]), int(recorded_date[2:4])) - timedelta(days=1)

            # convert datetime date_minus_1 to string in format: subject-month-date-year
            new_file_name = "subject"+subject+"-"+date_minus_1.strftime('%m-%d-')[1:]+"19"+".mp4"
        else:
        	new_file_name ="subject"+subject+"-"+recorded_date.replace('/','-')[:7]+".mp4"
    else:
        # recorded_date day is less than or equal to 9
        if int(recorded_date[-5:-3]) < 12:
            # submitted the day after the video was taken, so need to subtract one
            # from the day
            date_minus_1 = datetime(int(recorded_date[5:7])+2000, int(recorded_date[0]), int(recorded_date[2])) - timedelta(days=1)

            # convert datetime date_minus_1 to string in format: subject-month-date-year
            new_file_name = "subject"+subject+"-"+date_minus_1.strftime('%m-%d-')[1:]+"19"+".mp4"
        else:
        	new_file_name ="subject"+subject+"-"+recorded_date.replace('/','-')[:6]+".mp4"

	print os.path.join(path_to_videos, new_file_name)

    # rename current_file_name to new_file_name
    if len(old_file_name) > 0 and os.path.isfile(old_file_name[0]):
        	# file is inside folder, so need to rename
        	os.rename(old_file_name[0], path_to_videos+new_file_name)
    else:
       print "file doesn't exist"
