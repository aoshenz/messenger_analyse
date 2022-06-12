## Messenger data analysis

### Ideas
- Overview numbers
    - Total number of words (you vs from others)
    - Total number of messages (you vs from others)
- Overview graphs
    - Messages over time (hour, day of the week, years)
        - by sent/received
    - Net friends over time
    - Who you follow over time
    - Emojis used over time
- People
    - Bar chart of most number of messages
    - Ratio of messages (Them vs you)
    - Number of messages over time for specific person
- Words
    - Distribution of number of words per message
    - Top words
    - Top emojis
- Sentimentality
    - Mood by time of the day
- Median time between messages (to gauge closeness)
- Number of group chats shared with each person (also to gauge closeness)
- Samples
    - First message to a person!
- External data
    - Weather

### Definitions
- Words
- Messages
- Started conversation e.g. a new conversation is when there's 0 messages between friends for 24 hrs

### Inspiration
- [Towardsdatascience post](https://towardsdatascience.com/download-and-analyse-your-facebook-messenger-data-6d1b49404e09)
    - activity trend over time
    - usage on weekday vs weekend
    - usage on day vs night
    - most frequent phrase/word
- [Parse FB JSON files to tables](https://github.com/numbersprotocol/fb-json2table)

### Improvements
- logging (i.e. printing to console in a nice format)
- error handling
- OOP
- interactive plots using dash (e.g. with dropdowns, filters)
- HTML improvements (e.g. tabs, formatting tables)

### Current limitations
- Assumes Sydney timezone for all messages (i.e. converts UTC to Sydney time)
- Unsure how group chats are structured where participants can come and go


### Instructions
0. Download Facebook information (messages, personal information, friends) (low media quality, JSON, all time)
1. Clone repo
2. Within 'messenger_analyse', create a folder called 'personal_data'. Unzip facebook data here.
3. Create a virtual environment and install packages from `requirements.txt`

### What this script does
1. Reads in your Messenger data (locally).
2. Creates 2 files: 
    - GZIP file of messenger data so it doesn't need to reimport every run: `/personal_data/df.gzip`
    - Outputs analysis: `/output`
3. Produces a `html` analysis, allowing you to explore your data.


### Coding improvement questions
1. Should I group functions into classes?
    - When you do `self.example = 2` in one method, does that update the original `self.example`? How do you reference `self.example` in multiple methods without overwriting the original value?
