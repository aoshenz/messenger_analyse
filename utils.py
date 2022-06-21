from ast import Pass
from lib2to3.pgen2.pgen import DFAState
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
from wordcloud import WordCloud, STOPWORDS
import os
import pkg_resources
from jinja2 import Template
from datetime import datetime, timedelta
from emoji import EMOJI_DATA
import emojis
from collections import Counter
import personal_data.anon as anon  # DELETE

pd.options.mode.chained_assignment = None
pd.set_option("display.max_rows", 100)

layout = {
    "paper_bgcolor": "rgba(255,255,255,0.7)",
    "title_x": 0.5
    # 'plot_bgcolor': 'rgba(255,255,255,0.5)'
}


def check_data_exists():

    errors = 0

    # Check your profile info exists
    try:
        full_name()
    except:
        print(
            "Failed to gather your name. \nCheck you have downloaded 'Personal Information' and that this file exists 'profile_information.json'"
        )

        errors += 1

    print(f"Number of errors: {errors}")

    # Check paths
    # Check required files exist
    # Check config formats
    # Output in log
    # Check DATA_FROM/TIL is within data range of data
    None


def full_name():
    """Returns your full name."""

    inbox_folder = pathlib.Path(__file__).parent.absolute() / "personal_data"

    for path in pathlib.Path(inbox_folder).rglob("profile_information.json"):
        with open(path) as f:
            data = json.load(f)

    return "Eren Yaeger"  # DELETE
    return data["profile_v2"]["name"]["full_name"]


def import_data(create_new_file=False, limit_files=None):
    """
    Import messenger data, drop unused columns, add flags and saves an output for future runs.
    """

    start_time = time.time()

    local_file = pathlib.Path(__file__).parent.absolute() / "personal_data/df.gzip"
    inbox_folder = pathlib.Path(__file__).parent.absolute() / "personal_data"

    if pathlib.Path(local_file).is_file() & create_new_file == False:
        print(f"Importing previously saved output from: {local_file}")
        df = pd.read_parquet(local_file)
        print(f"Imported.")
        return df

    msg_folders = []
    for path in pathlib.Path(inbox_folder).rglob("message_*.json"):
        msg_folders.append(str(path))

    if limit_files != None:
        msg_folders = msg_folders[0:limit_files]

    df = pd.DataFrame()
    for i, msg_folder in enumerate(msg_folders):
        with open(msg_folder) as f:
            msg_json = json.load(f)

        df_temp = pd.DataFrame(msg_json["messages"])
        df_temp["file_path"] = msg_folder

        # participant identifier
        participants_list = []
        for j, value in enumerate(msg_json["participants"]):
            temp = list(msg_json["participants"][j].values())[0]

            participants_list.append(temp)

        participants_list = ",".join(participants_list)
        df_temp["participants"] = participants_list

        df = df.append(df_temp)

        num_msg_folders = "{:,.0f}".format(len(msg_folders))
        if (i + 1) % 50 == 0:
            i_format = "{:,.0f}".format(i + 1)
            print(f"{i_format} of {num_msg_folders} imported")

    # columns to keep
    col_to_keep = [
        "participants",
        "sender_name",
        "timestamp_ms",
        "content",
        "type",
        "file_path",
    ]
    df = df[col_to_keep]

    # fix encoding e.g. emojis and apostrophes
    df["content"] = df["content"].apply(
        lambda x: str(x).encode("latin-1").decode("utf-8")
    )

    # # map timestamps TODO: automate correct timezone instead of assuming Sydney
    df["datetime"] = (
        pd.to_datetime(df["timestamp_ms"], unit="ms")
        .dt.tz_localize("UTC")
        .dt.tz_convert(c.TIMEZONE)
    )
    df.drop("timestamp_ms", inplace=True, axis=1)

    df["date"] = df["datetime"].dt.date

    # metric variables
    df["num_words"] = df["content"].str.split().str.len()
    df["num_participants"] = df["participants"].str.split(",").str.len()

    # emojis
    df["emojis"] = df["content"].apply(extract_emojis)
    df["has_emoji"] = np.where(df["emojis"].isna(), 0, 1)

    df_length = "{:,.0f}".format(len(df))
    print(f"Messages imported: {df_length}")

    df.to_parquet(local_file, compression="gzip")
    print(f"Saved a copy of the data here: {local_file}")

    time_taken = time.time() - start_time
    print(
        f"Time taken: {round(time_taken/60, 2)} minutes"
    )  # TODO: change to MM:SS format
    return df


def extract_emojis(content):
    list = [i for i in content if i in EMOJI_DATA]

    return " ".join(list) if len(list) > 0 else pd.NA


