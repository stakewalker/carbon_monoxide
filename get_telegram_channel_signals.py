# This function listens to signals on some Telegram channels
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
channels = ['channel_or_id_1', 'channel_or_id_2']

# Create the client and connect
client = TelegramClient('anon', api_id, api_hash)

async def main():
    # Connecting and authorizing
    await client.start(phone_number)
    print("Client Created")
    
    # Listening to messages from channels
    @client.on(events.NewMessage(chats=channels))
    async def handler(event):
        message_content = event.message.message
        print(f"New message from {event.chat_id}: {message_content}")
        # Here you can save the message content to a file or database
        with open('messages.txt', 'a', encoding='utf-8') as f:
            f.write(f"Channel {event.chat_id}: {message_content}\n")

    print(f"Listening to messages from {len(channels)} channels...")
    await client.run_until_disconnected()

asyncio.run(main())
