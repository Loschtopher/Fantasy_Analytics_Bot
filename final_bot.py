"""
Final Fantasy Football Bot - Python 3.13 Compatible
"""
import logging
import os
from dotenv import load_dotenv

from telegram import Update, Bot
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

def _is_allowed_chat(chat_id: int) -> bool:
    """Check if chat is allowed to use the bot"""
    if not ALLOWED_CHAT_IDS or ALLOWED_CHAT_IDS == ['']:
        return True  # Allow all chats if not configured
    
    return str(chat_id) in ALLOWED_CHAT_IDS

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    if not _is_allowed_chat(update.effective_chat.id):
        return
    
    message = "Fantasy Football Analytics Bot Commands:\n\n"
    message += "/power - Power Rankings with movement tracking\n"
    message += "/recap - Weekly Recap with highlights\n"
    message += "/luck - Luck Analysis (Pythagorean expectation)\n"
    message += "/all - All-Play Records\n"
    message += "/boom - Boom/Bust Analysis\n"
    message += "/regret - Start/Sit Regret Analysis\n"
    message += "/elo - ELO Ratings\n"
    message += "/odds - Playoff Odds (Monte Carlo)\n"
    message += "/sos - Strength of Schedule\n"
    message += "/heat - Heat Map (Z-scores)\n"
    message += "/rivals - Rivalry Tracker\n"
    message += "/help - This command list\n\n"
    message += "Bot is online and ready!"
    
    await update.message.reply_text(message)

async def power_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /power command"""
    if not _is_allowed_chat(update.effective_chat.id):
        return
    
    message = "Power Rankings:\n\n"
    message += "1. Team Alpha (ALP) ▲\n"
    message += "   Record: 8-2-0 (0.800) | PF: 1250.5 | PA: 1100.2\n"
    message += "   Streak: W3 | Score: 0.847\n\n"
    message += "2. Team Beta (BET) ▼\n"
    message += "   Record: 7-3-0 (0.700) | PF: 1200.0 | PA: 1150.0\n"
    message += "   Streak: L1 | Score: 0.723\n\n"
    message += "*Full ESPN integration coming soon!*"
    
    await update.message.reply_text(message)

async def boom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /boom command"""
    if not _is_allowed_chat(update.effective_chat.id):
        return
    
    message = "Boom/Bust Analysis:\n\n"
    message += "Team Alpha (ALP)\n"
    message += "Ceiling (P80): 145.2 | Floor (P20): 98.7\n"
    message += "Spread: 46.5 | Consistency: 0.023\n\n"
    message += "Team Beta (BET)\n"
    message += "Ceiling (P80): 142.1 | Floor (P20): 95.3\n"
    message += "Spread: 46.8 | Consistency: 0.021\n\n"
    message += "*Live data integration coming soon!*"
    
    await update.message.reply_text(message)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Exception while handling an update: {context.error}")

def main():
    """Main entry point"""
    print("Starting Fantasy Football Analytics Bot...")
    
    if not TELEGRAM_BOT_TOKEN:
        print("ERROR: No bot token found. Check your .env file.")
        return
    
    # Create application with workaround for Python 3.13
    try:
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    except AttributeError as e:
        print(f"Compatibility issue detected: {e}")
        print("Using alternative startup method...")
        
        # Create bot directly
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Create application without builder
        application = Application(bot=bot)
    
    # Add handlers
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("power", power_command))
    application.add_handler(CommandHandler("boom", boom_command))
    application.add_handler(CommandHandler("recap", help_command))
    application.add_handler(CommandHandler("luck", help_command))
    application.add_handler(CommandHandler("all", help_command))
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
    print("Bot is connected to chat ID:", ALLOWED_CHAT_IDS)
    
    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()



