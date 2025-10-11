# 🍓 Raspberry Pi Deployment Guide

This guide will help you deploy your Fantasy Football Bot to run 24/7 on your Raspberry Pi.

## 📋 Prerequisites

- Raspberry Pi (any model with network connectivity)
- Raspberry Pi OS installed
- SSH access or keyboard/monitor connected
- Internet connection

## 🚀 Quick Start

### Step 1: Transfer Files to Raspberry Pi

**Option A: Using USB Drive**
1. Copy your entire project folder to a USB drive
2. Insert USB drive into Raspberry Pi
3. Copy files to Pi: `cp -r /media/usb/Telegram\ Fantasy\ Football\ Analytics ~/`

**Option B: Using Git (Recommended)**
1. Push your code to GitHub (create a private repo!)
2. On Raspberry Pi: `git clone <your-repo-url>`

**Option C: Using SCP (from Windows)**
```powershell
# From your Windows machine
scp -r "C:\Users\slick\Telegram Fantasy Football Analytics" pi@<raspberry-pi-ip>:~/
```

### Step 2: Install Dependencies on Raspberry Pi

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and pip (if not already installed)
sudo apt install python3 python3-pip -y

# Navigate to your project
cd ~/Telegram\ Fantasy\ Football\ Analytics/

# Install required packages
pip3 install -r requirements.txt
```

### Step 3: Configure Environment

Your `.env` file should already be configured from your Windows setup. If not, run:

```bash
python3 easy_setup.py
```

### Step 4: Test the Bot

```bash
# Test your setup
python3 test_setup.py

# If all tests pass, start the bot
python3 run_bot.py
```

You should see: "Bot started successfully!" 

Test by sending `/help` in your Telegram chat.

Press `Ctrl+C` to stop the bot.

## 🔄 Running Bot 24/7

To keep your bot running even after you disconnect, we'll use `systemd`.

### Create a Systemd Service

1. **Create a service file:**

```bash
sudo nano /etc/systemd/system/fantasy-football-bot.service
```

2. **Paste this configuration** (adjust paths if needed):

```ini
[Unit]
Description=Fantasy Football Analytics Telegram Bot
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Telegram Fantasy Football Analytics
ExecStart=/usr/bin/python3 /home/pi/Telegram Fantasy Football Analytics/run_bot.py
Restart=always
RestartSec=10

# Logging
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

3. **Save and exit** (Ctrl+X, then Y, then Enter)

### Enable and Start the Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable fantasy-football-bot.service

# Start the service now
sudo systemctl start fantasy-football-bot.service

# Check status
sudo systemctl status fantasy-football-bot.service
```

You should see: `Active: active (running)`

## 📊 Managing Your Bot

### Check Status
```bash
sudo systemctl status fantasy-football-bot.service
```

### View Logs
```bash
# View recent logs
sudo journalctl -u fantasy-football-bot.service -n 50

# Follow logs in real-time
sudo journalctl -u fantasy-football-bot.service -f

# View logs from today
sudo journalctl -u fantasy-football-bot.service --since today
```

### Stop the Bot
```bash
sudo systemctl stop fantasy-football-bot.service
```

### Start the Bot
```bash
sudo systemctl start fantasy-football-bot.service
```

### Restart the Bot
```bash
sudo systemctl restart fantasy-football-bot.service
```

### Disable Auto-Start
```bash
sudo systemctl disable fantasy-football-bot.service
```

## 🔧 Updating Your Bot

When you want to update your bot code:

```bash
# Stop the bot
sudo systemctl stop fantasy-football-bot.service

# Navigate to project
cd ~/Telegram\ Fantasy\ Football\ Analytics/

# Pull updates (if using git)
git pull

# Or manually copy updated files

# Restart the bot
sudo systemctl start fantasy-football-bot.service

# Check it's running
sudo systemctl status fantasy-football-bot.service
```

## 🌐 Remote Access to Your Raspberry Pi

### Set Static IP (Optional but Recommended)

1. Find your current IP:
```bash
hostname -I
```

2. Edit dhcpcd config:
```bash
sudo nano /etc/dhcpcd.conf
```

3. Add at the end (adjust for your network):
```
interface wlan0  # or eth0 for Ethernet
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8 8.8.4.4
```

4. Reboot:
```bash
sudo reboot
```

### Enable SSH (if not already enabled)

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

Now you can access from Windows using:
```powershell
ssh pi@<raspberry-pi-ip>
```

## 🔒 Security Best Practices

1. **Change default password:**
```bash
passwd
```

2. **Keep system updated:**
```bash
sudo apt update && sudo apt upgrade -y
```

3. **Enable firewall (optional):**
```bash
sudo apt install ufw
sudo ufw allow ssh
sudo ufw enable
```

4. **Never share your .env file!**

## 🛠️ Troubleshooting

### Bot Won't Start

1. Check service status:
```bash
sudo systemctl status fantasy-football-bot.service
```

2. Check logs for errors:
```bash
sudo journalctl -u fantasy-football-bot.service -n 100
```

3. Test manually:
```bash
cd ~/Telegram\ Fantasy\ Football\ Analytics/
python3 run_bot.py
```

### ESPN API Errors

Your ESPN cookies (SWID and S2) expire after ~30 days. To update:

1. Get new cookies from ESPN (see main README)
2. Edit .env file:
```bash
nano .env
```
3. Update ESPN_SWID and ESPN_S2
4. Restart bot:
```bash
sudo systemctl restart fantasy-football-bot.service
```

### Bot Not Auto-Posting

1. Check timezone is correct:
```bash
timedatectl
```

2. Set timezone if needed:
```bash
sudo timedatectl set-timezone America/New_York  # For ET
```

3. Restart bot:
```bash
sudo systemctl restart fantasy-football-bot.service
```

### Memory Issues

If your Pi is running low on memory:

```bash
# Check memory usage
free -h

# Increase swap (if needed)
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile  # Change CONF_SWAPSIZE to 1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

## 📈 Monitoring

### Check Bot is Running
```bash
ps aux | grep python3 | grep run_bot
```

### Check Network Connectivity
```bash
ping -c 4 google.com
```

### Check Disk Space
```bash
df -h
```

### CPU and Memory Usage
```bash
top
# Press 'q' to quit
```

## 🎯 Performance Tips

1. **Use Ethernet instead of Wi-Fi** for more stable connection
2. **Keep your Pi in a well-ventilated area** to prevent overheating
3. **Use a quality power supply** (at least 2.5A for Pi 3/4)
4. **Check logs weekly** to catch any issues early

## 📱 Quick Commands Reference

```bash
# Start bot
sudo systemctl start fantasy-football-bot.service

# Stop bot
sudo systemctl stop fantasy-football-bot.service

# Restart bot
sudo systemctl restart fantasy-football-bot.service

# Check status
sudo systemctl status fantasy-football-bot.service

# View logs
sudo journalctl -u fantasy-football-bot.service -f

# Update and restart
cd ~/Telegram\ Fantasy\ Football\ Analytics/ && git pull && sudo systemctl restart fantasy-football-bot.service
```

## 🎉 Success!

Your bot is now running 24/7 on your Raspberry Pi! It will:
- ✅ Auto-start when the Pi boots
- ✅ Auto-restart if it crashes
- ✅ Post power rankings every Tuesday at 10 AM ET
- ✅ Respond to all commands in your Telegram chat

Enjoy your hands-free Fantasy Football analytics! 🏈📊


