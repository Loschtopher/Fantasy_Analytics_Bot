"""
Example configuration file showing different customization options
"""

# Example power ranking weights - customize based on your league preferences
EXAMPLE_POWER_WEIGHTS = {
    'win_percentage': 0.4,      # 40% - Overall record
    'recent_form': 0.25,        # 25% - Last 3 games performance
    'efficiency': 0.2,          # 20% - Points for vs points against ratio
    'schedule_strength': 0.15   # 15% - Strength of opponents faced
}

# Example for a more record-focused league
RECORD_FOCUSED_WEIGHTS = {
    'win_percentage': 0.6,      # 60% - Heavy emphasis on wins
    'recent_form': 0.2,         # 20% - Recent performance
    'efficiency': 0.15,         # 15% - Efficiency matters less
    'schedule_strength': 0.05   # 5% - Schedule strength less important
}

# Example for a more scoring-focused league
SCORING_FOCUSED_WEIGHTS = {
    'win_percentage': 0.3,      # 30% - Wins matter but less
    'recent_form': 0.25,        # 25% - Recent scoring trends
    'efficiency': 0.35,         # 35% - Heavy emphasis on scoring efficiency
    'schedule_strength': 0.1    # 10% - Some schedule consideration
}

# Example auto-posting schedules
AUTO_POST_EXAMPLES = {
    'power_rankings_tuesday': {
        'day': 1,      # Tuesday
        'hour': 10,    # 10 AM
        'minute': 0    # On the hour
    },
    'power_rankings_wednesday': {
        'day': 2,      # Wednesday
        'hour': 9,     # 9 AM
        'minute': 30   # 9:30 AM
    },
    'recap_monday': {
        'day': 0,      # Monday
        'hour': 8,     # 8 AM
        'minute': 0    # Start of work week
    }
}

# Example chat configurations
CHAT_CONFIG_EXAMPLES = {
    'single_chat': {
        'allowed_chat_ids': ['-1001234567890']  # Single group chat
    },
    'multiple_chats': {
        'allowed_chat_ids': ['-1001234567890', '-1001234567891', '-1001234567892']
    },
    'all_chats': {
        'allowed_chat_ids': []  # Empty list allows all chats
    }
}

# Example ELO configurations
ELO_CONFIG_EXAMPLES = {
    'standard': {
        'k_factor': 32,
        'initial_rating': 1500
    },
    'volatile': {
        'k_factor': 50,        # Higher K-factor = more volatile ratings
        'initial_rating': 1500
    },
    'stable': {
        'k_factor': 16,        # Lower K-factor = more stable ratings
        'initial_rating': 1500
    }
}

# Example message formatting options
FORMATTING_EXAMPLES = {
    'compact': {
        'show_streaks': False,
        'show_points': False,
        'show_percentages': True
    },
    'detailed': {
        'show_streaks': True,
        'show_points': True,
        'show_percentages': True
    },
    'minimal': {
        'show_streaks': False,
        'show_points': False,
        'show_percentages': False
    }
}

# Example logging configurations
LOGGING_EXAMPLES = {
    'development': {
        'level': 'DEBUG',
        'file': 'bot_debug.log',
        'console': True
    },
    'production': {
        'level': 'INFO',
        'file': 'bot.log',
        'console': False
    },
    'minimal': {
        'level': 'WARNING',
        'file': 'bot_errors.log',
        'console': True
    }
}


