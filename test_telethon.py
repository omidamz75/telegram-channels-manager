from telethon import TelegramClient
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

async def main():
    # Load credentials
    api_id = int(os.getenv('TELEGRAM_API_ID'))
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = input("Please enter your phone number: ")
    
    print("Creating Telegram client...")
    client = TelegramClient('test_session', api_id, api_hash)
    
    print("Connecting to Telegram...")
    await client.connect()
    
    print("Checking connection...")
    if client.is_connected():  # Remove await here
        print("Successfully connected!")
        
        if not await client.is_user_authorized():
            print("Requesting verification code...")
            await client.send_code_request(phone)
            code = input("Enter the code you received: ")
            await client.sign_in(phone, code)
            print("Successfully logged in!")
        else:
            print("Already authorized!")
            
        print("Disconnecting...")
        await client.disconnect()
    else:
        print("Failed to connect!")

if __name__ == '__main__':
    asyncio.run(main())
