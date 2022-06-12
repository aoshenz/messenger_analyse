import utils as utils


def main():
    # Data
    # =================================================================
    df = utils.import_data(
        create_new_file=False, limit_files=None  # toggle to True if you need to update
    )

    # Show activity before adjustments
    time_series_all = utils.time_plot_all(df)

    # Apply global data adjustments
    df = utils.apply_adjustments(df)

    # Get report details
    report_details = utils.report_details(df)

    # Summary metrics
    # =================================================================
    overview_metrics = utils.overview_metrics(df)

    # Emojis
    # def plot_emoji_time():
    #     None

    # utils.plot_emoji_bar(df, is_from_me=1)
    # utils.plot_emoji_bar(df, is_from_me=0)

    # # Produce graphs
    # # =================================================================
    # # Bar chart of top friends by messages
    # bar_chart_1 = utils.rank_msgs_barh(df, is_direct_msg=1)
    # bar_chart_2 = utils.rank_msgs_barh(df, is_direct_msg=0)

    # # Stacked bar chart by time of the day
    # hour_day = utils.HourDay(df)
    # plot_hour_day = hour_day.plot_hour_day()
    # hour_day_metrics = hour_day.metrics()

    # # Rank top senders
    # top_senders_1 = utils.rank_msgs(df, top_n=20, is_direct_msg=1)
    # top_senders_2 = utils.rank_msgs(df, top_n=20, is_direct_msg=0)

    # # Time series by friend
    # time_series_1 = utils.time_plot(df, include_participants=top_senders_1, is_direct_msg=1)
    # time_series_2 = utils.time_plot(df, include_participants=top_senders_2, is_direct_msg=0)

    # # Word Cloud
    # # utils.wordcloud_plot(df)

    # # Samples
    # # =================================================================

    # # first_msg = utils.first_msg(df)

    # # Output results
    # # =================================================================
    # info = {
    #     "time_series_all": time_series_all,

    #     "bar_chart_1": bar_chart_1,
    #     "bar_chart_2": bar_chart_2,

    #     "time_series_1": time_series_1,
    #     "time_series_2": time_series_2,

    #     "plot_hour_day": plot_hour_day
    # }

    # utils.output_html(
    #     overview_metrics = overview_metrics,
    #     info = info,
    #     hour_day_metrics = hour_day_metrics,
    #     report_details = report_details)


if __name__ == "__main__":
    main()
