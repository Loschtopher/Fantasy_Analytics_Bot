# Deployment Guide

## 🚀 Quick Deployment

### 1. Environment Setup
```bash
# Clone or download the project
cd telegram-fantasy-football-analytics

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp env.example .env
```

### 2. Configuration
Edit `.env` file with your credentials:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
ALLOWED_CHAT_IDS=chat_id_1,chat_id_2

# ESPN Fantasy Football Configuration
ESPN_LEAGUE_ID=your_league_id
ESPN_SWID=your_swid_cookie
ESPN_S2=your_s2_cookie
```

### 3. Get Credentials

#### ESPN Credentials
1. **League ID**: Found in your ESPN league URL
   - URL: `https://fantasy.espn.com/football/league?leagueId=123456`
   - League ID: `123456`

2. **SWID and S2 Cookies**:
   - Log into ESPN Fantasy Football
   - Open Developer Tools (F12)
   - Go to Application → Cookies
   - Find `SWID` and `espn_s2` cookies
   - Copy their values

#### Telegram Bot Token
1. Message @BotFather on Telegram
2. Use `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token

#### Chat IDs
1. Add your bot to your group chat
2. Send a message in the chat
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find the chat ID in the response

### 4. Test Setup
```bash
# Run the test script
python test_setup.py
```

### 5. Start the Bot
```bash
# Run the bot
python run_bot.py

# Or use the batch file (Windows)
start_bot.bat
```

## 🔧 Production Deployment

### Option 1: VPS/Cloud Server
```bash
# Install Python and dependencies
sudo apt update
sudo apt install python3 python3-pip

# Clone the repository
git clone <your-repo-url>
cd telegram-fantasy-football-analytics

# Install dependencies
pip3 install -r requirements.txt

# Set up environment
cp env.example .env
nano .env  # Edit with your credentials

# Run as a service
sudo systemctl create-fantasy-bot.service
```

### Option 2: Docker (Recommended)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "run_bot.py"]
```

### Option 3: Heroku
```bash
# Create Procfile
echo "worker: python run_bot.py" > Procfile

# Deploy to Heroku
heroku create your-bot-name
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set ESPN_LEAGUE_ID=your_league_id
heroku config:set ESPN_SWID=your_swid
heroku config:set ESPN_S2=your_s2
heroku config:set ALLOWED_CHAT_IDS=chat_id_1,chat_id_2

git push heroku main
```

## 📊 Monitoring

### Logs
- Bot logs are written to `bot.log`
- Check logs for errors: `tail -f bot.log`

### Health Checks
- Test bot responsiveness: Send `/help` command
- Check ESPN API: Run `python test_setup.py`
- Verify auto-posting: Check logs for Tuesday 10 AM posts

### Maintenance
- **Weekly**: Check logs for errors
- **Monthly**: Update dependencies if needed
- **Season**: Update ESPN season year in config.py

## 🛠️ Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check Telegram bot token
   - Verify chat IDs are correct
   - Ensure bot is added to the chat

2. **ESPN API errors**
   - Check SWID and S2 cookies (they expire)
   - Verify league ID is correct
   - Ensure league is accessible

3. **Auto-posting not working**
   - Check system time/timezone
   - Verify ALLOWED_CHAT_IDS are set
   - Check scheduler logs

### Getting Help
1. Check the logs in `bot.log`
2. Run `python test_setup.py` for diagnostics
3. Verify all environment variables are set
4. Test ESPN API access manually

## 🔒 Security Best Practices

1. **Never commit** `.env` file to version control
2. **Use environment variables** in production
3. **Restrict chat access** with ALLOWED_CHAT_IDS
4. **Rotate credentials** periodically
5. **Monitor logs** for suspicious activity

## 📈 Scaling

### Multiple Leagues
- Run separate bot instances for each league
- Use different environment files
- Consider containerization for easy management

### High Availability
- Use process managers like PM2 or systemd
- Set up health checks and auto-restart
- Consider load balancing for multiple instances

## 🎯 Success Metrics

Track these metrics to measure bot success:
- **Command usage** frequency
- **Auto-post engagement** (reactions, replies)
- **League participation** increase
- **Error rates** and uptime
- **User feedback** and feature requests

The bot is designed to be reliable and low-maintenance, providing consistent value to your fantasy football league!










