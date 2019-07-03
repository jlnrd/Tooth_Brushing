# update the daily teeth brushing data with the right brushing time code
import csv

# first create a dictionary with the subject as the main key, date of the
# best/worst brushing date as the second key and whether that day was the best or
# worse as the value
best_worst_dictionary = {}

first_two_invalid_dates = ['1/31/19', '2/1/19', '2/28/19', '3/1/19', '3/21/19', '3/22/19', '4/3/19', '4/4/19', '6/10/19', '6/11/19']

clean_updated_csv_path = "/Users/appollo_liu/Documents/workspace/Tooth_Brushing/data/clean_updated_brushing.csv"

# open csv file with each parental encouragement, r for reader mode
clean_updated_csv = csv.DictReader(open(clean_updated_csv_path, 'r'))
clean_updated_csv_list = list(clean_updated_csv)

# best and worst brushing are arrays: [date, brushing time]
best_brushing = []
worst_brushing = []
# go through each row of the csv
for row_index in range(0, len(clean_updated_csv_list)-1):
    # check if the row has a valid date, doesn't have a serious other factor,
    # and submitted a survey that day (check that parent stress is filled)
    row_date = clean_updated_csv_list[row_index]['date']
    serious_other_factors = clean_updated_csv_list[row_index]['serious_other_factors']
    parent_stress = clean_updated_csv_list[row_index]['parent_stress']
    if (row_date not in first_two_invalid_dates) and (serious_other_factors == '0') and (parent_stress != "NA"):
        # this day's brushing time is valid
        # update this subject and compare with next row subject
        subject = clean_updated_csv_list[row_index]['subject']
        next_row_subject = clean_updated_csv_list[row_index+1]['subject']
        time_brushing = clean_updated_csv_list[row_index]['time_brushing']

        # sometimes there isn't any brushing, but still valid survey
        if time_brushing == 'NA':
            time_brushing = 0
        time_brushing = float(time_brushing)

        if len(best_brushing) == 0 and len(worst_brushing) == 0:
            # just got to a new subject, set best and worst brushing to the first date
            best_brushing = [row_date, time_brushing]
            worst_brushing = best_brushing
        elif next_row_subject == subject:
            # same subject, continue to adjust best and worst brushing
            if time_brushing > best_brushing[1]:
                # adjust best_brushing time
                best_brushing = [row_date, time_brushing]
            elif time_brushing < worst_brushing[1]:
                # adjust worst_brushing time
                worst_brushing = [row_date, time_brushing]
        else:
            # different subject, need to add the best and worst brushing to the
            # best_worst_dictionary
            best_worst_dictionary[subject] = {best_brushing[0]: "best", worst_brushing[0]: "worst"}

            # reset best and worst brushing
            best_brushing = []
            worst_brushing = []

# need to deal with very last row
last_row_time_brushing = float(clean_updated_csv_list[len(clean_updated_csv_list)-1]['time_brushing'])
# same subject, continue to adjust best and worst brushing
if last_row_time_brushing > best_brushing[1]:
    # adjust best_brushing time
    best_brushing = [row_date, time_brushing]
elif last_row_time_brushing < worst_brushing[1]:
    # adjust worst_brushing time
    worst_brushing = [row_date, time_brushing]

# always need to add the best and worst brushing to the best_worst_dictionary
# for the last subject
best_brushing_date = best_brushing[0]
worst_brushing_date = worst_brushing[0]
best_worst_dictionary[subject] = {best_brushing_date: "best", worst_brushing_date: "worst"}

# # go through each subject and find their best/worst brushing date
# for subject in time_brushing_dictionary:
#     # Note: best_brushing and worst_brushing contains [date, time_brushing]
#     best_brushing = []
#     worst_brushing = []
#     # go through each date and compare the time brushing
#     for date in time_brushing_dictionary[subject]:
#         if first_two_invalid_dates[date] == 0:
#             # don't consider the time brushing from this day
#             continue
#         else:
#             # valid date to compare


# # overwrite the old clean updated file with the new rows
# fieldnames = ['0', 'subject', 'date', 'time_pm', 'nap', 'nap_length', 'time_last_meal', 'amount_eat', 'child_mood', 'parent_mood', 'parent_stress', 'fussy_pm', 'other_factors', 'serious_other_factors', 'teeth_time', 'bed_time', 'time_am', 'wakeup_time', 'wakeup_night', 'times_wakeup_night', 'minutes_wakeup_night', 'fussy_am', 'day', 'wake', 'bed', 'min_up_night', 'time_sleep_nonap', 'time_sleep', 'time_meal', 'timebrush', 'time_since_meal', 'time_brushing', 'parent', 'total_utterances', 'bribe', 'direct_instruction', 'threat', 'pretend_play', 'cheering', 'praise', 'other', 'total_encouragements', 'Day_week', 'brushing_rank', 'study_version']
#
# # w for writer mode
# clean_updated_csv_writer = csv.DictWriter(open(clean_updated_csv_path, 'w'), fieldnames=fieldnames)
# clean_updated_csv_writer.writeheader()
# clean_updated_csv_writer.writerows(new_clean_updated_csv_rows)
