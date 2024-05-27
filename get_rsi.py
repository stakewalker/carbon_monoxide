import requests

# Get token data and calculate RSI
binance_tokens = [symbol['symbol'][:-4] for symbol in requests.get('https://api.binance.com/api/v3/exchangeInfo').json()['symbols'] if symbol['symbol'].endswith('USDT')]

counter = 0
def get_rsi(symbol):
    closes = [float(entry[4]) for entry in requests.get(f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=14").json()]
    changes = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    up_moves = [change for change in changes if change > 0]
    down_moves = [abs(change) for change in changes if change < 0]
    avg_gain = sum(up_moves) / 14
    avg_loss = sum(down_moves) / 14
    rs = avg_gain / avg_loss
    return int(100 - (100 / (1 + rs)))

# Calculate RSI
for symbol in binance_tokens:
    counter += 1
    print(f"{counter} - RSI for {symbol}: {get_rsi(symbol+"USDT")}")
