import pytest
from telegram import Update
from telegram.ext import ContextTypes
from bot.handler.help.help import help_handler, HELP_MESSAGE

@pytest.mark.asyncio
async def test_help_command():
    # Mock objects
    update = Update.de_json({
        "message": {
            "message_id": 1,
            "text": "/help",
            "chat": {"id": 123, "type": "private"}
        }
    }, None)
    
    context = ContextTypes.DEFAULT_TYPE()
    
    # Test help handler
    await help_handler(update, context)
    
    # Verify that reply_text was called with HELP_MESSAGE
    assert update.message.reply_text.call_args[0][0] == HELP_MESSAGE
