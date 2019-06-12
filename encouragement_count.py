# edit Teeth Brushing Coding - Video Coding Tracker to combine the encouragements
# from parents on each day of teeth brushing

import csv


def fill_video_coding_tracker(summary_csv_path, tracker_csv_path):
    # open csv file with each parental encouragement, r for reader mode
    summary_csv = csv.DictReader(open(summary_csv_path, 'r'))

    summary_csv_list = list(summary_csv)
    date = summary_csv_list[0]['DATE']
    encouragement_count = 0
    notes = ""

    # set up for adding rows to tracker_csv_path
    fieldnames = ['SUBJECT', 'DATE', 'ENCOURAGEMENT', 'PARENT', 'NOTES']
    # w for writer mode
    tracker_csv_writer = csv.DictWriter(open(tracker_csv_path, 'w'), fieldnames=fieldnames)
    tracker_csv_writer.writeheader()

    # for loop each row of the csv
    for row_index in range(0, len(summary_csv_list) - 1):
        row = summary_csv_list[row_index]
        row_date = row['DATE']
        next_row_date = summary_csv_list[row_index+1]['DATE']
        # add any notes in the row
        notes = notes + row['NOTES']

        if (len(row['PARENTAL ENCOURAGEMENT']) > 0):
            # row contains encouragement, increment encouragement_count
            encouragement_count += 1

        if (row_date != next_row_date):
            # starting a different day on next loop iteration, add a row in the
            # tracker csv that has subject, date, whether the video was coded,
            # total number of parental encouragements, parent, and notes
            row_dictionary = {
                'SUBJECT': row['SUBJECT'],
                'DATE': row_date,
                'ENCOURAGEMENT': encouragement_count,
                'PARENT': row['PARENT'],
                'NOTES': notes
            }

            tracker_csv_writer.writerow(row_dictionary)

            # reset date, encouragement_count, and notes
            date = row_date
            encouragement_count = 0
            notes = ""
        elif (row_index == len(summary_csv_list) - 2):
            # last iteration of for loop, need to add an encouragement for the last row
            row_dictionary = {
                'SUBJECT': row['SUBJECT'],
                'DATE': row_date,
                'ENCOURAGEMENT': encouragement_count + 1,
                'PARENT': row['PARENT'],
                'NOTES': notes
            }

            tracker_csv_writer.writerow(row_dictionary)

leonard_summary_csv_path = ""
leonard_tracker_csv_path = ""
hunter_summary_csv_path = "/Users/appollo_liu/Documents/workspace/Tooth_Brushing/data/Teeth Brushing Coding - pilot4 Summary.csv"
hunter_tracker_csv_path = "/Users/appollo_liu/Documents/workspace/Tooth_Brushing/data/Teeth Brushing Coding - Video Coding Tracker.csv"

fill_video_coding_tracker(hunter_summary_csv_path, hunter_tracker_csv_path)
