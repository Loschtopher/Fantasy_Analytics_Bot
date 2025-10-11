"""
Easy Setup Script for Fantasy Football Bot
Walks you through getting all credentials needed
"""
import os
import sys
import webbrowser

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(number, title):
    """Print a step header"""
    print(f"\n{'─'*60}")
    print(f"  STEP {number}: {title}")
    print(f"{'─'*60}\n")

def create_env_file():
    """Interactive setup to create .env file"""
    print_header("🎉 Fantasy Football Bot - Easy Setup")
    
    print("This script will help you set up your bot in 3 easy steps!")
    print("Don't worry - I'll guide you through everything.\n")
    
    input("Press Enter to begin...")
    
    # Step 1: Telegram Bot Token
    print_step(1, "Create Your Telegram Bot")
    print("1. Open Telegram and search for '@BotFather'")
    print("2. Send the command: /newbot")
    print("3. Choose a name for your bot (e.g., 'Fantasy Football Analytics')")
    print("4. Choose a username (must end in 'bot', e.g., 'my_ff_analytics_bot')")
    print("5. BotFather will give you a token that looks like:")
    print("   123456789:ABCdefGHIjklMNOpqrsTUVwxyz\n")
    
    token = input("Paste your bot token here: ").strip()
    
    if not token or ':' not in token:
        print("❌ That doesn't look like a valid token. Please try again.")
        sys.exit(1)
    
    # Step 2: Chat ID
    print_step(2, "Get Your Chat ID")
    print("1. Add your bot to your group chat (or use a private chat)")
    print("2. Send any message in the chat (e.g., 'test')")
    print("3. I'll open a webpage to help you find your chat ID...")
    
    input("\nPress Enter to open the webpage...")
    
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    try:
        webbrowser.open(url)
        print(f"\n✅ Opened: {url}")
    except:
        print(f"\n⚠️  Couldn't open browser. Visit this URL manually:")
        print(f"   {url}")
    
    print("\n4. Look for 'chat':{'id': -1001234567890}")
    print("   Copy the number (including the minus sign if present)\n")
    
    chat_id = input("Paste your chat ID here: ").strip()
    
    if not chat_id:
        print("❌ Chat ID cannot be empty. Please try again.")
        sys.exit(1)
    
    # Step 3: ESPN Credentials
    print_step(3, "ESPN Credentials")
    print("I need your ESPN Fantasy Football credentials.\n")
    
    league_id = input("ESPN League ID (press Enter to use 361353): ").strip()
    if not league_id:
        league_id = "361353"
    
    print("\nTo get your SWID and S2 cookies:")
    print("1. Log into ESPN Fantasy Football in your browser")
    print("2. Press F12 to open Developer Tools")
    print("3. Go to Application → Cookies")
    print("4. Find 'SWID' and 'espn_s2' cookies\n")
    
    swid = input("Paste your SWID cookie: ").strip()
    s2 = input("Paste your ESPN_S2 cookie: ").strip()
    
    # Create .env file
    print_step(4, "Creating Configuration")
    
    env_content = f"""# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN={token}
ALLOWED_CHAT_IDS={chat_id}

# ESPN Fantasy Football Configuration
ESPN_LEAGUE_ID={league_id}
ESPN_SWID={swid}
ESPN_S2={s2}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Successfully created .env file!")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        print("\nPlease create a file named '.env' with this content:")
        print(env_content)
        sys.exit(1)
    
    # Final instructions
    print_header("🎉 Setup Complete!")
    print("Your bot is now configured and ready to run!\n")
    print("Next steps:")
    print("1. Test your setup:")
    print("   python test_setup.py\n")
    print("2. Start your bot:")
    print("   python run_bot.py\n")
    print("3. Try commands in Telegram:")
    print("   /help - See all available commands")
    print("   /power - Get power rankings")
    print("   /recap - Weekly recap\n")
    print("Your bot will auto-post power rankings every Tuesday at 10 AM ET!")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        create_env_file()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)


