import utils as utils

# Data
# =================================================================
df = utils.import_data(
    create_new_file=False, # toggle to True if you need to update
    limit_files=None)

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

with_emoji = len(df[df['has_emoji']==1])
without_emoji = len(df[df['has_emoji']==0])
len_df = len(df)
print(with_emoji/len_df)

def plot_emoji_time():
    None



import plotly.express as px
def plot_emoji_bar(data, is_from_me=None):

    data = data[data['has_emoji']==1]

    if is_from_me != None:
        data = data[data['is_from_me']==is_from_me]
    
    emoji_count = data["emojis"].str.split(expand=True).stack().value_counts().rename_axis("emoji").reset_index(name="count")

    emoji_count = emoji_count.head(50)
    fig = px.bar(emoji_count, x="count", y="emoji", orientation="h")
    fig.show()

# plot_emoji_bar(df, is_from_me=1)
# plot_emoji_bar(df, is_from_me=0)







from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import emojis

class EmojiCloud:
    def __init__(self, font_path='./data/NotoEmoji-Regular.ttf'):
        self.font_path = font_path
        self.word_cloud = self.initialize_wordcloud()
        self.emoji_probability = None

        
    def initialize_wordcloud(self):
        return WordCloud(font_path=self.font_path,
                               width=2000,
                               height=1000,
                               background_color='white',
                               random_state=42,
                               collocations=False)

    
    def color_func(self, word, font_size, position, orientation, random_state=None,
                   **kwargs):
        hue_saturation = '42, 88%'

        current_emoji_probability = self.emoji_probability[word]
        if current_emoji_probability >= 0.10:
            opacity = 50
        else:
            opacity = 75 - current_emoji_probability/0.2 * 5
        return f"hsl({hue_saturation},{opacity}%)"

    def generate(self, text):
        emoji_frequencies = Counter(emojis.iter(text))
        total_count = sum(emoji_frequencies.values())
        
        self.emoji_probability = {emoji: count/total_count for emoji, count in emoji_frequencies.items()}
        wc = self.word_cloud.generate_from_frequencies(emoji_frequencies)
        
        plt.figure(figsize=(20,10))
        plt.imshow(wc.recolor(color_func=self.color_func, random_state=42))
        plt.axis("off")
        plt.show()


df = df[df['has_emoji']==1]
emoji_text = " ".join(msg for msg in df['emojis'])

emoji_cloud = EmojiCloud()
emoji_cloud.generate(emoji_text)



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
