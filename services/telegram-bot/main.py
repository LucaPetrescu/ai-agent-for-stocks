from telegram import Update
from telegram.ext import CommandHandler, Application, ContextTypes
from dotenv import load_dotenv
from loguru import logger
import os

load_dotenv()

API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to the AI Stock Agent Bot! 🤖📈")


def main():
    application = Application.builder().token(API_KEY).build()
    
    application.add_handler(CommandHandler("start", start))
    
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
