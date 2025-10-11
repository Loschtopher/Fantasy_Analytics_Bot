"""
Configuration settings for Telegram Fantasy Football Analytics Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_CHAT_IDS = os.getenv('ALLOWED_CHAT_IDS', '').split(',')  # Comma-separated chat IDs

# ESPN Fantasy Football Configuration
ESPN_LEAGUE_ID = os.getenv('ESPN_LEAGUE_ID')
ESPN_SWID = os.getenv('ESPN_SWID')
ESPN_S2 = os.getenv('ESPN_S2')

# ESPN API Configuration
ESPN_BASE_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl"
ESPN_SEASON = 2025  # Current fantasy season

# Bot Configuration
AUTO_POST_DAY = 1  # Tuesday (0=Monday, 1=Tuesday, etc.)
AUTO_POST_HOUR = 10  # 10 AM ET
AUTO_POST_MINUTE = 0

# File Paths
STATE_FILE = "state.json"
LOG_FILE = "bot.log"

# Power Rankings Configuration
POWER_RANKINGS_WEIGHTS = {
    'win_percentage': 0.4,
    'recent_form': 0.25,
    'efficiency': 0.2,
    'schedule_strength': 0.15
}

# ELO Configuration
ELO_K_FACTOR = 32
ELO_INITIAL_RATING = 1500
