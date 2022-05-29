import matplotlib.pyplot as plt
import numpy as np
import pathlib
import selfplots as sp
import seaborn as sns
import config as c


# automated paths TODO: put these lines of code inside the function?
msg_path = pathlib.Path(__file__).parent.absolute() / c.MSG_ROOT_FOLDER
local_copy_file = pathlib.Path(__file__).parent.absolute() / c.LOCAL_COPY

# other configs
custom_params = {"axes.spines.right": False, "axes.spines.top": False, "figure.figsize": (12,6)}
sns.set_theme(style="ticks", rc=custom_params)

df = sp.import_data(
    msg_path,
    local_copy_file,
    create_new_file=False, # toggle to True if you need to update
    limit_files=None)


# Number of messages over time (over all time, by day, by year)
# =================================================================

# Rank top senders
top_senders = sp.rank_msgs(
    df, 
    top_n=5,
    is_direct_msg=1)
print(top_senders)

bar_chart = sp.rank_msgs_barh(
    df, 
    top_n=20,
    is_direct_msg=1)


# By day of the week
# days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# df['day'] = df['date'].dt.day_name()
# df_msg_count = df.groupby('day')['content'].count().loc[days_order]

# fig, ax = plt.subplots()
# ax.bar(
#     df_msg_count.index,
#     df_msg_count)
# ax.set_xlabel('Day of the week')
# ax.set_ylabel('Count')
# ax.set_title('Number of messages by day of the week')
# plt.show()




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
    "time_series": time_series,
    "bar_chart": bar_chart,
    "first_msg": first_msg
}



sp.output_html(user_info = info)