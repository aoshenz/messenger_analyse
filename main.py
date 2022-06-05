import utils as utils

df = utils.import_data(
    create_new_file=False, # toggle to True if you need to update
    limit_files=None)

# Show activity before adjustments
time_series_all = utils.time_plot_all(df)

# Apply global data adjustments
df = utils.apply_adjustments(df)

# Get report details
report_details = utils.report_details(df)

# Summary metrics
# =================================================================

overview_metrics = utils.overview_metrics(df)


# Produce graphs
# =================================================================

# Bar chart of top friends by messages
bar_chart_dir_1 = utils.rank_msgs_barh(df, is_direct_msg=1) 
bar_chart_dir_none = utils.rank_msgs_barh(df, is_direct_msg=None)

# Stacked bar chart by time of the day
hour_day = utils.HourDay(df)
plot_hour_day = hour_day.plot_hour_day()
hour_day_metrics = hour_day.metrics()



# Rank top senders
top_senders_dir_1 = utils.rank_msgs(df, top_n=10, is_direct_msg=1)
top_senders_dir_none = utils.rank_msgs(df, top_n=10, is_direct_msg=None)

# Time series by friend
# this double counts it as all participants s
# how up for each msg.... 
# need to just capture sender name i think...
time_series_dir_1 = utils.time_plot(df, include_participants=top_senders_dir_1, is_direct_msg=1)
time_series_dir_none = utils.time_plot(df, include_participants=top_senders_dir_none, is_direct_msg=None)

# Message length by time of the d 
# ?

# Word Cloud
# utils.wordcloud_plot(df)

# Samples
# =================================================================

first_msg = utils.first_msg(df)


# NLP
# =================================================================



# Output results
# =================================================================
info = {
    "time_series_all": time_series_all,

    "bar_chart_dir_1": bar_chart_dir_1,
    "bar_chart_dir_none": bar_chart_dir_none,

    "time_series_dir_1": time_series_dir_1,
    "time_series_dir_none": time_series_dir_none,

    # "first_msg": first_msg,
    "plot_hour_day": plot_hour_day
}

utils.output_html(
    overview_metrics = overview_metrics,
    info = info,
    hour_day_metrics = hour_day_metrics,
    report_details = report_details)