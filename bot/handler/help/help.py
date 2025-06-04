from telethon import events
from ..client import client

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
/export_members - دریافت لیست اعضای کانال 📥

📌 نکات مهم:
• برای افزودن کانال، ابتدا ربات را ادمین کانال کنید
• احراز هویت مدیر از طریق کنسول انجام می‌شود
• در صورت نیاز به احراز هویت مجدد، با مدیر سیستم تماس بگیرید
"""

@client.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    """Handle the /help command"""
    await event.respond(HELP_MESSAGE)
