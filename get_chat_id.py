"""Quick script to get Telegram chat ID"""
import requests
import json

TOKEN = "8443429617:AAEzr52J4bW3S2ovQfP02-n6NInAK4xNRcw"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

try:
    response = requests.get(url)
    data = response.json()
    
    if data.get('ok') and data.get('result'):
        print("✅ Found messages! Here are your chat IDs:\n")
        chat_ids = set()
        for update in data['result']:
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                chat_name = update['message']['chat'].get('title', update['message']['chat'].get('first_name', 'Unknown'))
                chat_ids.add((chat_id, chat_name))
        
        for chat_id, name in chat_ids:
            print(f"Chat ID: {chat_id}")
            print(f"Chat Name: {name}")
            print()
        
        if len(chat_ids) == 1:
            print(f"\n✅ Your chat ID is: {list(chat_ids)[0][0]}")
    else:
        print("⚠️  No messages found yet.")
        print("\n📱 To get your chat ID:")
        print("1. Open Telegram")
        print("2. Find your bot or add it to a group")
        print("3. Send any message (like 'test')")
        print("4. Run this script again")
        
except Exception as e:
    print(f"❌ Error: {e}")


