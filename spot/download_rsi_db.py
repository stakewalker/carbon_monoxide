import requests
import pandas as pd
import time
import csv

# Fetch all Binance tokens that end with 'USDT'
binance_tokens = [symbol['symbol'][:-4] for symbol in requests.get('https://api.binance.com/api/v3/exchangeInfo').json()['symbols'] if symbol['symbol'].endswith('USDT')]

def get_token_info(symbol):
    return requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol.upper()}").json()

def get_rsi(symbol):
    closes = [float(entry[4]) for entry in requests.get(f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=14").json()]
    changes = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    up_moves = [change for change in changes if change > 0]
    down_moves = [abs(change) for change in changes if change < 0]
    avg_gain = sum(up_moves) / 14
    avg_loss = sum(down_moves) / 14
    rs = avg_gain / avg_loss
    return int(100 - (100 / (1 + rs)))

def append_to_csv(token_info, max_token_entries=10):
    try:
        # Read the existing data
        df = pd.read_csv("token_db.csv")
    except FileNotFoundError:
        # Initialize the DataFrame with the correct columns if the file does not exist
        columns = ['symbol', 'priceChange', 'priceChangePercent', 'weightedAvgPrice', 'prevClosePrice',
                   'lastPrice', 'lastQty', 'bidPrice', 'bidQty', 'askPrice', 'askQty', 'openPrice',
                   'highPrice', 'lowPrice', 'volume', 'quoteVolume', 'openTime', 'closeTime', 'firstId',
                   'lastId', 'count', 'rsi']
        df = pd.DataFrame(columns=columns)

    # Count the number of entries for each token
    token_counts = df['symbol'].value_counts().to_dict()

    token = token_info['symbol']
    if token in token_counts and token_counts[token] >= max_token_entries:
        # Remove the oldest entry for the token
        oldest_index = df[df['symbol'] == token].index[0]
        df = df.drop(oldest_index)

    # Add the new entry
    new_entry = pd.DataFrame([[
        token_info.get('symbol', ''),
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
        token_info.get('count', ''),
        get_rsi(token_info['symbol'])
    ]], columns=df.columns)

    df = pd.concat([df, new_entry], ignore_index=True)

    # Save the updated DataFrame back to the CSV
    df.to_csv("token_db.csv", index=False)

max_token_entries = 10

while True:
    counter = 0
    for token in binance_tokens:
        token_info = get_token_info(token+'USDT')
        if token_info['priceChangePercent'] == '0.000':
            continue  # Ignore dummy tokens
        else:
            append_to_csv(token_info, max_token_entries)
            counter += 1
            print(f"{counter}: {token_info['symbol']}")
    #time.sleep(300)  # Wait for 5 minutes before the next update
