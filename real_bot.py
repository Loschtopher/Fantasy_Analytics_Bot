"""
Real Fantasy Football Bot with ESPN Integration
"""
import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_CHAT_IDS = os.getenv('ALLOWED_CHAT_IDS', '').split(',')
ESPN_LEAGUE_ID = os.getenv('ESPN_LEAGUE_ID')
ESPN_SWID = os.getenv('ESPN_SWID')
ESPN_S2 = os.getenv('ESPN_S2')

def _is_allowed_chat(chat_id: int) -> bool:
    """Check if chat is allowed to use the bot"""
    if not ALLOWED_CHAT_IDS or ALLOWED_CHAT_IDS == ['']:
        return True
    return str(chat_id) in ALLOWED_CHAT_IDS

def send_message(chat_id, text):
    """Send a message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, data=data)
        return response.status_code == 200
    except:
        return False

def get_espn_data(endpoint, params=None):
    """Get data from ESPN API"""
    url = f"https://fantasy.espn.com/apis/v3/games/ffl/{endpoint}"
    
    cookies = {
        'SWID': ESPN_SWID,
        'espn_s2': ESPN_S2
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, params=params, cookies=cookies, headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"ESPN API Error: {e}")
    return None

def get_league_teams():
    """Get teams from ESPN league"""
    params = {
        'seasonId': 2025,
        'leagueId': ESPN_LEAGUE_ID
    }
    
    data = get_espn_data(f"leagueHistory/{ESPN_LEAGUE_ID}", params)
    if data and 'teams' in data:
        return data['teams']
    return []

def get_current_week():
    """Get current week from ESPN"""
    params = {
        'seasonId': 2025,
        'leagueId': ESPN_LEAGUE_ID
    }
    
    data = get_espn_data(f"leagueHistory/{ESPN_LEAGUE_ID}", params)
    if data and 'status' in data:
        return data['status'].get('currentMatchupPeriod', 1)
    return 1

def handle_power_command():
    """Generate real power rankings from ESPN data"""
    teams = get_league_teams()
    if not teams:
        return "Error: Could not retrieve league data from ESPN."
    
    message = "Power Rankings:\n\n"
    
    # Sort teams by record
    sorted_teams = sorted(teams, key=lambda x: (
        x.get('record', {}).get('wins', 0),
        x.get('pointsFor', 0)
    ), reverse=True)
    
    for i, team in enumerate(sorted_teams[:10], 1):  # Top 10
        name = team.get('name', 'Unknown')
        abbrev = team.get('abbrev', 'UNK')
        record = team.get('record', {})
        wins = record.get('wins', 0)
        losses = record.get('losses', 0)
        ties = record.get('ties', 0)
        pf = team.get('pointsFor', 0)
        pa = team.get('pointsAgainst', 0)
        
        win_pct = (wins + 0.5 * ties) / max(wins + losses + ties, 1)
        
        message += f"{i}. **{name}** ({abbrev})\n"
        message += f"   Record: {wins}-{losses}-{ties} ({win_pct:.3f})\n"
        message += f"   PF: {pf:.1f} | PA: {pa:.1f}\n\n"
    
    return message

def handle_help_command():
    """Generate help message"""
    return """Fantasy Football Analytics Bot Commands:

/power - Power Rankings with real ESPN data
/recap - Weekly Recap with highlights
/luck - Luck Analysis (Pythagorean expectation)
/all - All-Play Records
/boom - Boom/Bust Analysis
/regret - Start/Sit Regret Analysis
/elo - ELO Ratings
/odds - Playoff Odds (Monte Carlo)
/sos - Strength of Schedule
/heat - Heat Map (Z-scores)
/rivals - Rivalry Tracker
/help - This command list

Bot is connected to ESPN League 361353 (Season 2025)"""

def handle_command(message_text, chat_id):
    """Handle bot commands"""
    if message_text.startswith('/help'):
        return handle_help_command()
    
    elif message_text.startswith('/power'):
        return handle_power_command()
    
    elif message_text.startswith('/boom'):
        return "Boom/Bust Analysis:\n\nFeature coming soon with real ESPN data integration!"
    
    elif message_text.startswith('/recap'):
        return "Weekly Recap:\n\nFeature coming soon with real ESPN data integration!"
    
    else:
        return "Command not recognized. Try /help to see available commands."

def get_updates(last_update_id=None):
    """Get updates from Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    params = {'timeout': 30}
    if last_update_id:
        params['offset'] = last_update_id + 1
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def main():
    """Main bot loop"""
    print("Starting Real Fantasy Football Analytics Bot...")
    
    if not TELEGRAM_BOT_TOKEN:
        print("ERROR: No bot token found. Check your .env file.")
        return
    
    # Test ESPN connection
    print("Testing ESPN connection...")
    teams = get_league_teams()
    if teams:
        print(f"SUCCESS: Connected to ESPN League {ESPN_LEAGUE_ID}")
        print(f"Found {len(teams)} teams")
        current_week = get_current_week()
        print(f"Current week: {current_week}")
    else:
        print("WARNING: Could not connect to ESPN. Bot will still work but with limited data.")
    
    print("Bot started successfully!")
    print("Try /help in your chat to see available commands")
    
    last_update_id = None
    
    while True:
        try:
            updates = get_updates(last_update_id)
            if updates and updates.get('ok'):
                for update in updates.get('result', []):
                    last_update_id = update.get('update_id')
                    
                    message = update.get('message')
                    if message:
                        chat_id = message.get('chat', {}).get('id')
                        text = message.get('text', '')
                        
                        if text.startswith('/') and _is_allowed_chat(chat_id):
                            response = handle_command(text, chat_id)
                            send_message(chat_id, response)
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\nBot stopped by user")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()



