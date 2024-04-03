import os
from dotenv import load_dotenv
import pycoingecko

load_dotenv()
gecko = pycoingecko.CoinGeckoAPI()
symbol_to_id = {i['symbol']:i['id'] for i in gecko.get_coins_list()}  # Not working properly


def get_sentiment(symbol):
    up = symbol_data['sentiment_votes_up_percentage']
    down = symbol_data['sentiment_votes_down_percentage']
    if up > down: return (up-down)/100
    if up < down: return (down-up)/100

def get_socialmedia(symbol):
    pass

def get_news_score(symbol):
    pass

def get_exchange_score(symbol):
    pass

def get_market_score(symbol):
    pass

def make_ta(symbol):
    pass

def update_ranking():
    pass

def get_token_data(symbol):    
    symbol_data = gecko.get_coin_by_id()
    # Generate dict from results of score functions
    return {
        'id': symbol_to_id[symbol],
        'sentiment': get_sentiment(symbol),
        'social': get_socialmedia(symbol),
        'news': get_news_score(symbol),
        'exchange': get_exchange_score(symbol),
        'ta': make_ta(symbol)
    }
