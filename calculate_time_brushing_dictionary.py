# some of the txt files have duplicate coded brushing times because the original
# .cod file that the video file started in was not clean
from os import listdir
import re

txt_path = "/Volumes/Julia_HardDrive/Teeth_Brushing/pilot_txts/"

list_of_txt_folders_to_inspect = [
    "100_recoded",
    "101_txt",
    "102_txt",
    "104_txt",
    "105_txt",
    "106_txt",
    "107_txt",
    "108_txt",
    "109_txt",
    "110_recoded",
    "111_txt",
    "112_txt",
    "113_txt",
    "114_txt",
    "116_txt",
    "117_txt",
    "118_txt",
    "119",
    "120",
    "121",
    "122",
    "123",
    "124",
    "125",
    "127",
]

time_brushing_dictionary = {}

# go through each subject txt folder
for subject_txt_folder in list_of_txt_folders_to_inspect:
    list_of_subject_txt_files = listdir(txt_path+subject_txt_folder+"/")
    # for each of the subject txt files in the subject txt file, find the subject
    # key in the time_brushing_dictionary and create a sub dictionary with the date
    # as the sub key and time_brushing as the value to the sub key
    # Note: not adding the numbers together, just putting them right next to each other
    for subject_txt_file in list_of_subject_txt_files:
        if subject_txt_file.endswith('.txt'):
            # sometimes there is a .DS_store file, only want to open txt files,
            # know that this file is a txt file
            open_subject_txt_file = open(txt_path+subject_txt_folder+"/"+subject_txt_file)
            # separating the txt file by line
            open_subject_txt_file_lines = open_subject_txt_file.readlines()

            time_brushing_milliseconds = 0

            # go through each line
            for open_subject_txt_file_line in open_subject_txt_file_lines:
                # split the string by the comma and get the number in between the commas
                split_line = open_subject_txt_file_line.split(',')
                if len(split_line) > 2 and split_line[2] == 'Time':
                    # add the number in between the commas to time_brushing_milliseconds
                    time_brushing_milliseconds += int(split_line[1])

            time_brushing_seconds = time_brushing_milliseconds/1000

            split_txt_file_name = subject_txt_file.split('-')

            date = split_txt_file_name[1]

            # for the first two pilot subjects, the day of the study is
            # included in the txt file name, need to check if the 3rd index
            # of the file name includes the word day
            if 'pilot1' in split_txt_file_name[3]:
                subject = "100"
            elif 'pilot2' in split_txt_file_name[3]:
                sujbect = "101"
            else:
                subject = split_txt_file_name[2]

            if subject not in time_brushing_dictionary:
                # subject doesn't exist, need to add subject as key
                time_brushing_dictionary[subject] = { date: time_brushing_seconds}
            else:
                # subject already exists, just add a dictionary in the subject key
                time_brushing_dictionary[subject][date] = time_brushing_seconds
