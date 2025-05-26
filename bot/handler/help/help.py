from telegram import Update
from telegram.ext import ContextTypes

HELP_MESSAGE = """
📚 راهنمای دستورات ربات:

🔹 دستورات عمومی:
/start - شروع کار با ربات
/help - مشاهده این راهنما
/settings - تنظیمات ربات

🔸 مدیریت کانال:
/add_channel - افزودن کانال جدید
/list_channels - مشاهده لیست کانال‌ها
/channel_stats - آمار کانال‌ها

📌 نکته: برای افزودن کانال، ابتدا ربات را ادمین کانال کنید.
"""

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    await update.message.reply_text(HELP_MESSAGE)
