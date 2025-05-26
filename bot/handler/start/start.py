from telegram import Update
from telegram.ext import ContextTypes

WELCOME_MESSAGE = """
🌟 سلام! به ربات مدیریت کانال خوش آمدید

من اینجا هستم تا به شما در مدیریت کانال تلگرامتان کمک کنم.
برای شروع، یکی از دستورات زیر را انتخاب کنید:

/help - راهنمای دستورات
"""

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    await update.message.reply_text(WELCOME_MESSAGE)
