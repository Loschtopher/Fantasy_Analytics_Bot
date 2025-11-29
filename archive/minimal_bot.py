"""
Minimal Working Bot - No scheduler, just commands
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import TELEGRAM_BOT_TOKEN

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store components globally to avoid reinitializing
espn_api = None
state_manager = None
analytics = None
command_handlers = None


def init_components():
    """Initialize components only when needed"""
    global espn_api, state_manager, analytics, command_handlers
    
    if command_handlers is None:
        logger.info("Initializing components...")
        from espn_api import ESPNAPI
        from state_manager import StateManager
        from analytics import FantasyAnalytics
        from commands import CommandHandlers
        
        espn_api = ESPNAPI()
        state_manager = StateManager()
        analytics = FantasyAnalytics()
        command_handlers = CommandHandlers(espn_api, state_manager, analytics)
        logger.info("Components initialized!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    init_components()
    await command_handlers.help_command(update, context)


async def power_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Power rankings"""
    init_components()
    await command_handlers.power_command(update, context)


async def recap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Weekly recap"""
    init_components()
    await command_handlers.recap_command(update, context)


async def luck_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Luck analysis"""
    init_components()
    await command_handlers.luck_command(update, context)


async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """All-play records"""
    init_components()
    await command_handlers.all_command(update, context)


async def boom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Boom/bust analysis"""
    init_components()
    await command_handlers.boom_command(update, context)


async def regret_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start/sit regret"""
    init_components()
    await command_handlers.regret_command(update, context)


async def elo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ELO ratings"""
    init_components()
    await command_handlers.elo_command(update, context)


async def odds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Playoff odds"""
    init_components()
    await command_handlers.odds_command(update, context)


async def sos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Strength of schedule"""
    init_components()
    await command_handlers.sos_command(update, context)


async def heat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Heat map"""
    init_components()
    await command_handlers.heat_command(update, context)


async def rivals_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Rivalry tracker"""
    init_components()
    await command_handlers.rivals_command(update, context)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Exception: {context.error}")


def main():
    """Start the bot"""
    print("="*60)
    print("  Fantasy Football Analytics Bot")
    print("="*60)
    print()
    
    try:
        logger.info("Creating bot application...")
        application = (
            Application.builder()
            .token(TELEGRAM_BOT_TOKEN)
            .job_queue(None)  # Disable job queue to avoid timezone issues
            .build()
        )
        
        logger.info("Registering commands...")
        application.add_handler(CommandHandler("start", help_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("power", power_command))
        application.add_handler(CommandHandler("recap", recap_command))
        application.add_handler(CommandHandler("luck", luck_command))
        application.add_handler(CommandHandler("all", all_command))
        application.add_handler(CommandHandler("boom", boom_command))
        application.add_handler(CommandHandler("regret", regret_command))
        application.add_handler(CommandHandler("elo", elo_command))
        application.add_handler(CommandHandler("odds", odds_command))
        application.add_handler(CommandHandler("sos", sos_command))
        application.add_handler(CommandHandler("heat", heat_command))
        application.add_handler(CommandHandler("rivals", rivals_command))
        
        application.add_error_handler(error_handler)
        
        print()
        print("🎉 BOT STARTED SUCCESSFULLY!")
        print("="*60)
        print()
        print("📱 Your bot is now online!")
        print()
        print("💬 Go to Telegram and try:")
        print("   /help   - Show all commands")
        print("   /power  - Power rankings")
        print("   /recap  - Weekly recap")
        print()
        print("🔄 Bot is listening... (Press Ctrl+C to stop)")
        print("="*60)
        print()
        
        # Start polling
        application.run_polling(
            allowed_updates=["message"],
            drop_pending_updates=True
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

