import pytest
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
import asyncio
from dotenv import load_dotenv
from bot.utils.logging import logger

# Load environment variables
load_dotenv()

# Get test credentials
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

@pytest.fixture
async def bot_client():
    """Create a test bot client"""
    client = TelegramClient(
        StringSession(),
        API_ID,
        API_HASH,
        device_model="Test Device",
        system_version="Test System",
        app_version="1.0 Test",
    )
    
    try:
        await client.start(bot_token=BOT_TOKEN)
        logger.info("Test bot client started")
        yield client
    finally:
        await client.disconnect()
        logger.info("Test bot client disconnected")

@pytest.mark.asyncio
async def test_start_command(bot_client):
    """Test if /start command is registered and responds"""
    try:
        # Get bot info
        me = await bot_client.get_me()
        logger.info(f"Bot username: @{me.username}")
        
        # Register test command handler
        received_command = False
        
        @bot_client.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            nonlocal received_command
            received_command = True
            await event.reply("Bot started successfully!")
        
        # Simulate sending /start command
        await bot_client.send_message(me.username, '/start')
        
        # Wait a bit for command processing
        await asyncio.sleep(2)
        
        # Check if command was received
        assert received_command, "Start command was not received"
        logger.info("Start command test passed")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_command_registration():
    """Test if all commands are properly registered"""
    try:
        from bot.handler.client import client as bot_client
        
        # Get all registered command handlers
        handlers = bot_client.list_event_handlers()
        
        # Check if we have any command handlers
        command_handlers = [h for h in handlers if isinstance(h.event, events.NewMessage)]
        
        assert len(command_handlers) > 0, "No command handlers registered"
        logger.info(f"Found {len(command_handlers)} command handlers")
        
        # Log registered commands for debugging
        for handler in command_handlers:
            if hasattr(handler.event, 'pattern'):
                logger.info(f"Registered command pattern: {handler.event.pattern}")
        
    except Exception as e:
        logger.error(f"Command registration test failed: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_bot_responses():
    """Test if bot responds to basic commands"""
    try:
        from bot.handler.client import client as bot_client
        
        # List of basic commands to test
        test_commands = ['/start', '/help', '/settings']
        
        for command in test_commands:
            # Create a mock event
            event = events.NewMessage(pattern=command)
            
            # Get matching handlers
            matching_handlers = [h for h in bot_client.list_event_handlers() 
                               if isinstance(h.event, events.NewMessage) and 
                               h.event.pattern and command in str(h.event.pattern)]
            
            assert len(matching_handlers) > 0, f"No handler found for {command}"
            logger.info(f"Handler found for {command}")
            
    except Exception as e:
        logger.error(f"Response test failed: {str(e)}")
        raise 