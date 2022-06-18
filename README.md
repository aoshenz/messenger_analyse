# Messenger Analyse

The goal of this simple package is to help you better understand your Facebook Messenger data. It reads in your Messenger data locally and produces a `html` file, allowing you to explore your data.

To see what the analysis file will look like, see [here](https://github.com/aoshenz/messenger_analyse/blob/master/example/output_example.html) for an example. Below are some snippets from this file.

<img src="images/headline.png" alt="drawing" width="600"/>
<img src="images/trends.png" alt="drawing" width="600"/>

# Installation
1. Go to your Facebook [settings](https://www.facebook.com/dyi/?referrer=yfi_settings) > 'Your Facebook Information' > 'Download Your Information' and at a minimum you need to choose these options:
- JSON format
- All time date range
- And check the boxes for 'Messages', 'Profile information' and 'Friends and followers'

It takes up to a few days for Facebook to gather this information before you can download it.
<img src="images/fb_json.png" alt="drawing" width="600"/>
<img src="images/fb_msg.png" alt="drawing" width="600"/>
<img src="images/fb_profile.png" alt="drawing" width="600"/>
<img src="images/fb_friends.png" alt="drawing" width="600"/>
2. Meanwhile, clone this repository.
`Instructions here`
3. Within 'messenger_analyse', create a folder called 'personal_data'. Your Facebook data should be in a `.zip` file. Unzip that file here. So your folder structure should look like: 
messenger_analyse (this repo) > personal_data (folder you created) > facebook-your_name (unzipped facebook folders).

4. Create a virtual environment and install packages from `requirements.txt`.


# Usage
## Definitions
- Words
- Messages
- Started conversation e.g. a new conversation is when there's 0 messages between friends for 24 hrs

## Limitations
- Assumes Sydney timezone for all messages (i.e. converts UTC to Sydney time)
- Unsure how group chats are structured where participants can come and go

# Future improvements
### Data
- Emoji clouds
- Sentimentality
    - Mood by time of the day
- Median time between messages (to gauge closeness)
- Number of group chats shared with each person (also to gauge closeness)
- Samples
    - First message to a person!
- Net friends over time
- External data
    - Weather
### Code
- Logging to console
- Error handling
- Interactive plots with dropdowns and filters
- HTML improvements (e.g. tabs, formatting tables)

# Inspiration
- [Towardsdatascience post](https://towardsdatascience.com/download-and-analyse-your-facebook-messenger-data-6d1b49404e09)
    - activity trend over time
    - usage on weekday vs weekend
    - usage on day vs night
    - most frequent phrase/word
- [Parse FB JSON files to tables](https://github.com/numbersprotocol/fb-json2table)
