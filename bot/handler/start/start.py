from telethon import events
from ..client import client

WELCOME_MESSAGE = """
🌟 سلام! به ربات مدیریت کانال خوش آمدید

من اینجا هستم تا به شما در مدیریت کانال تلگرامتان کمک کنم.
برای شروع، یکی از دستورات زیر را انتخاب کنید:

/help - راهنمای دستورات
"""

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    """Handle the /start command"""
    await event.respond(WELCOME_MESSAGE)
