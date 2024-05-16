# Optimized for Binance Spot

import requests

binance_tokens = [symbol['symbol'][:-4] for symbol in requests.get('https://api.binance.com/api/v3/exchangeInfo').json()['symbols'] if symbol['symbol'].endswith('USDT')]
def spot_price(token):
    if token in binance_tokens:
        return float(requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={token.upper()}USDT').json()['price'])
