class Token:
    def __init__(self, symbol):
        self.symbol = symbol
        self.id = coingecko_data[symbol]
        self.scores = {'sentiment': get_sentiment(symbol),
                       'socialmedia': get_socialmedia(symbol),
                       'ta': make_technical_analysis(symbol),
                       'news': get_news_score(symbol),
                       'exchange': get_exchange_score(symbol)
                       }
        # join ranking
        # update ranking

class Ranking:
    def __init__(self):
        # check for previous file
        pass
    def update(self):
        # rank by scores
        pass
    def new(self, token):
        # add a new token to the ranking
        pass
    def remove(self, token):
        # remove token from the list
        pass
