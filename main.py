from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os
from bot.handler.start.start import start_handler
from bot.handler.help.help import help_handler
from bot.handler.settings.settings import settings_handler, settings_callback_handler

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
    
    # Start the bot
    print('Bot is running...')
    print('Press Ctrl+C to stop')
    application.run_polling()

if __name__ == '__main__':
    main()
