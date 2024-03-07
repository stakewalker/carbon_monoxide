import os
from dotenv import load_dotenv
#import requests
import pycoingecko

load_dotenv()
gecko = pycoingecko.CoinGeckoAPI()
token_id = {i['symbol']:i['id'] for i in gecko.get_coins_list()}  # Not working properly

token_data = gecko.get_coin_by_id()

def get_sentiment(token):
    up = token_data['sentiment_votes_up_percentage']
    down = token_data['sentiment_votes_down_percentage']
    if up > down: return (up-down)/100
    if up < down: return (down-up)/100

def get_socialmedia(token):
    pass

def get_news_score(token):
    pass

def get_exchange_score(token):
    pass

def get_market_score(token):
    pass

def make_ta(token):
    pass

def join_scores():
    pass

def update_ranking():
    pass

def get_token_data(symbol):
    # Gererate dict from the result of score functions
    return {
        'sentiment': get_sentiment(symbol),
        'social': get_socialmedia(symbol),
        'news': get_news_score(symbol),
        'exchange': get_exchange_score(symbol),
        'ta': make_ta(symbol)
    }
    pass
