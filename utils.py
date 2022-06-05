from unicodedata import category
from xml.etree.ElementInclude import include
import matplotlib.pyplot as plt
import plotly.express as px
import pathlib
import pandas as pd
import json
import numpy as np
import time
import config as c
from wordcloud import WordCloud
import os
import pkg_resources
from jinja2 import Template
from datetime import datetime, timedelta


pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', 100)

layout = {
    'paper_bgcolor': 'rgba(255,255,255,0.7)',
    'title_x':0.5
    # 'plot_bgcolor': 'rgba(255,255,255,0.5)'
    }

def check_data_exists():

    # Check paths
    # Check required files exist
    # Check config formats
    # Output in log
    None

def import_data(create_new_file=False, limit_files=None):
    """
    Import messenger data, drop unused columns, add flags and saves an output for future runs.
    """

    start_time = time.time()

    local_file = pathlib.Path(__file__).parent.absolute() / "personal_data/df.gzip"
    inbox_folder = pathlib.Path(__file__).parent.absolute() / "personal_data"

    if pathlib.Path(local_file).is_file() & create_new_file==False:
        print(f"Importing previously saved output from: {local_file}")
        df = pd.read_parquet(local_file)
        print(f"Imported.")
        return df

    msg_folders = []
    for path in pathlib.Path(inbox_folder).rglob('message_*.json'):
        msg_folders.append(str(path))

    if limit_files != None:
        msg_folders = msg_folders[0:limit_files]

    df = pd.DataFrame()
    for i, msg_folder in enumerate(msg_folders):
        with open(msg_folder) as f:
            msg_json = json.load(f)
        
        df_temp = pd.DataFrame(msg_json['messages'])
        df_temp['file_path'] = msg_folder

        # participant identifier
        participants_list = []
        for j, value in enumerate(msg_json['participants']):
            temp = list(msg_json['participants'][j].values())[0]

            participants_list.append(temp)

        participants_list = ",".join(participants_list)
        df_temp['participants'] = participants_list

        df = df.append(df_temp)

        if (i+1) % 50 == 0:
            print(f"{i+1} of {len(msg_folders)} imported")
    
    # columns to keep
    col_to_keep = ['participants', 'sender_name', 'timestamp_ms', 'content', 'type', 'file_path']
    df = df[col_to_keep]

    # fix encoding e.g. emojis and apostrophes
    df['content'] = df['content'].apply(lambda x: str(x).encode('latin-1').decode('utf-8'))

    # # map timestamps TODO: automate correct timezone instead of assuming Sydney
    df['date'] = pd.to_datetime(df['timestamp_ms'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Australia/Sydney')
    df.drop('timestamp_ms', inplace=True, axis=1)

    # metric variables
    df['num_words'] = df['content'].str.split().str.len()
    df['num_participants'] = df['participants'].str.split(",").str.len()

    # flags
    name = full_name()
    df['is_from_me'] = np.where(df['sender_name'] == name, 1, 0)
    df['is_direct_msg'] = np.where(df['num_participants'] == 2, 1, 0)

    print(f"Messages imported: {len(df)}")

    df.to_parquet(local_file, compression='gzip')
    print(f"Saved a copy of the data here: {local_file}")

    time_taken = time.time() - start_time
    print(f"Time taken: {round(time_taken/60, 2)} minutes") # TODO: change to MM:SS format
    return(df)


def apply_adjustments(data):
    """Filters data based on dates selected in config."""

    if (c.DATA_FROM != None) & (c.DATA_TIL != None):
        return data[(data['date'] >= c.DATA_FROM) & (data['date'] <= c.DATA_TIL)]
    elif c.DATA_FROM != None:
        return data[data['date'] >= c.DATA_FROM]
    elif c.DATA_TIL != None:
        return data[data['date'] >= c.DATA_TIL]
    else:
        return data

def full_name():
    """Returns your full name."""

    inbox_folder = pathlib.Path(__file__).parent.absolute() / "personal_data"

    for path in pathlib.Path(inbox_folder).rglob('profile_information.json'):
        with open(path) as f:
            data = json.load(f)
    
    return data["profile_v2"]['name']['full_name']


def report_details(data):
    """Dictionary of report details used for analysis output."""

    # Name
    name = full_name()

    # Run time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Earliest data date
    date_min = data['date'].dt.date.min()

    # Latest data date
    date_max = data['date'].dt.date.max()

    return {
        "full_name": name,
        "now": now,
        "date_min": date_min,
        "date_max": date_max,
        "ma_days": c.MOVING_AVG_DAYS}

def overview_metrics(data):
    """Dictionary of interesting metrics."""

    name = full_name()
    
    # Dates
    data_date_diff = data['date'].max() - data['date'].min() + timedelta(days=1)
    days_of_data = data_date_diff.days

    # Number of messages sent/received
    msg_sent = data[data['sender_name']==name]['content'].count()
    msg_received = data[data['sender_name']!=name]['content'].count()

    # Number of words sent/received
    words_sent = data[data['sender_name']==name]['num_words'].sum()
    words_received = data[data['sender_name']!=name]['num_words'].sum()

    # Average words per message sent/received
    words_per_msg_sent = words_sent / msg_sent
    words_per_msg_received = words_received / msg_received

    # Average number of messages per day
    msg_per_day_sent = msg_sent / days_of_data
    msg_per_day_received = msg_received / days_of_data

    var_list = [
        'days_of_data',
        'msg_sent',
        'msg_received',
        'words_sent',
        'words_received',
        'words_per_msg_sent',
        'words_per_msg_received',
        'msg_per_day_sent',
        'msg_per_day_received']

    dict = {}
    for i in var_list:
        num = eval(i)

        if num >= 10:
            num_formatted = "{:,.0f}".format(num)
        else:
            num_formatted = "{:.2f}".format(num)

        dict[i] = num_formatted
    
    return dict

def time_plot_all(data):
    """Time series for all messages received. Not grouping by friends."""
    
    name = full_name()

    data['zzdate'] = data['date'].dt.date
    data = data[data['sender_name']!=name]

    # fill in 0 value for dates with 0 messages
    plot_data = data.groupby('zzdate')['content'].count()
    date_range = pd.date_range(plot_data.index.min(), plot_data.index.max())
    plot_data = plot_data.reindex(date_range, fill_value=0)
    plot_data = plot_data.reset_index().rename(columns={'index': 'Date'}) #TODO: how to do these steps without resetting index?
    plot_data['Number of messages received'] = plot_data['content'].rolling(c.MOVING_AVG_DAYS).mean()

    fig = px.line(
            plot_data,
            x="Date",
            y="Number of messages received")
    
    fig.update_layout(layout)

    return fig.to_html(full_html=False, include_plotlyjs=True)


def time_plot(data, include_participants=None, is_direct_msg=None):
    """Time series by friends."""

    if is_direct_msg != None:
        data = data[data['is_direct_msg']==is_direct_msg]

    # format dates
    data['zzdate'] = data['date'].dt.date

    plot_data = pd.DataFrame()
    if include_participants != None:
        for person in include_participants:
            temp = data[data['sender_name'].str.lower().str.contains(person.lower())]

            temp = temp.groupby('zzdate')['content'].count()

            # fill in 0 value for dates with 0 messages
            date_range = pd.date_range(temp.index.min(), temp.index.max())
            temp = temp.reindex(date_range, fill_value=0)
            temp = temp.reset_index().rename(columns={'index': 'Date'}) #TODO: how to do these steps without resetting index?

            temp['Number of messages received'] = temp['content'].rolling(c.MOVING_AVG_DAYS).mean()
            temp['Friend'] = person

            plot_data = plot_data.append(temp)

    title = 0
    if is_direct_msg==None:
        title = "DMs & group chats"
    elif is_direct_msg==1:
        title = "DMs only"
    elif is_direct_msg==0:
        title = "Group chats only"

    fig = px.line(
            plot_data,
            x="Date",
            y="Number of messages received",
            title=title,
            color="Friend")
    
    fig.update_layout(layout)

    return fig.to_html(full_html=False, include_plotlyjs=True)

def rank_msgs(data, top_n=20, is_direct_msg=None):
    """Return a list of top n friends by number of messages."""

    if is_direct_msg != None:
        data = data[data['is_direct_msg']==is_direct_msg]

    # exclude yourself
    name = full_name()
    data = data[data['sender_name']!=name]

    # get list of top senders
    summary = data.groupby('sender_name', as_index=False)['content'].count().sort_values('content', ascending=False)
    summary = summary.head(top_n)
    top_senders = list(summary['sender_name'].unique())

    return top_senders

#TODO: need to refactor this function
def rank_msgs_barh(data, top_n=20, is_direct_msg=None):
    """Plot a horizontal bar chart by friend and number of messages."""

    if is_direct_msg != None:
        data = data[data['is_direct_msg']==is_direct_msg]

    # exclude yourself
    name = full_name()
    data = data[data['sender_name']!=name]

    # get list of top senders
    summary = data.groupby('sender_name', as_index=False)['content'].count().sort_values('content', ascending=False)
    summary = summary.head(top_n)

    title = 0
    if is_direct_msg==None:
        title = "DMs & group chats (top " + str(top_n) + ")"
    elif is_direct_msg==1:
        title = "DMs only (top " + str(top_n) + ")"
    elif is_direct_msg==0:
        title = "Group chats only (top " + str(top_n) + ")"

    fig = px.bar(
            summary,
            x="content",
            y="sender_name",
            orientation='h',
            title=title,
            labels={
                "content": "Number of messages received",
                "sender_name": ""
            })
    fig.update_layout(yaxis={'categoryorder': 'total ascending', 'tickmode': 'linear'})
    fig.update_layout(layout)

    return fig.to_html(full_html=False, include_plotlyjs=True)


class HourDay:

    def __init__(self, data):
        self.data = data

    def data_count(self):
        self.data['day'] = self.data['date'].dt.day_name()
        self.data['hour'] = self.data['date'].dt.hour

        return self.data.groupby(['hour', 'day'], as_index=False)['content'].count()

    def plot_hour_day(self):
        """Plot bar chart of messages in a 24h period segmented by day of the week."""

        df_msg_count = self.data_count()

        fig = px.bar(
            df_msg_count,
            x='hour',
            y="content",
            color="day",
            labels={
                "hour": "Hour",
                "content": "Number of messages",
                "day": "Day"
            },
            category_orders={"day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]})
        fig.update_xaxes(dtick=1)
        fig.update_layout(layout)

        return fig.to_html(full_html=False, include_plotlyjs=True)
    
    def metrics(self):
        
        df_msg_count = self.data_count().sort_values(['content'], ascending=False)

        hour24 = df_msg_count.iloc[0,0]
        if hour24 == 0:
            hour = "12am"
        elif hour24 >= 12:
            hour = str(hour24 - 12) + "pm"
        else:
            hour = str(hour24) + "am"

        day = df_msg_count.iloc[0,1]

        return {'hour': hour, "day": day}


def wordcloud_plot(data):
    """Plot a wordcloud"""
    
    data = data[data['num_words'] > 0]

    text = " ".join(msg for msg in data['content'])
    print(f"There are {len(text)} words.")

    wordcloud = WordCloud(background_color='white', width=1600, height=800, colormap='Set2', collocations=False).generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def first_msg(data, include_participants=None):
    """Get the first message from each friend."""

    if include_participants == None:
        include_participants = rank_msgs(data, top_n=20, is_direct_msg=1)

    standard_fb_msg = [
        "You can now message and call each other and see info like Active Status and when you've read messages.",
        "You are now connected on Messenger"]

    data = data[
        (data['sender_name'].isin(include_participants)) &
        (data['is_direct_msg']==1) &
        (~data['content'].isin(standard_fb_msg))]

    first_msg = data.sort_values('date').groupby('sender_name', as_index=False).first()

    return first_msg.to_html(classes='mystyle')


# rendering
def output_html(**kwargs):
    """Creates an html output and opens it."""
    
    output_folder = pathlib.Path(__file__).parent.absolute() / "output"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "output_id.html")

    template_contents = pkg_resources.resource_string(
        __name__, "templates/template.html"
    )

    template = Template(template_contents.decode("utf-8"))

    output_str = template.render(**kwargs)

    with open(output_path, "w") as f:
        f.write(output_str)

    print(f"Saved to {output_path}")
    os.system(f"open {output_path}")


# Table of friends
def friends():
    inbox_folder = pathlib.Path(__file__).parent.absolute() / "personal_data"

    for path in pathlib.Path(inbox_folder).rglob('friends.json'):
        with open(path) as f:
            friends_json = json.load(f)
        
    df = pd.DataFrame(friends_json['friends_v2'])
    df['name'] = df['name'].apply(lambda x: str(x).encode('latin-1').decode('utf-8'))

    # # map timestamps TODO: automate correct timezone instead of assuming Sydney
    df['date'] = pd.to_datetime(df['timestamp']*1000, unit='ms').dt.tz_localize('UTC').dt.tz_convert('Australia/Sydney')

    keep = ['name', 'date']
    df = df[keep]

    return df

def friends_plot():
    
    data = friends()

    data['date_mth'] = data['date'].dt.date.apply(lambda x : x.replace(day=1))

    data = data.groupby('date_mth', as_index=False)['name'].count()

    fig = px.bar(
            data,
            x="date_mth",
            y="name",
            labels={
                "date_mth": "Date",
                "name": "Number of new friends"
            })

    return fig.to_html(full_html=False, include_plotlyjs=True)


# Interesting stats
def interesting_stats(data):

    data = friends()

    # friends TODO: this doesn't reconcile??
    num_friends = len(data)
    first_friend = data[data['date']==data['date'].min()]['name'].iloc[0]

    None
