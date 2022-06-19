import utils as utils


class Messenger:
    def __init__(self, clean_run=False):
        self.clean_run = clean_run

    def analyse(self):

        self.get_data()
        self.get_metrics()
        self.get_charts()

        return None

    def get_data(self):

        data_all = utils.import_data(create_new_file=self.clean_run, limit_files=None)
        data_adj = utils.apply_adjustments(data_all)

        self.data_all = data_all
        self.data_adj = data_adj

        return None

    def get_metrics(self):

        self.report_details = utils.report_details(self.data_adj)
        self.overview_metrics = utils.overview_metrics(self.data_adj)
        self.hour_day_metrics = utils.hour_day_metrics(self.data_adj)

        return None

    def get_charts(self):

        # Time series using all data
        self.timeseries_all = self.plot_timeseries_all()

        # Time series
        self.timeseries_1 = self.plot_timeseries(
            include_participants=None, is_direct_msg=1
        )
        self.timeseries_2 = self.plot_timeseries(
            include_participants=None, is_direct_msg=0
        )

        # Bar chart
        self.bar_chart_1 = self.plot_barchart(is_direct_msg=1)
        self.bar_chart_2 = self.plot_barchart(is_direct_msg=1)

        # Time of day
        self.time_of_day = self.plot_timeofday()

        # Emojis
        self.emoji_sent = self.plot_emojis(is_from_me=1)
        self.emoji_received = self.plot_emojis(is_from_me=0)

        return None

    def plot_timeseries_all(self):

        return utils.time_plot_all(self.data_all)

    def plot_timeseries(self, include_participants=None, is_direct_msg=None):

        if is_direct_msg != None:
            is_direct_msg = is_direct_msg

        if include_participants != None:
            participants_list = include_participants
        else:
            participants_list = utils.rank_msgs(
                self.data_adj, top_n=20, is_direct_msg=is_direct_msg
            )

        plot_ts = utils.time_plot(
            self.data_adj,
            include_participants=participants_list,
            is_direct_msg=is_direct_msg,
        )

        return plot_ts

    def plot_barchart(self, is_direct_msg=None):

        return utils.plot_msgs_barh(self.data_adj, is_direct_msg=is_direct_msg)

    def plot_timeofday(self):

        return utils.plot_hour_day(self.data_adj)

    def plot_emojis(self, is_from_me=1):

        return utils.plot_emoji_bar(self.data_adj, is_from_me=is_from_me)
