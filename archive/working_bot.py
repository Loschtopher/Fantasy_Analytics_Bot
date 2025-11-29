"""
Working Fantasy Football Bot - Simplified Version
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import TELEGRAM_BOT_TOKEN, ALLOWED_CHAT_IDS
from espn_api import ESPNAPI
from state_manager import StateManager
from analytics import FantasyAnalytics
from commands import CommandHandlers

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors"""
    logger.error(f"Exception: {context.error}")
    if update and hasattr(update, 'effective_chat'):
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Sorry, something went wrong. Please try again."
            )
        except:
            pass


def main():
    """Start the bot"""
    print("="*60)
    print(" Fantasy Football Analytics Bot")
    print("="*60)
    print()
    
    try:
        # Initialize components
        print("🔧 Initializing components...")
        espn_api = ESPNAPI()
        state_manager = StateManager()
        analytics = FantasyAnalytics()
        command_handlers = CommandHandlers(espn_api, state_manager, analytics)
        print("   ✅ Components initialized")
        
        # Create application
        print("🤖 Creating bot application...")
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        print("   ✅ Bot application created")
        
        # Add command handlers
        print("📝 Registering command handlers...")
        handlers = {
            "start": command_handlers.help_command,
            "help": command_handlers.help_command,
            "power": command_handlers.power_command,
            "recap": command_handlers.recap_command,
            "luck": command_handlers.luck_command,
            "all": command_handlers.all_command,
            "boom": command_handlers.boom_command,
            "regret": command_handlers.regret_command,
            "elo": command_handlers.elo_command,
            "odds": command_handlers.odds_command,
            "sos": command_handlers.sos_command,
            "heat": command_handlers.heat_command,
            "rivals": command_handlers.rivals_command,
        }
        
        for command, handler in handlers.items():
            application.add_handler(CommandHandler(command, handler))
        print(f"   ✅ Registered {len(handlers)} commands")
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        print()
        print("="*60)
        print(" 🎉 BOT STARTED SUCCESSFULLY!")
        print("="*60)
        print()
        print("📱 Your bot is now online and ready to use!")
        print()
        print("Available commands:")
        print("  /help   - Show all commands")
        print("  /power  - Power rankings")
        print("  /recap  - Weekly recap")
        print("  /luck   - Luck analysis")
        print("  ... and 9 more!")
        print()
        print("🔄 Bot is now listening for commands...")
        print("   (Press Ctrl+C to stop)")
        print("="*60)
        print()
        
        # Start polling
        application.run_polling(
            allowed_updates=["message"],
            drop_pending_updates=True
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting bot: {e}")
        logger.exception("Bot startup error:")
        raise


if __name__ == "__main__":
    main()
