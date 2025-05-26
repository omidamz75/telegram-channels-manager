import pytest
from telegram import Update
from telegram.ext import ContextTypes
from bot.handler.help.help import help_handler, HELP_MESSAGE
from unittest.mock import AsyncMock
from datetime import datetime

@pytest.mark.asyncio
async def test_help_command():
    # Create mock message
    message = AsyncMock()
    message.reply_text = AsyncMock()
    
    # Create mock update
    update = AsyncMock(spec=Update)
    update.message = message
    
    # Create context
    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    
    # Call handler
    await help_handler(update, context)
    
    # Assert
    message.reply_text.assert_called_once_with(HELP_MESSAGE)
