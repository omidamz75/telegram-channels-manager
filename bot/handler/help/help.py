from telegram import Update
from telegram.ext import ContextTypes

HELP_MESSAGE = """
📚 راهنمای دستورات ربات:

/start - شروع مجدد ربات
/help - مشاهده این راهنما
/add_channel - افزودن کانال جدید
/my_channels - مشاهده لیست کانال‌های من
/backup - دریافت پشتیبان از اطلاعات
/settings - تنظیمات ربات

📌 نکات مهم:
• برای افزودن کانال جدید، باید ربات را ادمین کانال کنید
• حداکثر تعداد کانال قابل مدیریت: 5 کانال
• برای پشتیبان‌گیری از دستور /backup استفاده کنید
"""

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    await update.message.reply_text(HELP_MESSAGE)
