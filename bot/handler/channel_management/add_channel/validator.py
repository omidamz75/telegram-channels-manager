import re
from ..utils.exceptions import InvalidChannelError, NotAdminError
from telegram import Bot
from typing import Tuple

async def validate_channel_link(link: str, bot: Bot) -> Tuple[str, str]:
    """Validate channel link and check bot permissions"""
    # Clean and validate link format
    if link.startswith('@'):
        username = link[1:]
    else:
        # Check t.me format
        tme_pattern = r'(?:https?://)?t\.me/([a-zA-Z]\w{3,30}[a-zA-Z\d])'
        match = re.match(tme_pattern, link)
        if not match:
            raise InvalidChannelError("لینک کانال نامعتبر است. لطفاً در فرمت @username یا https://t.me/username ارسال کنید.")
        username = match.group(1)

    try:
        # Get channel info and check admin rights
        chat = await bot.get_chat(f"@{username}")
        member = await chat.get_member(bot.id)
        
        # بررسی وضعیت ادمین بودن
        if member.status not in ['administrator', 'creator']:
            raise NotAdminError("ربات در کانال ادمین نیست!")
        
        return str(chat.id), username

    except Exception as e:
        raise InvalidChannelError(f"خطا در بررسی کانال: {str(e)}")
