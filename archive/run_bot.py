"""
Simple startup script for the Fantasy Football Bot
"""
import asyncio
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from bot import main
    print("Starting Fantasy Football Analytics Bot...")
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nBot stopped by user")
except Exception as e:
    print(f"Error starting bot: {e}")
    sys.exit(1)

