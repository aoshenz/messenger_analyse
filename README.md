## Messenger data analysis

### Ideas
- Overview numbers
    - Total number of words (you vs from others)
    - Total number of messages (you vs from others)
- Overview graphs
    - Messages over time (hour, day of the week, years)
        - by sent/received
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