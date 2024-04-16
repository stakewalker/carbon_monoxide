import os
import json

class Token:
    def __init__(self, symbol):
        token_data = get_token_data(symbol)
        self.symbol = symbol
        self.id = token_data['id']
        self.all_scores = {'sentiment': token_data['sentiment'],
                       'socialmedia': token_data['social'],
                       'news': token_data['news'],
                       'exchange': token_data['exchanges'],
                       'ta_score': token_data['ta']
                       }
    def score():
        pass

    def join_ranking(self, ranking):
        self.ranking = ranking
        ranking.add_token(self)
        
    def update_ranking(self):
        self.ranking.update_token(self)

class Ranking:
    def __init__(self):
        self.filename = 'rank.json'
        # check for previous file
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)
        with open(self.filename, 'r') as f:
            self.rankings = json.load(f)
            
    def update(self):
        # rank by scores
        self.rankings = dict(sorted(self.rankings.items(), key=lambda item: item[1], reverse=True))
        with open(self.filename, 'w') as f:
            json.dump(self.rankings, f)

    def new(self, token, score):
        # add a new token to the ranking
        self.rankings[token] = score
        self.update()

    def remove(self, token):
        # remove token from the list
        if token in self.rankings:
            del self.rankings[token]
            self.update()

