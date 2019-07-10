# update the daily teeth brushing data with the right brushing time code
import csv
from find_max_min_time_brushing import best_worst_dictionary

clean_updated_csv_path = "/Users/appollo_liu/Documents/workspace/Tooth_Brushing/data/clean_updated_brushing.csv"

# open csv file with each parental encouragement, r for reader mode
clean_updated_csv = csv.DictReader(open(clean_updated_csv_path, 'r'))
clean_updated_csv_list = list(clean_updated_csv)

new_clean_updated_csv_rows = []

# go through each row of the csv
for old_row in clean_updated_csv_list:
    # copy over the data to a variable
    new_row = old_row
    row_subject = new_row['subject']
    row_date = new_row['date']
    new_row['brushing_rank'] = ""
    if row_date in best_worst_dictionary[row_subject]:
        # this row contains a best or worst brushing day
        new_row['brushing_rank'] = best_worst_dictionary[row_subject][row_date]

    new_clean_updated_csv_rows.append(new_row)

# overwrite the old clean updated file with the new rows
fieldnames = ['0', 'subject', 'date', 'time_pm', 'nap', 'nap_length', 'time_last_meal', 'amount_eat', 'child_mood', 'parent_mood', 'parent_stress', 'fussy_pm', 'fussy_pm_reversed', 'other_factors', 'other_leniant', 'other_stringent', 'sickness', 'teeth_time', 'bed_time', 'time_am', 'wakeup_time', 'wakeup_night', 'times_wakeup_night', 'minutes_wakeup_night', 'fussy_am', 'day', 'wake', 'bed', 'min_up_night', 'time_sleep_nonap', 'time_sleep', 'time_meal', 'timebrush', 'time_since_meal', 'time_brushing', 'brushing_rank', 'parent', 'bribe', 'direct_instruction', 'threat', 'pretend_play', 'cheering', 'praise', 'other', 'total_encouragements', 'total_utterances', 'Day_week', 'study_version']

# w for writer mode
clean_updated_csv_writer = csv.DictWriter(open(clean_updated_csv_path, 'w'), fieldnames=fieldnames)
clean_updated_csv_writer.writeheader()
clean_updated_csv_writer.writerows(new_clean_updated_csv_rows)