def apply_adjustments(df):
    """Filters data based on dates selected in config."""

    data = df.copy()

    # Remap names # DELETE
    data["sender_name"].replace(anon.mapping, inplace=True)

    # Keep only 'Messages'
    data = data[data["type"] == "Generic"]
    data = data[
        ~data["content"].str.startswith("Reacted ")
    ]  # Remove messages like "Reacted \u1234 to your message"

    # flags
    name = full_name()
    data["is_from_me"] = np.where(data["sender_name"] == name, 1, 0)
    data["is_direct_msg"] = np.where(data["num_participants"] == 2, 1, 0)

    if (c.DATA_FROM != None) & (c.DATA_TIL != None):
        return data[
            (data["datetime"] >= c.DATA_FROM) & (data["datetime"] <= c.DATA_TIL)
        ]
    elif c.DATA_FROM != None:
        return data[data["datetime"] >= c.DATA_FROM]
    elif c.DATA_TIL != None:
        return data[data["datetime"] >= c.DATA_TIL]
    else:
        return data


def report_details(df):
    """Dictionary of report details used for analysis output."""

    # Name
    name = full_name()

    # Run time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Earliest data date
    date_min = df["date"].min()

    # Latest data date
    date_max = df["date"].max()

    # Flag if data has been subsetted
    is_date_adj = 1 if (c.DATA_FROM != None) | (c.DATA_TIL != None) else 0

    return {
        "full_name": name,
        "now": now,
        "date_min": date_min,
        "date_max": date_max,
        "ma_days": c.MOVING_AVG_DAYS,
        "is_date_adj": is_date_adj,
    }


def overview_metrics(df):
    """Dictionary of interesting metrics."""

    name = full_name()

    # Dates
    data_date_diff = df["date"].max() - df["date"].min() + timedelta(days=1)
    days_of_data = data_date_diff.days

    # Number of messages sent/received
    msg_sent = df[df["sender_name"] == name]["content"].count()
    msg_received = df[df["sender_name"] != name]["content"].count()

    # Number of words sent/received
    words_sent = df[df["sender_name"] == name]["num_words"].sum()
    words_received = df[df["sender_name"] != name]["num_words"].sum()

    # Average words per message sent/received
    words_per_msg_sent = words_sent / msg_sent
    words_per_msg_received = words_received / msg_received

    # Average number of messages per day
    msg_per_day_sent = msg_sent / days_of_data
    msg_per_day_received = msg_received / days_of_data

    var_list = [
        "days_of_data",
        "msg_sent",
        "msg_received",
        "words_sent",
        "words_received",
        "words_per_msg_sent",
        "words_per_msg_received",
        "msg_per_day_sent",
        "msg_per_day_received",
    ]

    dict = {}
    for i in var_list:
        num = eval(i)

        if num >= 10:
            num_formatted = "{:,.0f}".format(num)
        else:
            num_formatted = "{:.2f}".format(num)

        dict[i] = num_formatted

    return dict


def time_plot_all(df):
    """Time series for all messages received. Not grouping by friends."""

    name = full_name()

    data = df[df["sender_name"] != name]

    # fill in 0 value for dates with 0 messages
    plot_data = data.groupby("date")["content"].count()
    date_range = pd.date_range(plot_data.index.min(), plot_data.index.max())
    plot_data = plot_data.reindex(date_range, fill_value=0)
    plot_data = plot_data.reset_index().rename(
        columns={"index": "Date"}
    )  # TODO: how to do these steps without resetting index?
    plot_data["Daily messages received"] = (
        plot_data["content"].rolling(c.MOVING_AVG_DAYS).mean()
    )

    fig = px.line(plot_data, x="Date", y="Daily messages received")

    # highlight section of analysis if data is subsetted
    if (c.DATA_FROM != None) | (c.DATA_FROM != None):
        x_start = c.DATA_FROM or data["date"].min()
        x_end = c.DATA_TIL or data["date"].max()

        x_start = pd.to_datetime(x_start)
        x_end = pd.to_datetime(x_end)

        fig.add_vrect(
            x0=x_start,
            x1=x_end,
            annotation_text="Analysis period",
            annotation_position="top left",
            fillcolor="purple",
            opacity=0.1,
            line_width=0,
        )

    fig.update_layout(layout)

    return fig.to_html(full_html=False, include_plotlyjs=True)


def time_plot(df, include_participants=None, is_direct_msg=None):
    """Time series by friends."""

    data = df.copy()

    if is_direct_msg != None:
        data = data[data["is_direct_msg"] == is_direct_msg]

    plot_data = pd.DataFrame()
    if include_participants != None:
        for person in include_participants:
            temp = data[data["sender_name"].str.lower().str.contains(person.lower())]

            temp = temp.groupby("date")["content"].count()

            # fill in 0 value for dates with 0 messages
            date_range = pd.date_range(temp.index.min(), temp.index.max())
            temp = temp.reindex(date_range, fill_value=0)
            temp = temp.reset_index().rename(
                columns={"index": "Date"}
            )  # TODO: how to do these steps without resetting index?

            temp["Daily messages received"] = (
                temp["content"].rolling(c.MOVING_AVG_DAYS).mean()
            )
            temp["Friend"] = person

            plot_data = plot_data.append(temp)

    title = 0
    if is_direct_msg == None:
        title = "DMs & group chats"
    elif is_direct_msg == 1:
        title = "DMs only"
    elif is_direct_msg == 0:
        title = "Group chats only"

    fig = px.line(
        plot_data, x="Date", y="Daily messages received", title=title, color="Friend"
    )

    fig.update_layout(layout)

    return fig.to_html(full_html=False, include_plotlyjs=True)


