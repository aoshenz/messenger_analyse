## Messenger Analyse


## Getting Started
1. Reads in your Messenger data (locally).
2. Creates 2 files: 
    - GZIP file of messenger data so it doesn't need to reimport every run: `/personal_data/df.gzip`
    - Outputs analysis: `/output`
3. Produces a `html` analysis, allowing you to explore your data.


### Installation
0. Download Facebook information (messages, personal information, friends) (low media quality, JSON, all time)
1. Clone repo
2. Within 'messenger_analyse', create a folder called 'personal_data'. Unzip facebook data here.
3. Create a virtual environment and install packages from `requirements.txt`


## Usage


### Definitions
- Words
- Messages
- Started conversation e.g. a new conversation is when there's 0 messages between friends for 24 hrs

### Current limitations
- Assumes Sydney timezone for all messages (i.e. converts UTC to Sydney time)
- Unsure how group chats are structured where participants can come and go

## Future improvements
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

### Inspiration
- [Towardsdatascience post](https://towardsdatascience.com/download-and-analyse-your-facebook-messenger-data-6d1b49404e09)
    - activity trend over time
    - usage on weekday vs weekend
    - usage on day vs night
    - most frequent phrase/word
- [Parse FB JSON files to tables](https://github.com/numbersprotocol/fb-json2table)
