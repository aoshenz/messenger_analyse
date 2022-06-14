import utils as utils
import typer

app = typer.Typer()

@app.command()
def main():
    # Data
    # =================================================================
    
    data = utils.LoadData()

    df = data.import_data(
        create_new_file=False, limit_files=None  # toggle to True if you need to update
    )

    # Show activity before adjustments
    time_series_all = utils.time_plot_all(df)

    # Apply global data adjustments
    df = data.apply_adjustments(df)

    # Get report details and metrics
    metrics = utils.Metrics(df)

    # Emojis
    emoji_sent = utils.plot_emoji_bar(df, is_from_me=1)
    emoji_received = utils.plot_emoji_bar(df, is_from_me=0)

    # Charts
    # =================================================================
    # Bar chart of top friends by messages
    bar_chart_1 = utils.rank_msgs_barh(df, is_direct_msg=1)
    bar_chart_2 = utils.rank_msgs_barh(df, is_direct_msg=0)

    # Stacked bar chart by time of the day
    hour_day = utils.HourDay(df)

    # Rank top senders
    top_senders_1 = utils.rank_msgs(df, top_n=20, is_direct_msg=1)
    top_senders_2 = utils.rank_msgs(df, top_n=20, is_direct_msg=0)

    # Time series by friend
    time_series_1 = utils.time_plot(df, include_participants=top_senders_1, is_direct_msg=1)
    time_series_2 = utils.time_plot(df, include_participants=top_senders_2, is_direct_msg=0)

    # Word Cloud
    # utils.wordcloud_plot(df)

    # Output results
    # =================================================================
    charts = {
        "time_series_all": time_series_all,
        "bar_chart_1": bar_chart_1,
        "bar_chart_2": bar_chart_2,
        "time_series_1": time_series_1,
        "time_series_2": time_series_2,
        "plot_hour_day": hour_day.plot_hour_day(),
        "emoji_sent": emoji_sent,
        "emoji_received": emoji_received
    }

    utils.output_html(
        overview_metrics = metrics.overview_metrics(),
        charts = charts,
        hour_day_metrics = hour_day.metrics(),
        report_details = metrics.report_details())

if __name__ == "__main__":
    app()
