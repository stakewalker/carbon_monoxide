import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from rich import print


# Download and initialize
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def get_news_sentiment():
    sia = SentimentIntensityAnalyzer()
    news_data = requests.get('https://min-api.cryptocompare.com/data/v2/news/?excludeCategories=Sponsored').json()['Data']
    counter = 0
    results = {}
    for i in news_data:
        results[counter] = {
            'title': i['title'],
            'title_sentiment': sia.polarity_scores(i['title'])['compound'],
            'description': i['body'],
            'description_sentiment': sia.polarity_scores(i['body'])['compound']
            }
        counter += 1
    print(results)
        #return results
        

get_news_sentiment()
