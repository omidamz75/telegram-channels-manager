from telethon import events
from telethon.tl.custom import Conversation
from telethon.tl.types import Channel, Chat
from ..client import client
from ..member_extraction import ChannelValidator
from bot.utils.logging import logger
import asyncio
import traceback

HELP_MESSAGE = """
📚 راهنمای دستورات ربات:

🔹 دستورات عمومی:
/start - شروع کار با ربات
/help - مشاهده این راهنما
/settings - تنظیمات ربات

🔸 استخراج اعضا:
/validate_channel - بررسی وضعیت کانال
/extract - شروع استخراج اعضا

🔸 مدیریت کانال:
/add_channel - افزودن کانال جدید
/list_channels - مشاهده لیست کانال‌ها
/channel_stats - آمار کانال‌ها
/export_members - دریافت لیست اعضای کانال 📥

📌 نکات مهم:
• برای استخراج اعضا، ابتدا ربات را ادمین کانال کنید
• احراز هویت مدیر از طریق کنسول انجام می‌شود
• در صورت نیاز به احراز هویت مجدد، با مدیر سیستم تماس بگیرید
"""

VALIDATE_HELP_MESSAGE = """
لطفاً یکی از این موارد را ارسال کنید:

1️⃣ نام کاربری کانال (مثال: @channelname)
2️⃣ آیدی عددی کانال (مثال: -1001234567890)

📌 نکات مهم:
• ربات باید ادمین کانال باشد
• برای پیدا کردن آیدی عددی کانال می‌توانید:
  - یک پیام از کانال را به @getidsbot فوروارد کنید
  - یا در نسخه وب تلگرام، روی پیامی کلیک راست کرده و 'Copy Post Link' را انتخاب کنید

⚠️ توجه: به دلیل محدودیت‌های تلگرام، ربات نمی‌تواند مستقیماً از لینک دعوت استفاده کند.
"""

@client.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    """Handle the /help command"""
    await event.respond(HELP_MESSAGE)

@client.on(events.NewMessage(pattern='/validate_channel'))
async def validate_channel_handler(event):
    """Handle the /validate_channel command"""
    logger.info(f"Validate channel request from user {event.sender_id}")
    
    async with client.conversation(event.chat_id, timeout=60) as conv:
        try:
            # Send initial help message
            await conv.send_message(VALIDATE_HELP_MESSAGE)
            
            # Get the channel ID/username from user
            response = await conv.get_response()
            channel_id = response.text.strip()
            logger.info(f"Received channel identifier: {channel_id}")
            
            # Create validator instance and validate channel
            validator = ChannelValidator(client)
            is_valid, error_msg, entity = await validator.validate_channel(channel_id)
            logger.info(f"Validation result: valid={is_valid}, error={error_msg}")
            
            if is_valid:
                try:
                    # Get channel stats
                    logger.debug("Getting channel stats...")
                    stats = await validator.get_channel_stats(entity)
                    logger.info(f"Channel stats: {stats}")
                    
                    # Format response message
                    response_msg = f"""
✅ کانال با موفقیت تأیید شد

📊 اطلاعات کانال:
• نام: {stats['title']}
• شناسه: {f"@{stats['username']}" if stats['username'] else 'ندارد'}
• نوع: {'کانال' if stats['is_broadcast'] else 'گروه'}
• تعداد اعضا: {stats['member_count']:,} نفر
• وضعیت: {'🔒 خصوصی' if not stats['username'] else '🔓 عمومی'}

✨ دسترسی‌های ربات:
• عضویت: ✅
• مدیریت: ✅
"""
                    await conv.send_message(response_msg)
                    
                except Exception as e:
                    logger.error(f"Error getting channel stats: {str(e)}")
                    await conv.send_message("✅ کانال معتبر است، اما در دریافت آمار آن مشکلی پیش آمد.")
            else:
                await conv.send_message(f"❌ خطا: {error_msg}")
                
        except asyncio.TimeoutError:
            logger.warning(f"Timeout waiting for user {event.sender_id} response")
            await conv.send_message("⚠️ مهلت ارسال به پایان رسید. لطفاً دوباره تلاش کنید.")
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            await conv.send_message("❌ خطای غیرمنتظره رخ داد. لطفاً دوباره تلاش کنید یا با پشتیبانی تماس بگیرید.")
