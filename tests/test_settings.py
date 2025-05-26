import pytest
from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from bot.handler.settings.settings import settings_handler, settings_callback_handler
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_settings_command():
    # Create mock message
    message = AsyncMock()
    message.reply_text = AsyncMock()
    
    # Create mock update
    update = AsyncMock(spec=Update)
    update.message = message
    
    # Create context
    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    
    # Call handler
    await settings_handler(update, context)
    
    # Assert message was sent with keyboard
    message.reply_text.assert_called_once()

@pytest.mark.asyncio
async def test_settings_callback():
    # Create mock callback query
    query = AsyncMock(spec=CallbackQuery)
    query.data = 'setting_timing'
    query.answer = AsyncMock()
    query.message = AsyncMock()
    
    # Create mock update
    update = AsyncMock(spec=Update)
    update.callback_query = query
    
    # Create context
    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    
    # Call handler
    await settings_callback_handler(update, context)
    
    # Assert
    query.answer.assert_called_once()
