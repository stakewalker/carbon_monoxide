import requests
import csv

binance_tokens = [symbol['symbol'][:-4] for symbol in requests.get('https://api.binance.com/api/v3/exchangeInfo').json()['symbols'] if symbol['symbol'].endswith('USDT')]

def get_token_info(symbol):
    return requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol.upper()}").json()


def append_to_csv(token_info):
    with open("token_db.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([token_info.get('symbol', ''),
                         token_info.get('priceChange', ''),
                         token_info.get('priceChangePercent', ''),
                         token_info.get('weightedAvgPrice', ''),
                         token_info.get('prevClosePrice', ''),
                         token_info.get('lastPrice', ''),
                         token_info.get('lastQty', ''),
                         token_info.get('bidPrice', ''),
                         token_info.get('bidQty', ''),
                         token_info.get('askPrice', ''),
                         token_info.get('askQty', ''),
                         token_info.get('openPrice', ''),
                         token_info.get('highPrice', ''),
                         token_info.get('lowPrice', ''),
                         token_info.get('volume', ''),
                         token_info.get('quoteVolume', ''),
                         token_info.get('openTime', ''),
                         token_info.get('closeTime', ''),
                         token_info.get('firstId', ''),
                         token_info.get('lastId', ''),
                         token_info.get('count', '')])

counter = 0

for i in binance_tokens:
    token_info = get_token_info(i+'USDT')
    if token_info:
        append_to_csv(token_info)
        counter += 1
        print(f"{counter}: {token_info['symbol']}")
