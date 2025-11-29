"""
Bot Enhancements - Additional features and utilities
"""
import time
from functools import wraps
from typing import Dict, Callable
from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter to prevent command spam"""
    
    def __init__(self, calls: int = 5, period: int = 60):
        """
        Args:
            calls: Number of calls allowed
            period: Time period in seconds
        """
        self.calls = calls
        self.period = period
        self.timestamps: Dict[int, list] = {}
    
    def is_allowed(self, user_id: int) -> bool:
        """Check if user is allowed to make a call"""
        now = time.time()
        
        if user_id not in self.timestamps:
            self.timestamps[user_id] = []
        
        # Remove old timestamps
        self.timestamps[user_id] = [
            ts for ts in self.timestamps[user_id]
            if now - ts < self.period
        ]
        
        # Check if under limit
        if len(self.timestamps[user_id]) < self.calls:
            self.timestamps[user_id].append(now)
            return True
        
        return False
    
    def get_wait_time(self, user_id: int) -> int:
        """Get seconds until user can make another call"""
        if user_id not in self.timestamps or not self.timestamps[user_id]:
            return 0
        
        oldest = min(self.timestamps[user_id])
        wait = self.period - (time.time() - oldest)
        return max(0, int(wait))


def rate_limit(limiter: RateLimiter):
    """Decorator to rate limit command handlers"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_id = update.effective_user.id
            
            if not limiter.is_allowed(user_id):
                wait_time = limiter.get_wait_time(user_id)
                await update.message.reply_text(
                    f"⏳ Slow down! Please wait {wait_time} seconds before trying again."
                )
                return
            
            return await func(self, update, context)
        return wrapper
    return decorator


class BotHealth:
    """Track bot health and statistics"""
    
    def __init__(self):
        self.start_time = time.time()
        self.command_count = 0
        self.error_count = 0
        self.last_error = None
    
    def record_command(self):
        """Record a command execution"""
        self.command_count += 1
    
    def record_error(self, error: Exception):
        """Record an error"""
        self.error_count += 1
        self.last_error = str(error)
        logger.error(f"Bot error: {error}", exc_info=True)
    
    def get_uptime(self) -> str:
        """Get bot uptime as formatted string"""
        uptime_seconds = int(time.time() - self.start_time)
        
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        
        return " ".join(parts)
    
    def get_status(self) -> dict:
        """Get bot status"""
        return {
            'uptime': self.get_uptime(),
            'commands_processed': self.command_count,
            'errors': self.error_count,
            'last_error': self.last_error
        }


def format_error_message(error: Exception) -> str:
    """Format error message for users"""
    error_str = str(error).lower()
    
    # Common errors and user-friendly messages
    if 'connection' in error_str or 'timeout' in error_str:
        return "⚠️ Connection error. The ESPN API might be slow. Please try again in a moment."
    elif 'not found' in error_str or '404' in error_str:
        return "⚠️ Data not found. This might be an off-season or the league data isn't available yet."
    elif 'forbidden' in error_str or '403' in error_str:
        return "⚠️ Access denied. Check your ESPN credentials in the .env file."
    elif 'unauthorized' in error_str or '401' in error_str:
        return "⚠️ Authorization failed. Your ESPN cookies might have expired."
    else:
        return f"❌ An error occurred: {str(error)}\n\nIf this persists, contact the bot admin."


def safe_command(func: Callable):
    """Decorator to safely handle command errors"""
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            # Record command if health tracker exists
            if hasattr(self, 'health'):
                self.health.record_command()
            
            return await func(self, update, context)
        except Exception as e:
            # Record error if health tracker exists
            if hasattr(self, 'health'):
                self.health.record_error(e)
            
            # Send user-friendly error message
            error_msg = format_error_message(e)
            await update.message.reply_text(error_msg)
            
            # Log full error for debugging
            logger.exception(f"Error in {func.__name__}")
    
    return wrapper

