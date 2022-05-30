import pathlib
import selfplots as sp
import config as c


# automated paths TODO: put these lines of code inside the function?
msg_path = pathlib.Path(__file__).parent.absolute() / c.MSG_ROOT_FOLDER
local_copy_file = pathlib.Path(__file__).parent.absolute() / c.LOCAL_COPY

df = sp.import_data(
    msg_path,
    local_copy_file,
    create_new_file=False, # toggle to True if you need to update
    limit_files=None)

# Apply global data adjustments
df = sp.apply_adjustments(df)

# Get report details
report_details = sp.report_details(df)

# Produce graphs
# =================================================================

# Rank top senders
top_senders = sp.rank_msgs(df, top_n=10, is_direct_msg=1)

# Bar chart of top friends by messages
bar_chart_dir_1 = sp.rank_msgs_barh(df, is_direct_msg=1) 

# Stacked bar chart by time of the day
plot_hour_day = sp.plot_hour_day(df)

# Time series by friend
# this double counts it as all participants show up for each msg.... 
# need to just capture sender name i think...
time_series = sp.time_plot(df, include_participants=top_senders, is_direct_msg=None)

# Message length by time of the d 
# ?

# Word Cloud
# sp.wordcloud_plot(df)

# Samples
# =================================================================

first_msg = sp.first_msg(df)

# Output results
# =================================================================
info = {
    "name": c.YOUR_FULL_NAME,
    "time_series": time_series,
    "bar_chart_dir_1": bar_chart_dir_1,
    # "bar_chart_dir_0": bar_chart_dir_0,
    # "first_msg": first_msg,
    "plot_hour_day": plot_hour_day
}

sp.output_html(
    user_info = info,
    report_details = report_details)