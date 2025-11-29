# Quick Start Guide

## ✅ Bot is Fixed and Ready!

The Telegram bot has been **fixed and enhanced** with better features.

## 🚀 How to Run

### Option 1: Double-click the Batch File (Easiest)
```
RUN_BOT_NOW.bat
```

### Option 2: Run from Command Line
```bash
python final_working_bot.py
```

### Option 3: Run Enhanced Version (Recommended)
```bash
python enhanced_bot.py
```

## 🎯 First Steps After Starting

1. **Start the bot** using one of the methods above
2. **Open Telegram** and find your bot
3. **Type:** `/pickteam` to link your team (one-click with buttons!)
4. **Try:** `/myteam` to see your stats
5. **Explore:** `/help` to see all commands

## 📱 Most Popular Commands

| Command | Description |
|---------|-------------|
| `/pickteam` | 🎯 Pick your team (interactive!) |
| `/myteam` | See your team stats |
| `/power` | Power rankings |
| `/recap` | Weekly recap |
| `/waiver` | Best waiver pickups |
| `/odds` | Playoff chances |
| `/help` | Show all commands |
| `/status` | Bot health check (NEW!) |

## 🛠️ What Was Fixed

1. ✅ **Emoji encoding crash** - Bot now works on Windows
2. ✅ **Better error handling** - More helpful error messages
3. ✅ **Rate limiting** - Prevents spam (10 commands/minute)
4. ✅ **Health monitoring** - New `/status` command
5. ✅ **UTF-8 support** - Emojis work in console

## 📊 Your League Stats

**League ID:** 361353
**Teams:** 12
**Current Season:** Active

### Teams in Your League:
1. Black Beard Penetrators (8-4)
2. First Down Syndrome (10-2)
3. The Ambulance Chasers (7-5)
4. PeePee PooPoo (7-5)
5. The Brothers in Christ (6-6)
6. Hog Crankers (6-6)
7. Team Bill (6-6)
8. Dirty mike and the boys (6-6)
9. 💩 Turd Sandwich 🥪 (6-6)
10. Jax and the gang (5-7)
11. Team Pizza (3-9)
12. Better Call Pearsall (2-10)

## 🔧 Testing

To verify everything works:
```bash
python test_bot_simple.py
```

Should show: **4/4 tests passed** ✅

## 📁 Files

- `final_working_bot.py` - Fixed original bot
- `enhanced_bot.py` - Enhanced version with extra features (NEW!)
- `bot_enhancements.py` - Enhancement utilities (NEW!)
- `RUN_BOT_NOW.bat` - Easy launcher
- `test_bot_simple.py` - Test script (NEW!)
- `IMPROVEMENTS.md` - Detailed improvement docs (NEW!)

## 🎮 Command Categories

### Personal
- `/pickteam` - Link your team
- `/myteam` - Your stats
- `/whoami` - Your info

### Analytics
- `/power` - Rankings
- `/luck` - Lucky/unlucky teams
- `/waiver` - Waiver gems
- `/odds` - Playoff odds
- `/boom` - Consistency
- `/heat` - Weekly trends
- `/sos` - Schedule strength
- `/all` - All-play records

### Weekly
- `/recap` - Week recap
- `/season` - Season highlights
- `/regret` - Lineup analysis
- `/rivals` - Head-to-head

### Betting
- `/parlay` - Safe TD parlay
- `/yolo` - Longshot parlay

### Admin
- `/users` - List users
- `/teams` - List teams
- `/linkuser` - Link user to team
- `/unlink` - Unlink user

### System
- `/status` - Bot health (NEW!)
- `/help` - Help menu

## 🐛 Troubleshooting

### Bot won't start?
1. Check `.env` file exists
2. Verify TELEGRAM_BOT_TOKEN is set
3. Run: `pip install -r requirements.txt`

### Commands not working?
1. Check bot is running
2. Use `/status` to check health
3. Check `bot.log` for errors

### Still having issues?
1. Run `python test_bot_simple.py`
2. Check which test fails
3. Fix that issue first

## 💡 Tips

- Use `/pickteam` first to link your account
- Most commands work without arguments
- Bot logs everything to `bot.log`
- Enhanced version includes rate limiting
- Check `/status` for bot health

## 🎉 You're All Set!

The bot is **fixed and enhanced**. Just run it and enjoy!

**Recommended:** Use `python enhanced_bot.py` for the best experience.

