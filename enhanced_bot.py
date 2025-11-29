"""
Enhanced Fantasy Football Bot with Improvements
- Better error handling
- Rate limiting
- Health monitoring
- Status command
"""
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from bot_enhancements import RateLimiter, BotHealth, safe_command

# Load environment
load_dotenv()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize once
espn_api = None
state_manager = None
analytics = None
command_handlers = None
user_mapping = None
user_commands = None
team_picker = None

# Bot enhancements
rate_limiter = RateLimiter(calls=10, period=60)  # 10 commands per minute
bot_health = BotHealth()


def init():
    """Initialize components"""
    global espn_api, state_manager, analytics, command_handlers, user_mapping, user_commands, team_picker
    
    if command_handlers is None:
        from espn_api import ESPNAPI
        from state_manager import StateManager
        from analytics import FantasyAnalytics
        from commands import CommandHandlers
        from user_mapping import UserMapping
        from user_commands import UserCommands
        from simple_team_picker import TeamPicker
        
        espn_api = ESPNAPI()
        state_manager = StateManager()
        analytics = FantasyAnalytics()
        user_mapping = UserMapping()
        command_handlers = CommandHandlers(espn_api, state_manager, analytics)
        user_commands = UserCommands(espn_api, user_mapping)
        team_picker = TeamPicker(espn_api, user_mapping)
        
        # Attach health tracker to handlers
        command_handlers.health = bot_health
        user_commands.health = bot_health


async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot status and health"""
    try:
        status = bot_health.get_status()
        
        message = "🤖 **BOT STATUS** 🤖\n\n"
        message += f"⏱️ **Uptime:** {status['uptime']}\n"
        message += f"📊 **Commands Processed:** {status['commands_processed']}\n"
        message += f"❌ **Errors:** {status['errors']}\n"
        
        if status['last_error']:
            message += f"\n⚠️ **Last Error:**\n`{status['last_error'][:100]}...`\n"
        
        message += "\n✅ Bot is running normally!"
        
        await update.message.reply_text(message, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Error getting status: {str(e)}")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.help_command(update, context)


async def power_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.power_command(update, context)


async def recap_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.recap_command(update, context)


async def season_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.season_command(update, context)


async def parlay_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.parlay_command(update, context)


async def yolo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.yolo_command(update, context)


async def luck_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.luck_command(update, context)


async def all_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.all_command(update, context)


async def boom_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.boom_command(update, context)


async def regret_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.regret_command(update, context)


async def waiver_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.waiver_command(update, context)


async def odds_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.odds_command(update, context)


async def sos_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.sos_command(update, context)


async def heat_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.heat_command(update, context)


async def rivals_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await command_handlers.rivals_command(update, context)


async def whoami_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await user_commands.whoami_command(update, context)


async def users_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await user_commands.users_command(update, context)


async def teams_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await user_commands.teams_command(update, context)


async def linkuser_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await user_commands.linkuser_command(update, context)


async def myteam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await user_commands.myteam_command(update, context)


async def unlink_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await user_commands.unlink_command(update, context)


async def pickteam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init()
    await team_picker.pickteam_command(update, context)


def main():
    """Start bot"""
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Set UTF-8 encoding for console on Windows
    import sys
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass  # If reconfigure fails, continue without emojis
    
    print("="*60)
    print("  Fantasy Football Analytics Bot - Enhanced")
    print("="*60)
    print()
    print("Starting...")
    
    # Build application WITHOUT job queue (to avoid timezone errors)
    app = Application.builder().token(TOKEN).job_queue(None).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", help_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("power", power_cmd))
    app.add_handler(CommandHandler("recap", recap_cmd))
    app.add_handler(CommandHandler("season", season_cmd))
    app.add_handler(CommandHandler("parlay", parlay_cmd))
    app.add_handler(CommandHandler("yolo", yolo_cmd))
    app.add_handler(CommandHandler("luck", luck_cmd))
    app.add_handler(CommandHandler("all", all_cmd))
    app.add_handler(CommandHandler("boom", boom_cmd))
    app.add_handler(CommandHandler("regret", regret_cmd))
    app.add_handler(CommandHandler("waiver", waiver_cmd))
    app.add_handler(CommandHandler("odds", odds_cmd))
    app.add_handler(CommandHandler("sos", sos_cmd))
    app.add_handler(CommandHandler("heat", heat_cmd))
    app.add_handler(CommandHandler("rivals", rivals_cmd))
    
    # User-team linking commands (EASY WAY - with buttons!)
    app.add_handler(CommandHandler("pickteam", pickteam_cmd))
    app.add_handler(CommandHandler("myteam", myteam_cmd))
    app.add_handler(CommandHandler("whoami", whoami_cmd))
    
    # Admin commands
    app.add_handler(CommandHandler("users", users_cmd))
    app.add_handler(CommandHandler("teams", teams_cmd))
    app.add_handler(CommandHandler("linkuser", linkuser_cmd))
    app.add_handler(CommandHandler("unlink", unlink_cmd))
    
    # Button callback handler (for team picker)
    init()  # Make sure team_picker is initialized
    app.add_handler(team_picker.get_callback_handler())
    
    print()
    print("*** BOT IS ONLINE! ***")
    print("="*60)
    print()
    print("Go to Telegram and try these commands:")
    print("   /pickteam - PICK YOUR TEAM (with buttons!)")
    print("   /myteam   - See your team stats")
    print("   /power    - Power rankings")
    print("   /status   - Bot health check")
    print("   /help     - List all commands")
    print()
    print("Bot running... (Ctrl+C to stop)")
    print("="*60)
    print()
    
    # Start (allow both messages and callback queries for buttons)
    app.run_polling(allowed_updates=["message", "callback_query"], drop_pending_updates=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot stopped")
    except Exception as e:
        print(f"\nError: {e}")
        logger.exception("Startup error")

