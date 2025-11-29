"""
Simplified bot startup - bypasses scheduler issues
"""
import logging
import asyncio
from telegram.ext import Application, CommandHandler

from config import TELEGRAM_BOT_TOKEN
from espn_api import ESPNAPI
from state_manager import StateManager
from analytics import FantasyAnalytics
from commands import CommandHandlers

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot with minimal setup"""
    logger.info("🚀 Starting Fantasy Football Analytics Bot...")
    
    try:
        # Initialize components
        espn_api = ESPNAPI()
        state_manager = StateManager()
        analytics = FantasyAnalytics()
        command_handlers = CommandHandlers(espn_api, state_manager, analytics)
        
        # Create application
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("power", command_handlers.power_command))
        application.add_handler(CommandHandler("recap", command_handlers.recap_command))
        application.add_handler(CommandHandler("luck", command_handlers.luck_command))
        application.add_handler(CommandHandler("all", command_handlers.all_command))
        application.add_handler(CommandHandler("boom", command_handlers.boom_command))
        application.add_handler(CommandHandler("regret", command_handlers.regret_command))
        application.add_handler(CommandHandler("elo", command_handlers.elo_command))
        application.add_handler(CommandHandler("odds", command_handlers.odds_command))
        application.add_handler(CommandHandler("sos", command_handlers.sos_command))
        application.add_handler(CommandHandler("heat", command_handlers.heat_command))
        application.add_handler(CommandHandler("rivals", command_handlers.rivals_command))
        application.add_handler(CommandHandler("help", command_handlers.help_command))
        application.add_handler(CommandHandler("start", command_handlers.help_command))
        
        logger.info("✅ Bot started successfully!")
        logger.info("📱 Send /help to your bot to see available commands")
        
        # Start polling
        application.run_polling(allowed_updates=["message"])
        
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
        raise


if __name__ == "__main__":
    main()








