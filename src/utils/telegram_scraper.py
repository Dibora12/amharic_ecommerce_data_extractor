from telethon import TelegramClient
from pathlib import Path
import asyncio
import csv
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('PHONE_NUMBER')
session_file_path = os.getenv('SESSION_FILE_PATH')

# Setup paths
output_path = Path('./data/raw')
output_path.mkdir(parents=True, exist_ok=True)
csv_file = output_path / 'telegram_data_2.csv'

if not session_file_path:
    raise EnvironmentError("SESSION_FILE_PATH not set")

session_path = Path(session_file_path).resolve()
if not session_path.exists() or not session_path.is_file():
    raise FileNotFoundError(f"Invalid session file: {session_path}")

session_name = session_path.stem

# Async scraping function
async def scrape_channel(client, channel_username, writer, batch_size=200):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title
    last_id = None
    total_scraped = 0
    max_limit = 5000

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

        last_id = messages[-1].id

        for message in messages:
            msg_text = (message.message or "").replace('\n', ' ').strip()
            views = message.views or 0
            writer.writerow([
                channel_title,
                channel_username,
                message.id,
                msg_text,
                message.date,
                views,
            ])

        total_scraped += len(messages)
        print(f"Written {len(messages)} (Total: {total_scraped}) from {channel_title}")
        await asyncio.sleep(2)

    print(f"Finished scraping {channel_username}")

# Telegram client setup
client = TelegramClient(str(session_path), api_id, api_hash)

async def main():
    await client.start()
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Channel Title',
            'Channel Username',
            'ID',
            'Message',
            'Date',
            'Views',
        ])

        channels = [
            '@Shageronlinestore',
            '@ethio_brand_collection',
            '@nevacomputer',
            '@meneshayeofficial',
            '@ZemenExpress',
            
        ]

        for channel in channels:
            await scrape_channel(client, channel, writer)
            await asyncio.sleep(3)

with client:
    client.loop.run_until_complete(main())