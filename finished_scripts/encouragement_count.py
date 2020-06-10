# edit Teeth Brushing Coding - Video Coding Tracker to combine the encouragements
# from parents on each day of teeth brushing

import csv

def fill_video_coding_tracker(summary_csv_path, tracker_csv_path):
    # open csv file with each parental encouragement, r for reader mode
    summary_csv = csv.DictReader(open(summary_csv_path, 'r', encoding='utf-8', errors='ignore'))

    summary_csv_list = list(summary_csv)
    number_of_rows = len(summary_csv_list)

    encouragement_count = {
        "bribe": 0,
        "direct instruction": 0,
        "threat": 0,
        "pretend play": 0,
        "cheering": 0,
        "praise": 0,
        "other": 0
    }

    # set up for adding rows to tracker_csv_path
    fieldnames = ['SUBJECT', 'DATE', 'PARENT', 'BRIBE', 'DIRECT_INSTRUCTION', 'THREAT', 'PRETEND_PLAY', 'CHEERING', 'PRAISE', 'OTHER']
    # w for writer mode
    tracker_csv_writer = csv.DictWriter(open(tracker_csv_path, 'w'), fieldnames=fieldnames)
    tracker_csv_writer.writeheader()

    # for loop each row of the csv through the second to last row
    for row_index in range(0, number_of_rows - 1):
        row = summary_csv_list[row_index]
        row_date = row['DATE']
        next_row_date = summary_csv_list[row_index+1]['DATE']

        if (len(row['PARENTAL ENCOURAGEMENT']) > 0):
            # row contains encouragement, increment specific type of encouragement
            type_of_encouragement = row["FINAL CODE"].lower()
            encouragement_count[type_of_encouragement] += 1

        if (row_date != next_row_date):
            # starting a different day on next loop iteration, add a row in the
            # tracker csv that has subject, date, parent, and encouragements
            row_dictionary = {
                'SUBJECT': row['SUBJECT'],
                'DATE': row_date,
                'PARENT': row['PARENT'],
                'BRIBE': encouragement_count["bribe"],
                'DIRECT_INSTRUCTION': encouragement_count["direct instruction"],
                'THREAT': encouragement_count["threat"],
                'PRETEND_PLAY': encouragement_count["pretend play"],
                'CHEERING': encouragement_count["cheering"],
                'PRAISE': encouragement_count["praise"],
                'OTHER': encouragement_count["other"],
            }

            tracker_csv_writer.writerow(row_dictionary)

            # reset encouragement_count
            encouragement_count = {
                "bribe": 0,
                "direct instruction": 0,
                "threat": 0,
                "pretend play": 0,
                "cheering": 0,
                "praise": 0,
                "other": 0
            }

    # need to add the last row's encouragement
    last_row = summary_csv_list[number_of_rows-1]
    if (row_date == next_row_date):
        # two last rows are for the same day
        if (len(last_row['PARENTAL ENCOURAGEMENT']) > 0):
            type_of_encouragement = row["FINAL CODE"].upper().replace(" ", "_")
            row_dictionary[type_of_encouragement] += 1
            tracker_csv_writer.writerow(row_dictionary)
    else:
        # just need to write in the last row's encouragement
        if (len(last_row['PARENTAL ENCOURAGEMENT']) > 0):
            row_dictionary = {
                'SUBJECT': last_row['SUBJECT'],
                'DATE': next_row_date,
                'PARENT': last_row['PARENT'],
                'BRIBE': 0,
                'DIRECT_INSTRUCTION': 0,
                'THREAT': 0,
                'PRETEND_PLAY': 0,
                'CHEERING': 0,
                'PRAISE': 0,
                'OTHER': 0
            }

            type_of_encouragement = row["FINAL CODE"].upper().replace(" ", "_")
            row_dictionary[type_of_encouragement] += 1

            tracker_csv_writer.writerow(row_dictionary)

hunter_main_path = "/Users/appollo_liu/Documents/workspace/changing_brain_lab/Tooth_Brushing/data/"
hunter_summary_csv_path = hunter_main_path + "parent_coding_raw.csv"
hunter_tracker_csv_path = hunter_main_path + "parent_coding.csv"

fill_video_coding_tracker(hunter_summary_csv_path, hunter_tracker_csv_path)
