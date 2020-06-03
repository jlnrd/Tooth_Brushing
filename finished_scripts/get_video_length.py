# create a .csv file that has the subject, date, and video length
import os
import re
import csv
from moviepy.editor import VideoFileClip

video_folders_path = "/Users/appollo_liu/Downloads/"
video_folders = [
    "130",
    "143"
]

video_length_csv_path = video_folders_path+"video_length.csv"

# see if there's already a video length .csv file
if os.path.exists(video_length_csv_path):
    # already ran this program, keep the old video lengths
    old_video_length_csv = csv.DictReader(open(video_length_csv_path, 'r'))
    video_length_rows = list(old_video_length_csv)
else:
    video_length_rows = []

# go through each subject videos folder
for video_folder in video_folders:
    video_files = os.listdir(video_folders_path+video_folder+"/")
    # for each of the video files in the folder, add new row in the video
    # length .csv that has the subject, date, and length of video
    for subject_video_file in video_files:
        if subject_video_file.endswith('.mp4'):
            # sometimes there is a .DS_store or image file, only want to find
            # video file lengths
            # https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
            video_filename = video_folders_path+video_folder+"/"+subject_video_file
            video = VideoFileClip(video_filename)
            video_length = video.duration

            subject = subject_video_file[7:10]
            date = subject_video_file[11:-4]
            video_length_row = {
                'subject': subject,
                'date': date,
                'video_length': video_length
            }
            video_length_rows.append(video_length_row)

# w for writer mode
fieldnames = ['subject', 'date', 'video_length']
video_length_csv_writer = csv.DictWriter(open(video_length_csv_path, 'w'), fieldnames=fieldnames)
video_length_csv_writer.writeheader()
video_length_csv_writer.writerows(video_length_rows)
