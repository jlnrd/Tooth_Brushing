# some of the txt files have duplicate coded brushing times because the original
# .cod file that the video file started in was not clean
from os import listdir
import re

txt_path = "/Volumes/Julia_HardDrive/Teeth_Brushing/pilot_txts/"

list_of_txt_folders_to_inspect = [
    "100_recoded"
]

# list_of_txt_folders_to_inspect = [
#     "100_recoded",
#     "101_txt",
#     "102_txt",
#     "103_txt",
#     "104_txt",
#     "105_txt",
#     "106_txt",
#     "107_txt",
#     "108_txt",
#     "109_txt",
#     "110_recoded",
#     "111_txt",
#     "112_txt",
#     "113_txt",
#     "114_txt",
#     "115_txt",
#     "116_txt",
#     "117_txt",
#     "118_txt",
#     "119",
#     "120",
#     "121",
#     "122",
#     "123",
#     "124",
#     "125",
#     "127",
# ]

coding_duplicates_dictionary = {}

# go through each subject txt folder
for subject_txt_folder in list_of_txt_folders_to_inspect:
    list_of_subject_txt_files = listdir(txt_path+subject_txt_folder+"/")
    # for each of the subject txt files in the subject txt file, find each coded
    # time stamp and add it to the coding duplicates dictionary with the format
    # beginning_brush_timebrushing_length
    # Note: not adding the numbers together, just putting them right next to each other
    for subject_txt_file in list_of_subject_txt_files:
        # open the txt file
        open_subject_txt_file = open(txt_path+subject_txt_folder+"/"+subject_txt_file)

        # separating the txt file by line
        open_subject_txt_file_lines = open_subject_txt_file.readlines()

        # go through each line and take out all of the numbers
        for open_subject_txt_file_line in open_subject_txt_file_lines:
            list_of_numbers_in_line = re.findall(r'\d+', open_subject_txt_file_line)
            if len(list_of_numbers_in_line) == 2:
                # contains start and length of teeth brushing
                key = list_of_numbers_in_line[0] + list_of_numbers_in_line[1]
                if key in coding_duplicates_dictionary:
                    # increment the number of times this code has been duplicated
                    # and add which subject txt file this is
                    coding_duplicates_dictionary[key][0] += 1
                    coding_duplicates_dictionary[key][1].append(subject_txt_file)
                else:
                    coding_duplicates_dictionary[key] = [0, [subject_txt_file]]

# filled the coding_duplicates_dictionary, for loop to find the coding duplicates
for brushing in coding_duplicates_dictionary:
    if coding_duplicates_dictionary[brushing][0] > 0:
        print(brushing)
        print("duplicate coding = ", coding_duplicates_dictionary[brushing])
