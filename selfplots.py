from unicodedata import category
from xml.etree.ElementInclude import include
import matplotlib.pyplot as plt
import plotly.express as px
import pathlib
import pandas as pd
import json
import numpy as np
import matplotlib.dates as mdates
import time
import config as c
from wordcloud import WordCloud
import os
import pkg_resources
from jinja2 import Template
from datetime import datetime


pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', 100)

def check_data_exists():

    # Check paths
    # Check required files exist
    # Check config formats
    # Output in log
    None

def import_data(inbox_folder, local_file=None, create_new_file=False, limit_files=None):
    """Import messenger data."""

    start_time = time.time()

    local_file = pathlib.Path(__file__).parent.absolute() / "personal_data/df.gzip"

    if pathlib.Path(local_file).is_file() & create_new_file==False:
        print(f"Local copy detected at: {local_file}")
        print(f"Importing this file.")
        df = pd.read_parquet(local_file)
        return df

    msg_folders = []
    for path in pathlib.Path(inbox_folder).rglob('message_*.json'):
        msg_folders.append(path)

    if limit_files != None:
        msg_folders = msg_folders[0:limit_files]

    df = pd.DataFrame()
    for i, msg_folder in enumerate(msg_folders):
        with open(msg_folder) as f:
            msg_json = json.load(f)
        
        df_temp = pd.DataFrame(msg_json['messages'])

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
    col_to_keep = ['participants', 'sender_name', 'timestamp_ms', 'content', 'type']
    df = df[col_to_keep]

    # # map timestamps TODO: automate correct timezone instead of assuming Sydney
    df['date'] = pd.to_datetime(df['timestamp_ms'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Australia/Sydney')
    df.drop('timestamp_ms', inplace=True, axis=1)

    # metric variables
    df['num_words'] = df['content'].str.split().str.len()
    df['num_participants'] = df['participants'].str.split(",").str.len()

    # flags
    df['is_from_me'] = np.where(df['sender_name'] == c.YOUR_FULL_NAME, 1, 0)
    df['is_direct_msg'] = np.where(df['num_participants'] == 2, 1, 0)

    print(f"Messages imported: {len(df)}")

    df.to_parquet(local_file, compression='gzip')
    print(f"Saved a copy of the data here: {local_file}")
    print(f"Time taken: {time.time() - start_time}")

    return(df)

def apply_adjustments(data):

    if (c.DATA_FROM != None) & (c.DATA_TIL != None):
        return data[(data['date'] >= c.DATA_FROM) & (data['date'] <= c.DATA_TIL)]
    elif c.DATA_FROM != None:
        return data[data['date'] >= c.DATA_FROM]
    elif c.DATA_TIL != None:
        return data[data['date'] >= c.DATA_TIL]
    else:
        return data

def report_details(data):

    # Run time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Earliest data date
    date_min = data['date'].dt.date.min()

    # Latest data date
    date_max = data['date'].dt.date.max()

    return {
        "now": now,
        "date_min": date_min,
        "date_max": date_max}

def time_plot(data, include_participants=None, is_direct_msg=None):

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

            temp['# of Messages'] = temp['content'].rolling(30).mean()
            temp['Friend'] = person

            plot_data = plot_data.append(temp)

    fig = px.line(
            plot_data,
            x="Date",
            y="# of Messages",
            color="Friend")

    return fig.to_html(full_html=False, include_plotlyjs=True)

def rank_msgs(data, top_n=20, is_direct_msg=None):

    if is_direct_msg != None:
        data = data[data['is_direct_msg']==is_direct_msg]

    # exclude yourself TODO: change so that it reads from user profile automatically
    data = data[data['sender_name']!=c.YOUR_FULL_NAME]

    # get list of top senders
    summary = data.groupby('sender_name', as_index=False)['content'].count().sort_values('content', ascending=False)
    summary = summary.head(top_n)
    top_senders = list(summary['sender_name'].unique())

    return top_senders

#TODO: need to refactor this function
def rank_msgs_barh(data, top_n=20, is_direct_msg=None):

    if is_direct_msg != None:
        data = data[data['is_direct_msg']==is_direct_msg]

    # exclude yourself TODO: change so that it reads from user profile automatically
    data = data[data['sender_name']!=c.YOUR_FULL_NAME]

    # get list of top senders
    summary = data.groupby('sender_name', as_index=False)['content'].count().sort_values('content', ascending=False)
    summary = summary.head(top_n)
    top_senders = list(summary['sender_name'].unique())

    #TODO: think about changing this to DMs only and use participants so we can color 
    # "if_from_me" in the plot

    fig = px.bar(
            summary,
            x="content",
            y="sender_name",
            orientation='h',
            labels={
                "content": "# of messages",
                "sender_name": "Friend"
            })
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})

    return fig.to_html(full_html=False, include_plotlyjs=True)

def plot_hour_day(data):

    data['day'] = data['date'].dt.day_name()
    data['hour'] = data['date'].dt.hour

    df_msg_count = data.groupby(['hour', 'day'], as_index=False)['content'].count()

    fig = px.bar(
        df_msg_count,
        x='hour',
        y="content",
        color="day",
        labels={
            "hour": "Hour",
            "content": "# of messages",
            "day": "Day"
        },
        category_orders={"day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]})
    fig.update_xaxes(dtick=1)

    return fig.to_html(full_html=False, include_plotlyjs=True)

def wordcloud_plot(data):
    
    data = data[data['num_words'] > 0]

    text = " ".join(msg for msg in data['content'])
    print(f"There are {len(text)} words.")

    wordcloud = WordCloud(background_color='white', width=1600, height=800, colormap='Set2', collocations=False).generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def first_msg(data, include_participants=None):

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

    os.system(f"open {output_path}")
