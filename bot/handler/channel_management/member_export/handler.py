from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters
)
from telethon import TelegramClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# States
SELECTING_CHANNEL = 1

# Messages
EXPORT_START_MESSAGE = """
📥 استخراج لیست اعضای کانال

لطفا یکی از روش‌های زیر را انجام دهید:
1. آیدی عددی کانال را ارسال کنید
2. لینک کانال را به صورت @username ارسال کنید

برای لغو عملیات از دستور /cancel استفاده کنید.
"""

async def start_export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the export process"""
    await update.message.reply_text(EXPORT_START_MESSAGE)
    return SELECTING_CHANNEL

async def cancel_export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the export process"""
    await update.message.reply_text("❌ عملیات استخراج لیست اعضا لغو شد.")
    return ConversationHandler.END

export_members_handler = ConversationHandler(
    entry_points=[CommandHandler('export_members', start_export)],
    states={
        SELECTING_CHANNEL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, cancel_export)
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel_export)]
)
