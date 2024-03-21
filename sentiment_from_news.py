import requests
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

news_data = requests.get('https://min-api.cryptocompare.com/data/v2/news/?categories=BTC,ETH&excludeCategories=Sponsored').json()['Data']

# Download and initialize
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    # Use the polarity_scores method to get the sentiment metrics
    sentiment = sia.polarity_scores(text)
    
    # -1 (most extreme negative) and +1 (most extreme positive)
    return sentiment['compound']

counter = 0
for i in news_data:
    print({
        f'id:{counter}',
        i['title'],
        get_sentiment(i['title']),
        i['body'],
        get_sentiment(i['body'])
        })
    counter += 1
