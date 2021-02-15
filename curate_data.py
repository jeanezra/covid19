import pandas as pd
from os import listdir
from os.path import isfile, join
from functools import reduce


path = '/coronavirus-data-extraction/case-hosp-death/'
export_path = '/coronavirus-data-extraction/analysis/'

# Order files to be read by earliest to latest
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
print(onlyfiles)
print(len(onlyfiles))
# 224
sortedfiles = sorted(onlyfiles)

# Track each versioned file
rows = []

for i in sortedfiles[0:]:
    print(i)
    # Note: date format are inconsistent across files (with and without leading zero)
    # Note: schema changed from 4 to 6 columns on 8/19
    # Note: 4/15 schema problem: Retrieving data. Wait a few seconds and try to cut or copy again.
        # Instead of 'DATE_OF_INTEREST'
    try:
        instance = pd.read_table(path + str(i), sep=',', header=0, index_col=None
                                 # , dtype = {'NEW_COVID_CASE_COUNT' : int},
                                 , parse_dates = ['DIAGNOSIS_DATE']
                                 )
    except:
        instance = pd.read_table(path + str(i), sep=',', header=0, index_col=None
                                 # , dtype = {'NEW_COVID_CASE_COUNT' : int},
                                 , parse_dates=['DATE_OF_INTEREST']
                                 )
    try:
        instance.columns = ['DIAGNOSIS_DATE', 'NEW_COVID_CASE_COUNT', 'HOSPITALIZED_CASE_COUNT',
                            'DEATH_COUNT']
    except:
        instance.columns = ['DIAGNOSIS_DATE', 'NEW_COVID_CASE_COUNT', 'HOSPITALIZED_CASE_COUNT',
                            'DEATH_COUNT', 'CASE_COUNT_7DAY_AVG', 'INCOMPLETE']
    instance['commit_datetime'] = i[0:25]
    rows.append(instance[['DIAGNOSIS_DATE', 'NEW_COVID_CASE_COUNT']])

print(len(rows))
# 224

# Compute the cumulative changes by event date and update date
left = 0
right = 1
counter = 1
differences = []

for i in range(0, len(rows) - 1):
    pair = pd.merge(rows[left], rows[right], how='outer', on=['DIAGNOSIS_DATE'])
    pair['diff_' + str(left)] = pair['NEW_COVID_CASE_COUNT_y'] - pair['NEW_COVID_CASE_COUNT_x']
    # print(pair.head())
    differences.append(pair[['DIAGNOSIS_DATE', 'diff_' + str(left)]])
    left += 1
    right += 1

print(len(differences))
# 223

diff_seq = reduce(lambda left, right: pd.merge(left, right, on=['DIAGNOSIS_DATE'],
                                               how='outer'), differences)
print(len(diff_seq['DIAGNOSIS_DATE'].unique()))
# 252

# QA that matrix is appropriately filled
print(diff_seq.shape)
print(diff_seq.head())
print(diff_seq.tail())
# Date format is inconsistent 3/3/20 vs. 03/03/20
non_null = diff_seq.isnull()[diff_seq.isnull() == False].count()
non_null.tail(223).describe()
# count    223.000000
# mean     137.183857
# std       65.248847
# min       24.000000
# 25%       81.500000
# 50%      138.000000
# 75%      193.500000
# max      248.000000
223*137
# 30551
252*223
# 56196
30551/56916
# 0.5367734907583105
# Note: Expect around 50% filled because matrix should be diagonally filled
diff_seq.to_csv(export_path + 'difference_matrix.csv', header=True, index=False)

event_cumulative_diff = pd.DataFrame(diff_seq[diff_seq.columns[1:]].sum(axis=1))
event_cumulative_diff.columns = ['event_cumulative_difference']
cumdiff_event = diff_seq[diff_seq.columns[0:1]].join(event_cumulative_diff)
print(cumdiff_event.shape)
# (252, 2)
print(cumdiff_event.tail())
cumdiff_event.to_csv(export_path + 'difference_by_event_date.csv', header=True, index=False)

global_cumulative_diff = pd.DataFrame(diff_seq[diff_seq.columns[1:]].sum(axis=0))
global_cumulative_diff.columns = ['global_cumulative_difference']
print(global_cumulative_diff.shape)
# (223, 1)
print(global_cumulative_diff.head())
global_cumulative_diff.to_csv(export_path + 'difference_by_update_date.csv', header=True, index=True)
