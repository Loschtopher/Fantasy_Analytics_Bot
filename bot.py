"""
Telegram Fantasy Football Analytics Bot
Main bot file with command handlers
"""
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

from config import TELEGRAM_BOT_TOKEN, ALLOWED_CHAT_IDS, AUTO_POST_DAY, AUTO_POST_HOUR, AUTO_POST_MINUTE
from espn_api import ESPNAPI
from state_manager import StateManager
from analytics import FantasyAnalytics
from commands import CommandHandlers
from scheduler import AutoPoster

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class FantasyBot:
    """Main Fantasy Football Analytics Bot"""
    
    def __init__(self):
        self.espn_api = ESPNAPI()
        self.state_manager = StateManager()
        self.analytics = FantasyAnalytics()
        self.command_handlers = CommandHandlers(self.espn_api, self.state_manager, self.analytics)
        
        # Set up Telegram application
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.auto_poster = AutoPoster(self.application)
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up command handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("power", self.command_handlers.power_command))
        self.application.add_handler(CommandHandler("recap", self.command_handlers.recap_command))
        self.application.add_handler(CommandHandler("luck", self.command_handlers.luck_command))
        self.application.add_handler(CommandHandler("all", self.command_handlers.all_command))
        self.application.add_handler(CommandHandler("boom", self.command_handlers.boom_command))
        self.application.add_handler(CommandHandler("regret", self.command_handlers.regret_command))
        self.application.add_handler(CommandHandler("elo", self.command_handlers.elo_command))
        self.application.add_handler(CommandHandler("odds", self.command_handlers.odds_command))
        self.application.add_handler(CommandHandler("sos", self.command_handlers.sos_command))
        self.application.add_handler(CommandHandler("heat", self.command_handlers.heat_command))
        self.application.add_handler(CommandHandler("rivals", self.command_handlers.rivals_command))
        self.application.add_handler(CommandHandler("help", self.command_handlers.help_command))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Exception while handling an update: {context.error}")
        
        if update and update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, something went wrong. Please try again later."
            )
    
    def _is_allowed_chat(self, chat_id: int) -> bool:
        """Check if chat is allowed to use the bot"""
        if not ALLOWED_CHAT_IDS or ALLOWED_CHAT_IDS == ['']:
            return True  # Allow all chats if not configured
        
        return str(chat_id) in ALLOWED_CHAT_IDS
    
    async def auto_post_power_rankings(self, context: ContextTypes.DEFAULT_TYPE):
        """Auto-post power rankings weekly"""
        try:
            for chat_id in ALLOWED_CHAT_IDS:
                if chat_id:
                    await self.command_handlers.power_command(
                        Update(update_id=0, message=None),
                        ContextTypes.DEFAULT_TYPE.from_update(Update(update_id=0), context.application)
                    )
        except Exception as e:
            logger.error(f"Auto-post failed: {e}")
    
    def setup_auto_posting(self):
        """Set up weekly auto-posting"""
        # Note: Auto-posting will be added in a future update
        # For now, we'll focus on getting the basic bot working
        pass
    
    def start(self):
        """Start the bot"""
        logger.info("Starting Fantasy Football Analytics Bot...")
        
        # Set up auto-posting
        self.setup_auto_posting()
        
        logger.info("Bot started successfully!")
        
        # Start the bot using run_polling (simpler method)
        self.application.run_polling()


def main():
    """Main entry point"""
    bot = FantasyBot()
    bot.start()


if __name__ == "__main__":
    main()