def rank_msgs(df, top_n=20, is_direct_msg=None):
    """Return a list of top n friends by number of messages."""

    data = df.copy()

    if is_direct_msg != None:
        data = data[data["is_direct_msg"] == is_direct_msg]

    # exclude yourself
    name = full_name()
    data = data[data["sender_name"] != name]

    # get list of top senders
    summary = (
        data.groupby("sender_name", as_index=False)["content"]
        .count()
        .sort_values("content", ascending=False)
    )
    summary = summary.head(top_n)
    top_senders = list(summary["sender_name"].unique())

    return top_senders


# TODO: need to refactor this function
def plot_msgs_barh(df, top_n=20, is_direct_msg=None):
    """Plot a horizontal bar chart by friend and number of messages."""

    data = df.copy()

    if is_direct_msg != None:
        data = data[data["is_direct_msg"] == is_direct_msg]

    # exclude yourself
    name = full_name()
    data = data[data["sender_name"] != name]

    # get list of top senders
    summary = (
        data.groupby("sender_name", as_index=False)["content"]
        .count()
        .sort_values("content", ascending=False)
    )
    summary = summary.head(top_n)

    title = 0
    if is_direct_msg == None:
        title = "DMs & group chats"
    elif is_direct_msg == 1:
        title = "DMs only"
    elif is_direct_msg == 0:
        title = "Group chats only"

    fig = px.bar(
        summary,
        x="content",
        y="sender_name",
        orientation="h",
        title=title,
        labels={"content": "Daily messages received", "sender_name": ""},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending", "tickmode": "linear"})
    fig.update_layout(layout)

    return fig.to_html(full_html=False, include_plotlyjs=True)


def data_count(df):

    data = df.copy()

    data["day"] = data["datetime"].dt.day_name()
    data["hour"] = data["datetime"].dt.hour

    return data.groupby(["hour", "day"], as_index=False)["content"].count()


def plot_hour_day(df):
    """Plot bar chart of messages in a 24h period segmented by day of the week."""

    df_msg_count = data_count(df)

    fig = px.bar(
        df_msg_count,
        x="hour",
        y="content",
        color="day",
        labels={"hour": "Hour", "content": "Daily messages", "day": "Day"},
        category_orders={
            "day": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        },
    )
    fig.update_xaxes(dtick=1)
    fig.update_layout(layout)

    return fig.to_html(full_html=False, include_plotlyjs=True)


def hour_day_metrics(df):

    df_msg_count = data_count(df).sort_values(["content"], ascending=False)

    hour24 = df_msg_count.iloc[0, 0]
    if hour24 == 0:
        hour = "12am"
    elif hour24 >= 12:
        hour = str(hour24 - 12) + "pm"
    else:
        hour = str(hour24) + "am"

    day = df_msg_count.iloc[0, 1]

    return {"hour": hour, "day": day, "timezone": c.TIMEZONE}


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


# emojis
def plot_emoji_cloud(df, is_from_me=None):

    data = df[df["has_emoji"] == 1]

    if is_from_me != None:
        data = data[data["is_from_me"] == is_from_me]
        file_path = "./output/emoji_cloud_" + str(is_from_me) + ".png"
        if is_from_me == 1:
            header = "From you"
        elif is_from_me == 0:
            header = "From others"
    else:
        file_path = "./output/emoji_cloud_all.png"
        header = "All messages"

    emoji_text = " ".join(msg for msg in data["emojis"])

    emoji_frequencies = Counter(emojis.iter(emoji_text))
    wordcloud = WordCloud(
        font_path="./data/NotoEmoji-Regular.ttf",
        background_color="white",
        width=1600,
        height=800,
        colormap="Set2",
        collocations=False,
    )

    wordcloud.generate_from_frequencies(emoji_frequencies)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.title(header)
    plt.savefig(file_path, format="png", dpi=300)


# text wordcloud
def plot_text_cloud(df, is_from_me=None):
    """Plot a wordcloud"""

    data = df[df["num_words"] > 0]

    if is_from_me != None:
        data = data[data["is_from_me"] == is_from_me]
        file_path = "./output/text_cloud_" + str(is_from_me) + ".png"
        if is_from_me == 1:
            header = "From you"
        elif is_from_me == 0:
            header = "From others"
    else:
        file_path = "./output/text_cloud_all.png"
        header = "All messages"

    text = " ".join(msg for msg in data["content"])

    my_stopwords = list(map(chr, range(97, 123))) + [
        "nan",
        "ll",
    ]  # add letters of the alphabet and other custom words
    custom_stopwords = STOPWORDS.update(my_stopwords)

    wordcloud = WordCloud(
        stopwords=custom_stopwords,
        background_color="white",
        width=1600,
        height=800,
        colormap="Set2",
        collocations=False,
    )

    wordcloud.generate(text)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.title(header)
    plt.savefig(file_path, format="png", dpi=300)
