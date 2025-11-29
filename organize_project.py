"""
Organize project files into a clean structure
"""
import os
import shutil
import sys

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def organize_project():
    """Organize files into proper folders"""
    
    print("="*60)
    print("  Project File Organization")
    print("="*60)
    print()
    
    # Create directory structure
    directories = {
        'docs': 'Documentation files',
        'tests': 'Test and debug scripts',
        'scripts': 'Utility and helper scripts',
        'archive': 'Old/unused bot versions',
    }
    
    for dir_name, description in directories.items():
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"✅ Created {dir_name}/ - {description}")
    
    print()
    print("-"*60)
    print("File Organization Plan:")
    print("-"*60)
    print()
    
    # Files to move
    moves = {
        # Documentation
        'docs': [
            'IMPROVEMENTS.md',
            'QUICK_START.md',
            'SUMMARY.md',
            'WAIVER_FIX.md',
            'RESTART_INSTRUCTIONS.md',
            'DATA_VERIFICATION.md',
            'DEPLOYMENT.md',
            'DEPLOYMENT_CHECKLIST.md',
            'DEPLOY_TO_PI.md',
            'FINAL_STATUS.md',
            'GET_ESPN_COOKIES.md',
            'ODDS_API_SETUP.md',
            'PROJECT_STATUS.md',
            'PROJECT_SUMMARY.md',
            'RASPBERRY_PI_SETUP.md',
            'SETUP_GUIDE.md',
            'USER_LINKING_GUIDE.md',
            'USAGE.md',
        ],
        
        # Test files
        'tests': [
            'test_bot_simple.py',
            'test_waiver_fix.py',
            'debug_waiver.py',
            'debug_waiver2.py',
            'debug_espn_fields.py',
            'verify_league_scoring.py',
            'test_bot_live.py',
            'test_myteam.py',
            'test_real_espn.py',
            'test_setup.py',
            'debug_espn.py',
            'debug_espn2.py',
            'debug_team_data.py',
            'demo_analytics.py',
            'player_fields.txt',
        ],
        
        # Helper scripts
        'scripts': [
            'easy_setup.py',
            'get_chat_id.py',
            'setup_and_test.bat',
            'STOP_BOT.bat',
            'QUICK_RESTART.bat',
            'restart_bot.bat',
        ],
        
        # Old bot versions
        'archive': [
            'bot.py',
            'final_bot.py',
            'minimal_bot.py',
            'real_bot.py',
            'run_bot.py',
            'simple_bot.py',
            'simple_bot_start.py',
            'simple_http_bot.py',
            'working_bot.py',
            'start_bot.bat',
        ],
    }
    
    # Files to keep in root
    keep_in_root = [
        # Main bot files
        'final_working_bot.py',
        'enhanced_bot.py',
        
        # Core modules
        'commands.py',
        'espn_api.py',
        'analytics.py',
        'state_manager.py',
        'user_commands.py',
        'user_mapping.py',
        'simple_team_picker.py',
        'optimal_lineup.py',
        'odds_api.py',
        'scheduler.py',
        'bot_enhancements.py',
        
        # Config files
        'config.py',
        'requirements.txt',
        'env.example',
        
        # Data files
        'state.json',
        'user_team_mapping.json',
        'bot.log',
        
        # Main launchers
        'RUN_BOT_NOW.bat',
        
        # Documentation (key ones)
        'README.md',
        
        # Git
        '.gitignore',
        '.git',
    ]
    
    # Show what will be moved
    for target_dir, files in moves.items():
        existing = [f for f in files if os.path.exists(f)]
        if existing:
            print(f"\n{target_dir}/")
            for f in existing:
                print(f"  ← {f}")
    
    print()
    print("-"*60)
    print("\nProceed with organization? (This will move files)")
    print("Type 'yes' to continue: ", end='')
    
    response = input().strip().lower()
    
    if response == 'yes':
        print()
        print("Moving files...")
        print()
        
        moved_count = 0
        for target_dir, files in moves.items():
            for filename in files:
                if os.path.exists(filename):
                    dest = os.path.join(target_dir, filename)
                    try:
                        shutil.move(filename, dest)
                        print(f"✅ Moved {filename} → {target_dir}/")
                        moved_count += 1
                    except Exception as e:
                        print(f"❌ Error moving {filename}: {e}")
        
        print()
        print(f"✅ Organized {moved_count} files!")
        print()
        print("="*60)
        print("  New Project Structure")
        print("="*60)
        print()
        print("Root/")
        print("  ├── final_working_bot.py       (Main bot - FIXED)")
        print("  ├── enhanced_bot.py            (Enhanced version)")
        print("  ├── RUN_BOT_NOW.bat            (Quick launcher)")
        print("  ├── commands.py                (All bot commands)")
        print("  ├── espn_api.py                (ESPN API wrapper)")
        print("  ├── analytics.py               (Analytics logic)")
        print("  ├── bot_enhancements.py        (Rate limiting, health)")
        print("  ├── requirements.txt           (Dependencies)")
        print("  ├── README.md                  (Main docs)")
        print("  │")
        print("  ├── docs/                      (All documentation)")
        print("  ├── tests/                     (Test & debug scripts)")
        print("  ├── scripts/                   (Helper scripts)")
        print("  └── archive/                   (Old bot versions)")
        print()
        
    else:
        print("\n❌ Organization cancelled")

if __name__ == "__main__":
    organize_project()

