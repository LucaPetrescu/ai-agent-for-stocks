from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Application, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()


API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /start command"""
    await update.message.reply_text("Welcome to the AI Stock Agent Bot! 🤖📈")


def main():
    """Main function to start the bot"""
    application = Application.builder().token(API_KEY).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    
    # Start the bot
    print("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()