from telethon import TelegramClient
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()

# Get credentials from environment variables
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

print("Credentials loaded:")
print(f"API_ID: {API_ID}")
print(f"API_HASH: {API_HASH}")
print(f"BOT_TOKEN: {BOT_TOKEN}")

async def test_connection():
    try:
        print("\nTrying to connect to Telegram...")
        client = TelegramClient('bot_session', API_ID, API_HASH)
        
        print("Starting client...")
        await client.start(bot_token=BOT_TOKEN)
        
        print("\n✅ Connection successful!")
        print("Bot information:")
        me = await client.get_me()
        print(f"Username: @{me.username}")
        print(f"Bot ID: {me.id}")
        print(f"Name: {me.first_name}")
        
        await client.disconnect()
        print("\nConnection closed properly")
        
    except Exception as e:
        print("\n❌ Error occurred:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")

if __name__ == '__main__':
    print("Starting connection test...\n")
    asyncio.run(test_connection())
