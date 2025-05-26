from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

SETTINGS_MESSAGE = """
⚙️ تنظیمات ربات:

لطفا یکی از گزینه‌های زیر را انتخاب کنید:
"""

def get_settings_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🕒 تنظیمات زمانبندی", callback_data='setting_timing'),
            InlineKeyboardButton("📊 محدودیت‌ها", callback_data='setting_limits')
        ],
        [
            InlineKeyboardButton("👥 مدیریت دسترسی", callback_data='setting_access'),
            InlineKeyboardButton("🔔 اعلان‌ها", callback_data='setting_notifications')
        ],
        [
            InlineKeyboardButton("🔙 بازگشت به منو", callback_data='back_to_menu')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /settings command"""
    await update.message.reply_text(
        SETTINGS_MESSAGE,
        reply_markup=get_settings_keyboard()
    )

async def settings_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle settings menu callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'setting_timing':
        await query.message.edit_text(
            "⏰ تنظیمات زمانبندی:\n\n"
            "• فاصله بین ارسال‌ها: 15-30 ثانیه\n"
            "• حداکثر پیام در ساعت: 20\n"
            "• حداکثر پیام در روز: 200",
            reply_markup=get_settings_keyboard()
        )
    # ... سایر callback ها بعداً اضافه می‌شوند
