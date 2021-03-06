## Messenger Analyse

The goal of this simple package is to enable you to understand your Facebook Messenger data. It will help you answer questions such as:
- How has my Messenger use changed over time?
- Who have I talked to most over the last few years?
- What are my favourite emojis?
- What hours of the day and week am I most active?

It does this by reading in your Messenger data locally and produces a `html` file, allowing you to explore your data. Below are some snippets from this file.

<div align="center">
<img src="images/all_time_activity.png" alt="drawing" width="800"/>
<img src="images/emojis.png" alt="drawing" width="600"/>
</div>

## How to set up
1. Go to your Facebook [settings](https://www.facebook.com/dyi/?referrer=yfi_settings) > 'Your Facebook Information' > 'Download Your Information' and at a minimum you need to choose these options:
    - File optins in JSON format
    - All time date range
    - Check the boxes for 'Messages' and 'Profile information'

    It takes up to a few days for Facebook to gather this information before you can download it.
<div align="center">
<img src="images/fb_json.png" alt="drawing" width="600"/>
<img src="images/fb_msg.png" alt="drawing" width="600"/>
<img src="images/fb_profile.png" alt="drawing" width="600"/>
</div>


2. Meanwhile, clone this repository. Using your terminal:
```
git clone https://github.com/aoshenz/messenger_analyse.git
```
3. Within `messenger_analyse`, create a folder called `personal_data`. When your Facebook data is ready. Download it and unzip it in this folder. So your folder structure should look like: 
```
messenger_analyse (this repo)
 - personal_data (folder you created)
 -- facebook-your_name (unzipped facebook data)
```
4. Create a virtual environment (optional) and install dependencies from `requirements.txt`. Using your terminal, change directory to `messenger_analyse` and run `pip install -r requirements.txt`.
5. In `config.py`, you can adjust parameters such as which time period of data to use, your local timezone (default: Sydney), moving average days and so on.


## How to use
After you have completed the steps above, you are now ready to run this script. The first run of this script may take a few minutes as it imports your data. It'll save a copy as `/messenger_analyse/personal_data/df.gzip`, where it is used for quicker subsequent re-runs.
### Run from terminal
1. Change directory to the `messenger_analyse` repo folder.
2. Run `python3 main.py`.

For example, it should look something like this:
```
(venv) ???  messenger_analyse git:(master) python3 main.py
```

### Run from notebook
The `Messenger` class contains methods and attributes which allow you to do further exploration. The code below is an example of some useful attributes to help you get started. See [explore.ipynb](https://github.com/aoshenz/messenger_analyse/blob/master/example/explore.ipynb) as a Jupyter Notebook example.
```python
from messenger import Messenger

msg = Messenger()
msg.get_data()
msg.get_metrics()

# Data
msg.data_all # data before adjustments
msg.data_adj # data after adjustments based settings chosen in config.py

# Metrics
msg.report_details # configurations
msg.overview_metrics # data metrics
```

## Future improvements
Here's a list of ideas that I considered during the project but did not implement.
### Data
- Emoji clouds
- Sentimentality
    - Mood by time of the day
- Closeness between friends
    - Median time between messages
    - Number of group chats shared with each person
- Samples
    - First message to a friend
- Net friends over time
- Calls
- External data
    - Weather
- Group chats
    - Unsure how group chats are structured where participants can come and go
### Code
- Better logging to console
- Error handling
- Interactive plots with dropdowns and filters
- HTML improvements (e.g. tabs, formatting tables)

## Inspiration
I started this project with the following personal goals:
- pratice data wrangling with Python
- practice object-oriented programming
- learn basic HTML and CSS
- explore my personal Messenger history

References
- [Download and analyse your facebook messenger data - TowardsDataScience](https://towardsdatascience.com/download-and-analyse-your-facebook-messenger-data-6d1b49404e09)
- [Parse FB JSON files to tables](https://github.com/numbersprotocol/fb-json2table)
