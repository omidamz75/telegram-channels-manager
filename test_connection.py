import pytest
from telethon import TelegramClient
from bot.handler.channel_management.utils.database import ChannelDatabase
from dotenv import load_dotenv
import os
import sqlite3

# Load environment variables
load_dotenv()

# Telegram credentials
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

@pytest.mark.asyncio
async def test_telegram_connection():
    """Test Telegram API connection"""
    try:
        client = TelegramClient('bot_session', API_ID, API_HASH)
        await client.connect()
        assert await client.is_user_authorized() == False
        await client.disconnect()
    except Exception as e:
        pytest.fail(f"Telegram connection failed: {str(e)}")

def test_bot_token():
    """Test bot token validity"""
    assert BOT_TOKEN is not None
    assert len(BOT_TOKEN.split(':')) == 2
    assert BOT_TOKEN.split(':')[0].isdigit()

def test_database_connection():
    """Test database connection and initialization"""
    try:
        db = ChannelDatabase(":memory:")  # Use in-memory database for testing
        assert isinstance(db, ChannelDatabase)
        
        # Test table creation
        with sqlite3.connect(":memory:") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='channels'")
            assert cursor.fetchone() is not None
            
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")
