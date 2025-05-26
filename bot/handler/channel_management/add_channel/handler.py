from telegram import Update
from telegram.ext import (
    ContextTypes, 
    ConversationHandler, 
    CommandHandler, 
    MessageHandler,
    filters
)
from .validator import validate_channel_link
from ..utils.database import ChannelDatabase
from ..utils.exceptions import InvalidChannelError, NotAdminError

# States
(
    SELECTING_ACTION,
    WAITING_FOR_LINK,
) = range(2)

# Messages
ADD_CHANNEL_MESSAGE = """
👋 برای افزودن کانال جدید:

1️⃣ ابتدا ربات را ادمین کانال کنید
2️⃣ سپس لینک کانال را ارسال کنید

برای لغو عملیات از دستور /cancel استفاده کنید.
"""

async def start_add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the add channel process"""
    await update.message.reply_text(ADD_CHANNEL_MESSAGE)
    return WAITING_FOR_LINK

async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process received channel link"""
    db = ChannelDatabase()
    try:
        channel_id, username = await validate_channel_link(
            update.message.text,
            context.bot
        )
        
        if db.add_channel(channel_id, username, f"@{username}"):
            await update.message.reply_text("✅ کانال با موفقیت اضافه شد!")
        else:
            await update.message.reply_text("⚠️ این کانال قبلاً اضافه شده است.")
            
    except (InvalidChannelError, NotAdminError) as e:
        await update.message.reply_text(f"❌ {str(e)}")
        return WAITING_FOR_LINK
        
    return ConversationHandler.END

async def cancel_operation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation"""
    await update.message.reply_text("❌ عملیات افزودن کانال لغو شد.")
    return ConversationHandler.END

# Update conversation handler
add_channel_handler = ConversationHandler(
    entry_points=[
        CommandHandler('add_channel', start_add_channel)
    ],
    states={
        WAITING_FOR_LINK: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_link)
        ]
    },
    fallbacks=[
        CommandHandler('cancel', cancel_operation)
    ],
    allow_reentry=True
)
