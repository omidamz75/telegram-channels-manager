import asyncio
import os
import json
from pathlib import Path
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import BotCommand
from telethon.tl.functions.bots import SetBotCommandsRequest
from telethon.tl.types import BotCommandScopeDefault
from dotenv import load_dotenv
from bot.utils.logging import logger

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

# Telegram API credentials
API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not all([API_ID, API_HASH, BOT_TOKEN]):
    logger.critical("Missing required environment variables (API_ID, API_HASH, or BOT_TOKEN)")
else:
    logger.debug("API credentials loaded successfully")

def get_session_string():
    """Get session string from various sources"""
    logger.debug("Attempting to get session string")
    # Try getting from env first
    session = os.getenv('TELEGRAM_SESSION_STRING')
    if session:
        logger.info("Session string found in environment variables")
        return session
        
    # Try getting from config file
    config_file = Path('config/session.json')
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                session = data.get('session_string')
                if session:
                    logger.info("Session string loaded from config file")
                    return session
                logger.warning("Config file exists but no session string found")
        except Exception as e:
            logger.error(f"Error reading config file: {e}")
    
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
    logger.info("Starting bot...")
    
    # Get session string
    session = get_session_string()
    if not session:
        logger.warning("No valid session string found")
        session = await generate_session()
        if not session:
            logger.error("Failed to generate session string")
            return
        logger.info("New session generated, restart required")
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
        
        logger.info("Connecting to Telegram...")
        await client.connect()
        
        if not await client.is_user_authorized():
            logger.error("Session is no longer valid")
            session = await generate_session()
            if not session:
                logger.error("Failed to generate new session")
                return
            logger.info("New session generated, restart required")
            return
            
        logger.info("Successfully connected!")
        
        # Import and initialize command handlers
        try:
            import bot.handler
            from bot.handler import AVAILABLE_COMMANDS
            logger.info("Command handlers loaded successfully")
            
            # Start the bot
            from bot.handler.client import client as bot_client
            await bot_client.start(bot_token=BOT_TOKEN)
            
            # Set bot commands
            await bot_client(SetBotCommandsRequest(
                scope=BotCommandScopeDefault(),
                lang_code="fa",
                commands=[
                    BotCommand(command=cmd.split(' - ')[0][1:], description=cmd.split(' - ')[1])
                    for cmd in AVAILABLE_COMMANDS
                ]
            ))
            logger.info("Bot commands registered with Telegram")
            
            logger.info("Bot is running...")
            print("Bot is running...")
            print("Press Ctrl+C to stop")
            
            await bot_client.run_until_disconnected()
            
        except Exception as e:
            logger.error(f"Error initializing handlers: {str(e)}")
            raise
            
    except Exception as e:
        logger.error(f"Bot error: {str(e)}")
    finally:
        if 'client' in locals() and client.is_connected():
            await client.disconnect()
            logger.info("Bot disconnected")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"\nBot stopped due to error: {str(e)}")
