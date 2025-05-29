from telegram import Update
from telegram.ext import (
    ContextTypes, 
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters
)
from .auth_manager import AuthManager

# States
PHONE_NUMBER, VERIFICATION_CODE = range(2)

async def start_auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start authentication process"""
    auth = AuthManager()
    context.user_data['auth'] = auth
    await update.message.reply_text("لطفاً شماره تلفن خود را وارد کنید (مثال: +989123456789)")
    return PHONE_NUMBER

async def phone_number_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle received phone number"""
    auth = context.user_data.get('auth')
    try:
        await auth.request_code(update.message.text)
        await update.message.reply_text("کد تأیید ارسال شد. لطفاً کد را وارد کنید.")
        return VERIFICATION_CODE
    except Exception as e:
        await update.message.reply_text(f"خطا: {str(e)}")
        return ConversationHandler.END

async def code_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle verification code"""
    auth = context.user_data.get('auth')
    try:
        if await auth.sign_in(update.message.text):
            await update.message.reply_text("✅ احراز هویت موفقیت‌آمیز بود.")
        else:
            await update.message.reply_text("❌ کد نامعتبر است.")
    except Exception as e:
        await update.message.reply_text(f"خطا: {str(e)}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel authentication"""
    await update.message.reply_text("عملیات لغو شد.")
    return ConversationHandler.END

auth_handler = ConversationHandler(
    entry_points=[CommandHandler("auth", start_auth)],
    states={
        PHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_number_received)],
        VERIFICATION_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, code_received)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
