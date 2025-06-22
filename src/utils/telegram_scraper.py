from telethon import TelegramClient
from pathlib import Path
import asyncio
import csv
import os
from dotenv import load_dotenv

# Load environment variables once
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('PHONE_NUMBER')
session_file_path = os.getenv('SESSION_FILE_PATH')

output_path = Path('./data/raw')
output_path.mkdir(parents=True, exist_ok=True)  # Create folders if they don't exist
csv_file = output_path / 'telegram_data.csv'


if not session_file_path:
    raise EnvironmentError("SESSION_FILE_PATH not set")

session_path = Path(session_file_path).resolve()

if not session_path.exists():
    raise FileNotFoundError(f"Session file not found: {session_path}")

if not session_path.is_file():
    raise ValueError(f"Session path is not a file: {session_path}")

# Extract session name 
session_name = session_path.stem


# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, batch_size=200):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title
    last_id = None
    total_scraped = 0
    max_limit = 10000

    print(f"Scraping channel: {channel_title} ({channel_username})")

    while total_scraped < max_limit:
        messages = []
        
        if last_id:
            async for msg in client.iter_messages(entity, limit=batch_size, max_id=last_id):
                messages.append(msg)
        else:
            async for msg in client.iter_messages(entity, limit=batch_size):
                messages.append(msg)

        if not messages:
            break

        last_id = messages[-1].id  # Get ID of the last message in the batch
        
        # Process messages
        for message in messages:
            media_path = None 
            writer.writerow([
                channel_title,
                channel_username,
                message.id,
                (message.message or "").replace('\n', ' ').strip(),
                message.date,
                media_path
            ])

        total_scraped += len(messages)
        print(f"Written {len(messages)} messages (Total: {total_scraped}) from {channel_title}")

        await asyncio.sleep(2)  # Delay between batches

    print(f"Finished scraping {channel_username}")

# Initialize Telegram client
client = TelegramClient(str(session_path), api_id, api_hash)

async def main():
    await client.start()




    # Open CSV for writing
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])

        # List of channels to scrape
        channels = [
            '@channelusername',
            '.....'
        ]

        for channel in channels:
            await scrape_channel(client, channel, writer )
            await asyncio.sleep(3)  # Delay between channels

with client:
    client.loop.run_until_complete(main())