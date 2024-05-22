import asyncio, os, re, csv
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
recipient = os.getenv('MSG_RECEIVER')  # Who's gonna receive the message?

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
def append_to_csv(timestamp, channel, token):
    with open('tokens.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, channel, token, "[]"])

# Funtion to get TOKEN price from CoinGecko
def get_price(token_id):
    return requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd").json().get(token_id, {}).get('usd', None)

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
        try:
            for token in message_content:
                if not token_exists(token):
                    token_price_now = get_price(token)
                    append_to_csv(
                        int(datetime.now(timezone.utc).timestamp()),  # Time at the moment
                        event.chat.username,  # Channel name
                        token,  # Token ID
                        [token_price_now]
                        )
                    final_msg = f"New message from {event.chat.username}: {token} @ ${token_price_now}"
                    await client.send_message(recipient, token)  
                    print(final_msg)
        except Exception as e:
            print(f"Error fetching new token from {event.chat.username}")

    print(f"Listening to messages from {len(channels)} channels...")
    await client.run_until_disconnected()

asyncio.run(main())
