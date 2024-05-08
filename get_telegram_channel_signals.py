# This function listens to signals on Telegram crypto channels
# get your api key on my.telegram.org

import asyncio, os
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load & setup credentials
load_dotenv()
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

# List of channels names or IDs
channels = ["channel_name_or_id_1", "channel_name_or_id_2"]

# RegEx function to find #TOKEN and $TOKEN patterns in msgs
def filter_pattern(text):
    matches = re.findall(r'#[A-Z]{3}|\$[A-Z]{3}',text)
    if len(matches) >= 1: return matches[0][1:]

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
        if message_content >= 1:
            print(f"New message from {event.chat_id}: {message_content}")

    print(f"Listening to messages from {len(channels)} channels...")
    await client.run_until_disconnected()

asyncio.run(main())