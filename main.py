from distutils.command.clean import clean
import utils as utils
from messenger import Messenger
import typer

app = typer.Typer()

@app.command()
def main():

    msg = Messenger()
    msg.analyse()

    charts = {
        "time_series_all": msg.timeseries_all,
        "bar_chart_1": msg.bar_chart_1,
        "bar_chart_2": msg.bar_chart_2,
        "time_series_1": msg.timeseries_1,
        "time_series_2": msg.timeseries_2,
        "plot_hour_day": msg.time_of_day,
        "emoji_sent": msg.emoji_sent,
        "emoji_received": msg.emoji_received,
    }

    utils.output_html(
        overview_metrics=msg.overview_metrics,
        charts=charts,
        hour_day_metrics=msg.hour_day_metrics,
        report_details=msg.report_details,
    )

if __name__ == "__main__":
    app()
