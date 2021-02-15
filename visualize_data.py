import pandas as pd
import seaborn as sns
sns.set_theme()
sns.set(rc={'figure.figsize':(12,8)})


path = '/coronavirus-data-extraction/analysis/'

# Show lag reporting over 6 or so months
diff_seq = pd.read_table(path + 'difference_matrix.csv', sep=',', header=0, index_col=False)
print(diff_seq.shape)
print(diff_seq.head())
print(diff_seq.tail())

diff_seq.set_index('DIAGNOSIS_DATE', inplace=True)
print(diff_seq.head())
# Note: raw values show absolute lag; max threshold shows low changes; quantiles relativizes
lag_matrix1 = sns.heatmap(diff_seq, robust=True)
lag_matrix1.set_title('Matrix of case count changes - event date by update counter (quantiles)')
lag_matrix1.get_figure().savefig(path + "matrix_case_count_changes1_quantiles.png")

lag_matrix2 = sns.heatmap(diff_seq, vmax=138, cmap="YlGnBu")
lag_matrix2.set_title('Matrix of case count changes - event date by update counter (max threshold)')
lag_matrix2.get_figure().savefig(path + "matrix_case_count_changes2_max.png")

lag_matrix3 = sns.heatmap(diff_seq)
lag_matrix3.set_title('Matrix of case count changes - event date by update counter (raw)')
lag_matrix3.get_figure().savefig(path + "matrix_case_count_changes3_raw.png")

# Show count by event date
cumdiff_event = pd.read_table(path + 'difference_by_event_date.csv', sep=',', header=0, index_col=False
                              , parse_dates = ['DIAGNOSIS_DATE'])
print(cumdiff_event.shape)
print(cumdiff_event.head())

event_line = sns.lineplot(data=cumdiff_event, x="DIAGNOSIS_DATE", y="event_cumulative_difference")
event_line.set_title("Change in case counts by event date")
event_line.get_figure().savefig(path + "case_counts_by_event_counter.png")

# Show count by update date
global_cumulative_diff = pd.read_table(path + 'difference_by_update_date.csv', sep=',', header=0, index_col=False)
print(global_cumulative_diff.shape)
print(global_cumulative_diff.head())
global_cumulative_diff.columns = ['difference_counter','global_cumulative_difference']

update_line = sns.lineplot(data=global_cumulative_diff, x="difference_counter", y="global_cumulative_difference")
update_line.set_xticklabels(labels=[])
update_line.set_title("Change in case counts by update counter")
update_line.get_figure().savefig(path + "case_counts_by_update_counter.png")
