from telethon import events, Button
from ..client import client

SETTINGS_MESSAGE = """
⚙️ تنظیمات ربات:

لطفا یکی از گزینه‌های زیر را انتخاب کنید:
"""

def get_settings_keyboard():
    return [
        [
            Button.inline("🕒 تنظیمات زمانبندی", b'setting_timing'),
            Button.inline("📊 محدودیت‌ها", b'setting_limits')
        ],
        [
            Button.inline("👥 مدیریت دسترسی", b'setting_access'),
            Button.inline("🔔 اعلان‌ها", b'setting_notifications')
        ],
        [
            Button.inline("🔙 بازگشت به منو", b'back_to_menu')
        ]
    ]

@client.on(events.NewMessage(pattern='/settings'))
async def settings_handler(event):
    """Handle the /settings command"""
    await event.respond(
        SETTINGS_MESSAGE,
        buttons=get_settings_keyboard()
    )

@client.on(events.CallbackQuery)
async def settings_callback_handler(event):
    """Handle settings menu callbacks"""
    if event.data == b'setting_timing':
        await event.edit(
            "⏰ تنظیمات زمانبندی:\n\n"
            "• فاصله بین ارسال‌ها: 15-30 ثانیه\n"
            "• حداکثر پیام در ساعت: 20\n"
            "• حداکثر پیام در روز: 200",
            buttons=get_settings_keyboard()
        )
    # ... سایر callback ها بعداً اضافه می‌شوند
