# update the daily teeth brushing data with the right brushing time code
import csv
from calculate_time_brushing_dictionary import time_brushing_dictionary

clean_updated_csv_path = "/Users/appollo_liu/Documents/workspace/Tooth_Brushing/data/clean_updated_brushing.csv"

# open csv file with each parental encouragement, r for reader mode
clean_updated_csv = csv.DictReader(open(clean_updated_csv_path, 'r'))
clean_updated_csv_list = list(clean_updated_csv)

new_clean_updated_csv_rows = []

# go through each row of the csv
for old_row in clean_updated_csv_list:
    print('old_row = ', old_row)
    # copy over the data to a variable
    new_row = old_row
    row_subject = new_row['subject']

    # date in old csv comes in as month/date/year without zeros
    # Example: 1/2/19; need to remove all "/" and add a "0" at the beginning
    row_date = "0"+new_row['date'].replace("/", "")
    if len(row_date) == 5:
        # day of the month is single digit, need to add a zero to the beginning
        # of the date to make it the same format as how the txt files are saved
        row_date = row_date[:2] + "0" + row_date[2:]

    if row_date in time_brushing_dictionary[row_subject]:
        # child brushed their teeth this night, edit the time_brushing in the
        # new variable
        new_row['time_brushing'] = time_brushing_dictionary[row_subject][row_date]

    new_clean_updated_csv_rows.append(new_row)

# overwrite the old clean updated file with the new rows
fieldnames = ['0', 'subject', 'date', 'time_pm', 'nap', 'nap_length', 'time_last_meal', 'amount_eat', 'child_mood', 'parent_mood', 'parent_stress', 'fussy_pm', 'other_factors', 'serious_other_factors', 'teeth_time', 'bed_time', 'time_am', 'wakeup_time', 'wakeup_night', 'times_wakeup_night', 'minutes_wakeup_night', 'fussy_am', 'day', 'wake', 'bed', 'min_up_night', 'time_sleep_nonap', 'time_sleep', 'time_meal', 'timebrush', 'time_since_meal', 'time_brushing', 'parent', 'total_utterances', 'bribe', 'direct_instruction', 'threat', 'pretend_play', 'cheering', 'praise', 'other', 'total_encouragements', 'Day_week', 'brushing_rank', 'study_version']

# w for writer mode
clean_updated_csv_writer = csv.DictWriter(open(clean_updated_csv_path, 'w'), fieldnames=fieldnames)
clean_updated_csv_writer.writeheader()
clean_updated_csv_writer.writerows(new_clean_updated_csv_rows)
