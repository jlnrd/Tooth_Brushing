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

subject = "100"

# best and worst brushing are arrays: [date, brushing time]
# first set this with empty date and brushing time in between the first subject's
# max and min time_brushing
best_brushing = ['empty date', 10.0]
worst_brushing = ['empty date', 10.0]

# go through each row of the csv
for row_index in range(0, len(clean_updated_csv_list)):
    # first check if the row has a valid date, doesn't have a serious other factor,
    # and submitted a survey that day (check that parent stress is filled)
    row_date = clean_updated_csv_list[row_index]['date']
    serious_other_factors = clean_updated_csv_list[row_index]['serious_other_factors']
    parent_stress = clean_updated_csv_list[row_index]['parent_stress']
    if (row_date not in first_two_invalid_dates) and (serious_other_factors == '0') and (parent_stress != "NA"):
        row_subject = clean_updated_csv_list[row_index]['subject']

        # this day's brushing time is valid
        time_brushing = clean_updated_csv_list[row_index]['time_brushing']
        # sometimes there isn't any brushing, but still valid survey
        if time_brushing == 'NA':
            time_brushing = 0
        time_brushing = float(time_brushing)

        # check if row subject is the same as the previous row's subject
        if row_subject == subject:
            # same subject, continue to adjust best and worst brushing
            if time_brushing > best_brushing[1]:
                # adjust best_brushing time
                best_brushing = [row_date, time_brushing]
            elif time_brushing < worst_brushing[1]:
                # adjust worst_brushing time
                worst_brushing = [row_date, time_brushing]
        else:
            # this is a new subject, need to update the best_worst_dictionary with
            # the previous subject's best and worst brushing
            best_worst_dictionary[subject] = {best_brushing[0]: "best", worst_brushing[0]: "worst"}

            # set best and worst brushing to the this row's time_brushing
            best_brushing = [row_date, time_brushing]
            worst_brushing = best_brushing

            # reset subject
            subject = row_subject

# need to include the very last subject's data
best_worst_dictionary[subject] = {best_brushing[0]: "best", worst_brushing[0]: "worst"}
