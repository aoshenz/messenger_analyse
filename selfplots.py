from xml.etree.ElementInclude import include
import matplotlib.pyplot as plt
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


pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', 100)

def plot_hist(x_var, title, x_label, y_label='Frequency', bins=100):
    fig, ax = plt.subplots()
    ax.hist(x_var, bins=10)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.show()


def import_data(inbox_folder, local_file=None, create_new_file=False, limit_files=None):
    """Import messenger data."""

    start_time = time.time()

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

def time_plot(data, include_participants=None, is_direct_msg=None):

    if is_direct_msg != None:
        data = data[data['is_direct_msg']==is_direct_msg]

    # format dates
    data['zzdate'] = data['date'].dt.date

    fig, ax = plt.subplots()

    if include_participants != None:
        for person in include_participants:
            temp = data[data['sender_name'].str.lower().str.contains(person.lower())]

            temp = temp.groupby('zzdate')['content'].count()

            # fill in 0 value for dates with 0 messages
            date_range = pd.date_range(temp.index.min(), temp.index.max())
            temp = temp.reindex(date_range, fill_value=0)
            temp = temp.reset_index().rename(columns={'index': 'zzdate'}) #TODO: how to do these steps without resetting index?

            temp['content_ma'] = temp['content'].rolling(30).mean()

            ax.plot(temp['zzdate'], temp['content_ma'], label=person)

    ax.set_xlabel('Date')
    ax.set_ylabel('Number of messages')
    ax.set_title('Messages over time')

    ax.grid(axis='y', alpha=0.5)
    ax.grid(axis='x', alpha=0.5)

    years = mdates.YearLocator()   # every year
    ax.xaxis.set_major_locator(years)

    plt.legend()
    plt.show()

def rank_msgs(data, top_n=20, is_direct_msg=None):

    if is_direct_msg != None:
        data = data[data['is_direct_msg']==is_direct_msg]

    # exclude yourself TODO: change so that it reads from user profile automatically
    data = data[data['sender_name']!=c.YOUR_FULL_NAME]

    # get list of top senders
    summary = data.groupby('sender_name', as_index=False)['content'].count().sort_values('content', ascending=False)
    summary = summary.head(top_n) # TODO: better way to keep top n
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
    summary = summary.head(top_n) # TODO: better way to keep top n
    top_senders = list(summary['sender_name'].unique())

    # subset table and bar plot
    summary = summary[summary['sender_name'].isin(top_senders)]

    fig, ax = plt.subplots()

    ax.barh(summary['sender_name'], summary['content'])
    ax.invert_yaxis()

    ax.set_xlabel('Number of messages')
    ax.set_ylabel('Friend')
    ax.set_title('Number of messages from friend')

    ax.grid(axis='x', alpha=0.5)
    plt.show()

def wordcloud_plot(data):
    
    data = data[data['num_words'] > 0]

    text = " ".join(msg for msg in data['content'])
    print(f"There are {len(text)} words.")

    wordcloud = WordCloud(background_color='white', width=1600, height=800, colormap='Set2', collocations=False).generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def first_msg(data, include_participants=None):

    # if include_participants == None:
    #     include_participants = rank_msgs(data, top_n=20, is_direct_msg=1)

    # data = data[data['sender_name'].isin(include_participants)]

    # first_msg = data.sort_values('date').groupby('sender_name', as_index=False).first()

    # print(first_msg)

    print(data[data['sender_name'] == 'Ben S Foo'].sort_values('date'))


# rendering
def outputresults():
    
    output_folder = pathlib.Path(__file__).parent.absolute() / "output"
    os.makedirs(output_folder, exist_ok=True)

    os.system(f"open {output_folder}")

def render_template():
