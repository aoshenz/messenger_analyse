def time_plot(data, include_participants=None, is_direct_msg=None):

    if is_direct_msg != None:
        data = data[data["is_direct_msg"] == is_direct_msg]

    # format dates
    data["zzdate"] = data["date"].dt.date

    fig, ax = plt.subplots()

    if include_participants != None:
        for person in include_participants:
            temp = data[data["sender_name"].str.lower().str.contains(person.lower())]

            temp = temp.groupby("zzdate")["content"].count()

            # fill in 0 value for dates with 0 messages
            date_range = pd.date_range(temp.index.min(), temp.index.max())
            temp = temp.reindex(date_range, fill_value=0)
            temp = temp.reset_index().rename(
                columns={"index": "zzdate"}
            )  # TODO: how to do these steps without resetting index?

            temp["content_ma"] = temp["content"].rolling(30).mean()

            ax.plot(temp["zzdate"], temp["content_ma"], label=person)

    ax.set_xlabel("Date")
    ax.set_ylabel("Number of messages")
    ax.set_title("Messages over time")

    ax.grid(axis="y", alpha=0.5)
    ax.grid(axis="x", alpha=0.5)

    years = mdates.YearLocator()  # every year
    ax.xaxis.set_major_locator(years)

    plt.legend()
    plt.show()


# TODO: need to refactor this function
def rank_msgs_barh(data, top_n=20, is_direct_msg=None):

    if is_direct_msg != None:
        data = data[data["is_direct_msg"] == is_direct_msg]

    # exclude yourself TODO: change so that it reads from user profile automatically
    data = data[data["sender_name"] != c.YOUR_FULL_NAME]

    # get list of top senders
    summary = (
        data.groupby("sender_name", as_index=False)["content"]
        .count()
        .sort_values("content", ascending=False)
    )
    summary = summary.head(top_n)  # TODO: better way to keep top n
    top_senders = list(summary["sender_name"].unique())

    # subset table and bar plot
    summary = summary[summary["sender_name"].isin(top_senders)]

    fig, ax = plt.subplots()

    ax.barh(summary["sender_name"], summary["content"])
    ax.invert_yaxis()

    ax.set_xlabel("Number of messages")
    ax.set_ylabel("Friend")
    ax.set_title("Number of messages from friend")

    ax.grid(axis="x", alpha=0.5)
    plt.show()


def plot_hist(x_var, title, x_label, y_label="Frequency", bins=100):
    fig, ax = plt.subplots()
    ax.hist(x_var, bins=10)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.show()
