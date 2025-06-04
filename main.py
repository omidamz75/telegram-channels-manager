import asyncio
import os
import json
from pathlib import Path
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram API credentials
API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def get_session_string():
    """Get session string from various sources"""
    # Try getting from env first
    session = os.getenv('TELEGRAM_SESSION_STRING')
    if session:
        return session
        
    # Try getting from config file
    config_file = Path('config/session.json')
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                return data.get('session_string')
        except Exception as e:
            print(f"Error reading config file: {e}")
    
    return None

def save_session_string(session_string: str):
    """Save session string to config file"""
    config_dir = Path('config')
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / 'session.json'
    try:
        data = {'session_string': session_string}
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\nSession string saved to {config_file}")
        print("You can also add it to your .env file as TELEGRAM_SESSION_STRING")
    except Exception as e:
        print(f"Error saving config file: {e}")
        print("\nPlease manually add this session string to your .env file as TELEGRAM_SESSION_STRING:")
        print(session_string)

async def generate_session():
    """Generate a new session string through authentication"""
    print("\nStarting new authentication process...")
    client = TelegramClient(
        StringSession(),
        API_ID,
        API_HASH,
        device_model="Desktop",
        system_version="Windows 10",
        app_version="1.0",
        lang_code="en"
    )
    
    try:
        await client.connect()
        
        print("\nPlease enter your phone number and follow the authentication steps.")
        print("If you have two-factor authentication enabled, you'll need to enter your password.")
        phone = input("\nEnter your phone number (international format, e.g. +989123456789): ")
        
        await client.send_code_request(phone)
        code = input("\nEnter the code you received: ")
        
        try:
            await client.sign_in(phone=phone, code=code)
        except SessionPasswordNeededError:
            print("\nTwo-factor authentication is enabled.")
            password = input("Enter your 2FA password: ")
            await client.sign_in(password=password)
            
        # Get and save the session string
        session_string = client.session.save()
        save_session_string(session_string)
        return session_string
        
    except Exception as e:
        print(f"\nError during authentication: {str(e)}")
        return None
    finally:
        await client.disconnect()

async def main():
    print("Starting bot...")
    
    # Get session string
    session = get_session_string()
    if not session:
        print("No valid session string found.")
        session = await generate_session()
        if not session:
            print("Failed to generate session string. Please try again.")
            return
        print("\nPlease restart the bot to use the new session.")
        return
    
    try:
        # Create client with session string
        client = TelegramClient(
            StringSession(session),
            API_ID,
            API_HASH,
            device_model="Desktop",
            system_version="Windows 10",
            app_version="1.0",
            lang_code="en"
        )
        
        print("Connecting to Telegram...")
        await client.connect()
        
        if not await client.is_user_authorized():
            print("Session is no longer valid. Generating new session...")
            session = await generate_session()
            if not session:
                print("Failed to generate new session. Please try again.")
                return
            print("\nPlease restart the bot to use the new session.")
            return
            
        print("Successfully connected!")
        print("Starting bot operations...")
        
        # Start the bot
        from bot.handler.client import client as bot_client
        await bot_client.start(bot_token=BOT_TOKEN)
        print("Bot is running...")
        print("Press Ctrl+C to stop")
        
        await bot_client.run_until_disconnected()
        
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        if 'client' in locals() and client.is_connected():
            await client.disconnect()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"\nBot stopped due to error: {str(e)}")
