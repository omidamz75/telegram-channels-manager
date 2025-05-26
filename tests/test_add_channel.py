import pytest
from telegram import Update
from telegram.ext import ContextTypes
from unittest.mock import AsyncMock
from bot.handler.channel_management.add_channel.handler import (
    start_add_channel,
    cancel_operation,
    receive_link,
    ADD_CHANNEL_MESSAGE
)

@pytest.fixture
def mock_update():
    message = AsyncMock()
    message.reply_text = AsyncMock()
    
    update = AsyncMock(spec=Update)
    update.message = message
    return update

@pytest.fixture
def mock_context():
    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    return context

@pytest.mark.asyncio
async def test_start_add_channel(mock_update, mock_context):
    """Test starting add channel process"""
    result = await start_add_channel(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_called_once_with(ADD_CHANNEL_MESSAGE)
    assert result == 1  # WAITING_FOR_LINK state

@pytest.mark.asyncio
async def test_cancel_operation(mock_update, mock_context):
    """Test cancel command"""
    result = await cancel_operation(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_called_once()
    assert "لغو شد" in mock_update.message.reply_text.call_args[0][0]
    assert result == -1  # ConversationHandler.END
