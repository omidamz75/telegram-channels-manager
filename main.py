from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os
from bot.handler.start.start import start_handler
from bot.handler.help.help import help_handler
from bot.handler.settings.settings import settings_handler, settings_callback_handler
from bot.handler.channel_management.add_channel import add_channel_handler
from bot.handler.channel_management.member_export.handler import export_members_handler
# from bot.handler.authentication.handler import auth_handler  # Import the new handler

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def main():
    # Initialize bot
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(CommandHandler('help', help_handler))
    application.add_handler(CommandHandler('settings', settings_handler))
    application.add_handler(CallbackQueryHandler(settings_callback_handler))
    application.add_handler(add_channel_handler)
    application.add_handler(export_members_handler)  # Add this line
    # application.add_handler(auth_handler)  # Add the new handler here
    
    # Start the bot
    print('Bot is running...')
    print('Press Ctrl+C to stop')
    application.run_polling()

if __name__ == '__main__':
    main()
