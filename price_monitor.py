import csv, os, ast, re
import requests
import asyncio
from telethon import TelegramClient, events, Button
from dotenv import load_dotenv

# Load & setup credentials
load_dotenv()
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

# Initialize Telegram client
client = TelegramClient('anon', api_id, api_hash)

# Function to get token price from CoinGecko
def get_token_price(token_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data.get(token_id, {}).get('usd', None)

# Read and update tokens in the CSV file
def update_prices_and_check_variations():
    updated_rows = []
    significant_changes = []

    if os.path.exists('tokens.csv'):
        with open('tokens.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                timestamp, channel, token, price_list_str = row
                price_list = ast.literal_eval(price_list_str)
                current_price = get_token_price(token)
                
                if current_price is not None:
                    price_list.append(current_price)
                    if len(price_list) > 1:
                        first_price = price_list[0]
                        last_price = price_list[-1]
                        change = ((last_price - first_price) / first_price) * 100
                        if abs(change) > 1:
                            significant_changes.append((timestamp, channel, token, change))
                
                updated_rows.append([timestamp, channel, token, str(price_list)])

        # Rewrite the CSV file with updated prices
        with open('tokens.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(updated_rows)
    
    return significant_changes

# Send Telegram message with significant changes and buttons to dismiss tokens
async def send_alerts():
    significant_changes = update_prices_and_check_variations()
    for timestamp, channel, token, change in significant_changes:
        message = (f"Token: {token}\n"
                   f"Channel: {channel}\n"
                   f"Time Added: {timestamp}\n"
                   f"Price Change: {change:.2f}%")
        await client.send_message(
            'channel_or_name',  # Replace with the correct recipient
            message,
            buttons=[
                Button.inline("Dismiss", data=f"dismiss_{token}")
            ]
        )

# Handle button clicks to dismiss tokens
@client.on(events.CallbackQuery(data=re.compile(b'dismiss_(.*)')))
async def dismiss_token(event):
    token_to_dismiss = event.data.decode().split('_')[1]

    # Read the current CSV file and filter out the dismissed token
    updated_rows = []
    if os.path.exists('tokens.csv'):
        with open('tokens.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[2] != token_to_dismiss:
                    updated_rows.append(row)
    
    # Rewrite the CSV file without the dismissed token
    with open('tokens.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(updated_rows)
    
    await event.answer(f"Token {token_to_dismiss} dismissed", alert=True)

# Function to run the price monitor
async def price_monitor():
    while True:
        await send_alerts()
        await asyncio.sleep(300)  # Check every 5 minutes

# Run the price monitor
async def main():
    await client.start(phone_number)
    print("Price Monitor Started...")
    await price_monitor()

asyncio.run(main())
