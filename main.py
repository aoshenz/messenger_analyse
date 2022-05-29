import matplotlib.pyplot as plt
import numpy as np
import pathlib
import selfplots as sp
import seaborn as sns
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



# Number of messages over time (over all time, by day, by year)
# =================================================================

# Rank top senders
top_senders = sp.rank_msgs(
    df, 
    top_n=10,
    is_direct_msg=1)
print(top_senders)

bar_chart_dir_1 = sp.rank_msgs_barh(df, is_direct_msg=1) 
bar_chart_dir_0 = sp.rank_msgs_barh(df, is_direct_msg=0)

# By day of the week
plot_hour_day = sp.plot_hour_day(df)




# Over time

# this double counts it as all participants show up for each msg.... 
# need to just capture sender name i think...

time_series = sp.time_plot(
    df,
    include_participants=top_senders,
    is_direct_msg=None)


# Message length by time of the d



# sp.plot_hist(
#     df['num_words'],
#     "Distribution of message length (number of words)",
#     "Message length (number of words)")


# Word Cloud
# =================================================================
# Word cloud
# sp.wordcloud_plot(df)




# Samples
# =================================================================

first_msg = sp.first_msg(df)




# Output results

info = {
    "name": c.YOUR_FULL_NAME,
    "data_from": c.DATA_FROM,
    "data_til": c.DATA_TIL,
    "time_series": time_series,
    "bar_chart_dir_1": bar_chart_dir_1,
    "bar_chart_dir_0": bar_chart_dir_0,
    # "first_msg": first_msg,
    "plot_hour_day": plot_hour_day
}



sp.output_html(user_info = info)