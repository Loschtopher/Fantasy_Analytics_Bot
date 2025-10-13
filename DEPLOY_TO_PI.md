# 🥧 DEPLOY TO RASPBERRY PI - QUICK GUIDE

## ✅ Your Bot is Ready to Deploy!

Your code is on GitHub: https://github.com/Loschtopher/Fantasy_Analytics_Bot

---

## 🚀 **STEP 1: SSH into Your Raspberry Pi**

On your Windows PC, open PowerShell or Command Prompt:

```bash
ssh pi@YOUR_PI_IP_ADDRESS
```

**Default password:** `raspberry` (unless you changed it)

**Don't know your Pi's IP?** Check your router or run this on the Pi:
```bash
hostname -I
```

---

## 📦 **STEP 2: Clone the Repository**

Once connected to your Pi:

```bash
cd ~
git clone https://github.com/Loschtopher/Fantasy_Analytics_Bot.git
cd Fantasy_Analytics_Bot
```

---

## 🔧 **STEP 3: Install Python & Dependencies**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+ (if not already installed)
sudo apt install python3 python3-pip python3-venv -y

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🔑 **STEP 4: Configure Environment Variables**

Create your `.env` file:

```bash
nano .env
```

Paste this (use your actual values):

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=8443429617:AAGeQUK1jnKCwicCmU4-04hS9n7mzEwUoTU
ALLOWED_CHAT_IDS=1375980805

# ESPN Fantasy Football Configuration
ESPN_LEAGUE_ID=361353
ESPN_SWID={AD9C8849-E351-41B7-9BDC-4085193C8A92}
ESPN_S2=AECTisLqMTwjOmL8vJb3lBK9pfHSUcTMYKw4jVfYlBtOD97BDWOZypCGsXMhIiXc45JGNiqNYk0dZ6yDBysudNoWbp77O6kL8cjOfK9E/xYsJHxvri8mCgeMuBMzuR5SLLsY9PnQItRBxtn/AcQRwg6cGIFT9kgz79XJYdNpWJMIp5vSoqO/M4hYwRY74TBo/TgpMCpBOJxGeUp7mkw9PsA+XsVFkS2YFmH9bUz1223zYjInAdgR+mDIx4gi5eMIcHyXkvqjVKcmxnPSUg2xASLojgSv44811axLqbAh99TJmg==

# The Odds API (Optional)
ODDS_API_KEY=your_odds_api_key_here
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

---

## 🧪 **STEP 5: Test the Bot**

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Run the bot
python final_working_bot.py
```

**If you see:** `🎉 BOT IS ONLINE!` → **SUCCESS!** ✅

**Test in Telegram:** Send `/start` to your bot

Press `Ctrl+C` to stop the bot for now.

---

## 🔄 **STEP 6: Set Up Auto-Start (Run Forever!)**

Create a systemd service to run the bot automatically:

```bash
sudo nano /etc/systemd/system/fantasy-bot.service
```

Paste this (replace `pi` with your username if different):

```ini
[Unit]
Description=Fantasy Football Analytics Telegram Bot
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Fantasy_Analytics_Bot
Environment="PATH=/home/pi/Fantasy_Analytics_Bot/venv/bin"
ExecStart=/home/pi/Fantasy_Analytics_Bot/venv/bin/python final_working_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Save:** `Ctrl+X`, `Y`, `Enter`

---

## ▶️ **STEP 7: Start the Service**

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable fantasy-bot

# Start the bot now
sudo systemctl start fantasy-bot

# Check status
sudo systemctl status fantasy-bot
```

**If you see:** `active (running)` in green → **PERFECT!** ✅

---

## 📊 **STEP 8: Monitor Your Bot**

### **Check if running:**
```bash
sudo systemctl status fantasy-bot
```

### **View logs:**
```bash
sudo journalctl -u fantasy-bot -f
```

### **Restart bot:**
```bash
sudo systemctl restart fantasy-bot
```

### **Stop bot:**
```bash
sudo systemctl stop fantasy-bot
```

---

## 🔄 **Update Your Bot (Future)**

When you make changes on Windows and push to GitHub:

```bash
# SSH into Pi
ssh pi@YOUR_PI_IP

# Navigate to bot directory
cd ~/Fantasy_Analytics_Bot

# Pull latest changes
git pull

# Restart the bot
sudo systemctl restart fantasy-bot

# Check it's running
sudo systemctl status fantasy-bot
```

---

## 🎯 **Quick Commands Reference**

| Task | Command |
|------|---------|
| Start bot | `sudo systemctl start fantasy-bot` |
| Stop bot | `sudo systemctl stop fantasy-bot` |
| Restart bot | `sudo systemctl restart fantasy-bot` |
| Check status | `sudo systemctl status fantasy-bot` |
| View logs | `sudo journalctl -u fantasy-bot -f` |
| Update code | `cd ~/Fantasy_Analytics_Bot && git pull && sudo systemctl restart fantasy-bot` |

---

## 🆘 **Troubleshooting**

### **Bot won't start?**
```bash
# Check logs for errors
sudo journalctl -u fantasy-bot -n 50
```

### **Connection issues?**
```bash
# Test manually
cd ~/Fantasy_Analytics_Bot
source venv/bin/activate
python final_working_bot.py
```

### **Need to update ESPN cookies?**
```bash
# Edit .env file
nano ~/.Fantasy_Analytics_Bot/.env

# Update ESPN_S2 and ESPN_SWID
# Save and restart
sudo systemctl restart fantasy-bot
```

---

## 📱 **Expected Behavior:**

Once deployed:
- ✅ Bot runs 24/7 on Raspberry Pi
- ✅ Auto-restarts if it crashes
- ✅ Starts automatically on Pi reboot
- ✅ You can close your Windows PC - bot keeps running!

---

## 🎉 **You're Done!**

Your bot will now run indefinitely on your Raspberry Pi! Test all your commands in Telegram:

- `/power` - Power rankings
- `/luck` - Luck analysis
- `/waiver` - Waiver wire gems
- `/parlay` - TD parlay picks
- `/yolo` - Longshot parlays
- And ALL the others!

**Your league is about to get a lot more fun!** 🏈🎰💎

