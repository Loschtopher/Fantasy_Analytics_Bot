# Setup Guide for Your Fantasy Football Bot

## ✅ Current Status
Your bot is set up with the following credentials:
- **League ID**: 361353
- **Season**: 2025
- **ESPN SWID & S2**: Configured
- **Environment**: Ready

## 🔧 Final Setup Steps

### 1. Get Your Telegram Bot Token

1. **Message @BotFather** on Telegram
2. **Send `/newbot`** command
3. **Choose a name** for your bot (e.g., "Fantasy Football Analytics")
4. **Choose a username** (must end in 'bot', e.g., "fantasy_analytics_bot")
5. **Copy the token** (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Update Your .env File

Edit the `.env` file in your project folder:

```env
# Replace this line:
TELEGRAM_BOT_TOKEN=xxxxx:yyyyyyyyy

# With your actual token:
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 3. Get Your Chat ID

1. **Add your bot to your group chat**
2. **Send any message** in the chat (like "test")
3. **Visit this URL** (replace with your actual token):
   ```
   https://api.telegram.org/bot123456789:ABCdefGHIjklMNOpqrsTUVwxyz/getUpdates
   ```
4. **Find the chat ID** in the response (look for `"chat":{"id":-1001234567890}`)
5. **Add it to .env**:
   ```env
   ALLOWED_CHAT_IDS=-1001234567890
   ```

### 4. Test Your Setup

Run the test script:
```bash
python test_windows.py
```

You should see all tests pass!

### 5. Start Your Bot

Run the bot:
```bash
python run_bot.py
```

## 🎉 Your Bot Commands

Once running, your bot will respond to these commands:

- `/power` - Power Rankings with movement tracking
- `/recap` - Weekly highlights and game analysis
- `/luck` - Pythagorean expectation luck analysis
- `/all` - All-play records (season and weekly)
- `/boom` - Boom/bust consistency metrics
- `/regret` - Start/sit regret analysis
- `/elo` - Head-to-head ELO ratings
- `/odds` - Monte Carlo playoff simulations
- `/sos` - Strength of schedule analysis
- `/heat` - Weekly z-score heat map
- `/rivals` - Rivalry tracker and analysis
- `/help` - Complete command reference

## 🔄 Auto-Posting

Your bot will automatically post power rankings every **Tuesday at 10 AM ET**. No setup required!

## 🛠️ Troubleshooting

### Bot Not Responding
- Check your Telegram bot token is correct
- Verify the chat ID is added to ALLOWED_CHAT_IDS
- Make sure the bot is added to your group chat

### ESPN API Errors
- Your SWID and S2 cookies are already configured
- If you get errors, the cookies may have expired (they last ~30 days)
- You can get new ones from ESPN Fantasy Football

### Commands Not Working
- Make sure you're using the exact command format (e.g., `/power`, not `power`)
- Check the bot is running (you should see "Bot started successfully!")

## 📊 What Your Bot Provides

Your Fantasy Football Analytics Bot will provide:

1. **Advanced Power Rankings** - Weighted scoring with week-over-week movement
2. **Luck Analysis** - Pythagorean expectation vs actual wins
3. **Playoff Odds** - Monte Carlo simulations of remaining schedule
4. **Strength of Schedule** - How tough each team's schedule has been
5. **Boom/Bust Analysis** - Consistency and variance metrics
6. **Rivalry Tracking** - Head-to-head records and streaks
7. **Weekly Recaps** - High/low scores, closest games, biggest blowouts
8. **ELO Ratings** - Head-to-head strength ratings
9. **Heat Maps** - Performance trends with visual indicators
10. **All-Play Records** - What records would be if everyone played everyone

## 🚀 Ready to Go!

Your bot is configured and ready to provide advanced analytics for your ESPN Fantasy Football league. Once you complete the Telegram setup, you'll have the most comprehensive fantasy football analytics tool available!

**Next Step**: Get your Telegram bot token and update the .env file, then run `python run_bot.py` to start your bot!










