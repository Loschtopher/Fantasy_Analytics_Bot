"""
Test script to validate bot setup and ESPN API connectivity
"""
import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment variables are set correctly"""
    print("🔍 Testing Environment Variables...")
    
    load_dotenv()
    
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'ESPN_LEAGUE_ID',
        'ESPN_SWID',
        'ESPN_S2'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def test_imports():
    """Test that all required packages can be imported"""
    print("\n📦 Testing Package Imports...")
    
    try:
        import telegram
        print("✅ python-telegram-bot imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-telegram-bot: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    try:
        import numpy
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import numpy: {e}")
        return False
    
    try:
        import pandas
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import pandas: {e}")
        return False
    
    return True

def test_espn_api():
    """Test ESPN API connectivity"""
    print("\n🌐 Testing ESPN API Connectivity...")
    
    try:
        from espn_api import ESPNAPI
        
        api = ESPNAPI()
        
        # Test basic league info
        league_info = api.get_league_info()
        if league_info:
            print("✅ ESPN API connection successful")
            print(f"   League ID: {api.league_id}")
            return True
        else:
            print("❌ ESPN API returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ ESPN API test failed: {e}")
        return False

def test_telegram_bot():
    """Test Telegram bot token"""
    print("\n🤖 Testing Telegram Bot Token...")
    
    try:
        import requests
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        url = f"https://api.telegram.org/bot{token}/getMe"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                print("✅ Telegram bot token is valid")
                print(f"   Bot name: {bot_info.get('first_name')}")
                print(f"   Username: @{bot_info.get('username')}")
                return True
            else:
                print("❌ Invalid bot token")
                return False
        else:
            print(f"❌ Telegram API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Telegram bot test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Fantasy Football Bot Setup Test\n")
    
    tests = [
        test_environment,
        test_imports,
        test_telegram_bot,
        test_espn_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your bot is ready to run.")
        print("\nTo start the bot, run:")
        print("python bot.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above before running the bot.")
        sys.exit(1)

if __name__ == "__main__":
    main()


