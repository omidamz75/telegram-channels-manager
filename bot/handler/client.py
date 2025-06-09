from telethon import TelegramClient
import os
from dotenv import load_dotenv
from bot.utils.logging import logger

# Load environment variables
load_dotenv()
logger.debug("Environment variables loaded in client module")

# Get credentials from environment variables
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not all([API_ID, API_HASH, BOT_TOKEN]):
    logger.critical("Missing required environment variables in client module")
else:
    logger.debug("Client credentials loaded successfully")

# Initialize the bot client
try:
    client = TelegramClient('bot_session', API_ID, API_HASH)
    logger.info("Bot client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize bot client: {str(e)}")
    raise 