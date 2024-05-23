import asyncio, os, re, csv, requests
from datetime import datetime, timezone
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load & setup credentials
load_dotenv()
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
# List of channels names or IDs (CHANNEL_LIST="1,2,3")
channels = os.getenv('CHANNEL_LIST').split(",")
recipient = os.getenv('MSG_RECEIVER')  # Who's going to receive the message?

# RegEx function to find #TOKEN and $TOKEN patterns in msgs
def filter_pattern(text):
    matches = re.findall(r'#[A-Z]{2,}|\$[A-Z]{2,}', text)
    return [match[1:].upper() for match in matches] if matches else []

# Check if token exists in CSV
def token_exists(token):
    if not os.path.exists('tokens.csv'):
        return False
    with open('tokens.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[2] == token:
                return True
    return False

# Append token to CSV
def append_to_csv(timestamp, channel, token, item_list):
    with open('tokens.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, channel, token, item_list])

# Function to get TOKEN price from Binance Spot
binance_tokens = [symbol['symbol'][:-4] for symbol in requests.get('https://api.binance.com/api/v3/exchangeInfo').json()['symbols'] if symbol['symbol'].endswith('USDT')]
def get_price(token):
    return float(requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={token.upper()}USDT').json()['price'])

# Create the client and connect
client = TelegramClient('anon', api_id, api_hash)

async def main():
    # Connecting and authorizing
    await client.start(phone_number)
    print("Client Started...")
    
    # Listening to messages from channels
    @client.on(events.NewMessage(chats=channels))
    async def handler(event):
        message_content = filter_pattern(event.message.message)
        #try:
        for token in message_content:
            if not token_exists(token):
                if token in binance_tokens:
                    token_price_now = get_price(token)
                    channel_name = event.chat.username
                    final_msg = f"New message from {channel_name}: {token} @ ${token_price_now}"
                    append_to_csv(
                        int(datetime.now(timezone.utc).timestamp()),  # Time at the moment
                        channel_name,  # Channel name
                        token,  # Token ID
                        [token_price_now]
                        )
                    await client.send_message(final_msg)  
                    print(final_msg)
            #except Exception as e:
        #    print(f"Error fetching new token from {channel_name}")

    print(f"Listening to messages from {len(channels)} channels...")
    await client.run_until_disconnected()

asyncio.run(main())
