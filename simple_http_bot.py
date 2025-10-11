"""
Simple HTTP-based Fantasy Football Bot - Python 3.13 Compatible
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

def handle_command(message_text, chat_id):
    """Handle bot commands"""
    if message_text.startswith('/help'):
        return "Fantasy Football Analytics Bot Commands:\n\n/power - Power Rankings\n/recap - Weekly Recap\n/luck - Luck Analysis\n/all - All-Play Records\n/boom - Boom/Bust Analysis\n/regret - Start/Sit Regret\n/elo - ELO Ratings\n/odds - Playoff Odds\n/sos - Strength of Schedule\n/heat - Heat Map\n/rivals - Rivalry Tracker\n/help - This command list"
    
    elif message_text.startswith('/power'):
        return "Power Rankings:\n\n1. Team Alpha (ALP) ▲\n   Record: 8-2-0 (0.800) | PF: 1250.5\n   Streak: W3 | Score: 0.847\n\n2. Team Beta (BET) ▼\n   Record: 7-3-0 (0.700) | PF: 1200.0\n   Streak: L1 | Score: 0.723\n\n*Full ESPN integration coming soon!*"
    
    elif message_text.startswith('/boom'):
        return "Boom/Bust Analysis:\n\nTeam Alpha (ALP)\nCeiling (P80): 145.2 | Floor (P20): 98.7\nSpread: 46.5 | Consistency: 0.023\n\n*Live data integration coming soon!*"
    
    elif message_text.startswith('/recap'):
        return "Weekly Recap:\n\nFeature coming soon!\nThis will show high/low scores, closest games, and biggest blowouts."
    
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
    print("Starting Fantasy Football Analytics Bot...")
    
    if not TELEGRAM_BOT_TOKEN:
        print("ERROR: No bot token found. Check your .env file.")
        return
    
    print("Bot started successfully!")
    print("Try /help in your chat to see available commands")
    print("Bot is connected to chat IDs:", ALLOWED_CHAT_IDS)
    
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



