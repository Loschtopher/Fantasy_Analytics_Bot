"""
Simplified Fantasy Football Bot for Windows compatibility
"""
import asyncio
import logging
import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_CHAT_IDS = os.getenv('ALLOWED_CHAT_IDS', '').split(',')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    message = "Fantasy Football Analytics Bot Commands:\n\n"
    message += "/power - Power Rankings\n"
    message += "/recap - Weekly Recap\n"
    message += "/luck - Luck Analysis\n"
    message += "/all - All-Play Records\n"
    message += "/boom - Boom/Bust Analysis\n"
    message += "/regret - Start/Sit Regret\n"
    message += "/elo - ELO Ratings\n"
    message += "/odds - Playoff Odds\n"
    message += "/sos - Strength of Schedule\n"
    message += "/heat - Heat Map\n"
    message += "/rivals - Rivalry Tracker\n"
    message += "/help - This command list"
    
    await update.message.reply_text(message)

async def power_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /power command"""
    message = "Power Rankings:\n\n"
    message += "Feature coming soon! The full analytics engine is being loaded.\n"
    message += "For now, try /help to see all available commands."
    
    await update.message.reply_text(message)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Exception while handling an update: {context.error}")
    
    if update and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sorry, something went wrong. Please try again later."
        )

def main():
    """Main entry point"""
    print("Starting Fantasy Football Analytics Bot...")
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("power", power_command))
    application.add_handler(CommandHandler("recap", help_command))
    application.add_handler(CommandHandler("luck", help_command))
    application.add_handler(CommandHandler("all", help_command))
    application.add_handler(CommandHandler("boom", help_command))
    application.add_handler(CommandHandler("regret", help_command))
    application.add_handler(CommandHandler("elo", help_command))
    application.add_handler(CommandHandler("odds", help_command))
    application.add_handler(CommandHandler("sos", help_command))
    application.add_handler(CommandHandler("heat", help_command))
    application.add_handler(CommandHandler("rivals", help_command))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    print("Bot started successfully!")
    print("Try /help in your chat to see available commands")
    
    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()









