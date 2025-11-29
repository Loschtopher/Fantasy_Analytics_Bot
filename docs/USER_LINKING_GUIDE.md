# 👥 User-Team Linking Guide

Your bot now has user-team linking! This lets you connect Telegram users to their ESPN Fantasy teams.

---

## 🎯 How It Works

The bot **automatically detects users** when they use ANY command. You don't need to find their usernames manually!

---

## 📋 Setup Steps (One-Time)

### Step 1: Get Everyone to Send a Command

Ask your league members to send **any command** to the bot, like:
- `/help`
- `/whoami`
- `/power`

This lets the bot detect them automatically!

### Step 2: See Detected Users

You (as admin) run:
```
/users
```

This shows all detected users with their:
- Display name (@username or first name)
- User ID
- Whether they're linked to a team

### Step 3: See Team List

Run:
```
/teams
```

This shows all 12 ESPN teams with their numbers (1-12)

### Step 4: Link Users to Teams

For each user, run:
```
/linkuser <user_id> <team_number>
```

**Example:**
```
/linkuser 1375980805 5
```

This links user ID `1375980805` to team #5

---

## 🎮 User Commands (After Linking)

Once linked, users can run:

### `/whoami`
Shows their Telegram info and linked team
```
👤 Your Info
Name: Topher
Username: @topher
User ID: 1375980805

⭐ Linked Team:
Team Awesome

Use /myteam to see your stats!
```

### `/myteam`
Shows personalized team stats
```
⭐ YOUR TEAM ⭐

🏈 Team Awesome

📊 Record: 4-1
📈 Win %: 80.0%

⚡ Points For: 612.5
🛡️ Points Against: 548.2
📊 Avg PPG: 122.5

💡 Use /power to see where you rank!
```

---

## 🔧 Admin Commands

### `/users`
See all detected users and their link status

### `/teams`
See all ESPN teams with numbers for linking

### `/linkuser <user_id> <team_number>`
Link a user to a team

### `/unlink <user_id>`
Remove a user's team link

---

## 💡 Tips

1. **Have everyone send `/whoami` first** - This detects them all at once
2. **Use `/teams` to see the team list** before linking
3. **Users can check `/whoami` anytime** to see if they're linked
4. **Linking is permanent** until you unlink them

---

## 📱 Quick Setup Example

**In your group chat:**

1. **You say:** "Everyone send `/whoami` to the bot!"
2. **Everyone does it**
3. **You run:** `/users` (see who's detected)
4. **You run:** `/teams` (see team list)
5. **You link each person:**
   ```
   /linkuser 123456 1
   /linkuser 789012 2
   /linkuser 345678 3
   ```
   (etc. for all 12 teams)

6. **Everyone can now use `/myteam`!**

---

## 🎉 Benefits

- ✅ Personalized stats with `/myteam`
- ✅ Users can quickly check their own team
- ✅ Future features: auto-tagging in recaps
- ✅ Future features: `/mystats` for personalized analytics
- ✅ No need to know everyone's usernames manually

---

## 🚀 Try It Now!

1. Send `/whoami` in Telegram
2. You'll see your Telegram info
3. Send `/teams` to see all 12 teams
4. Link yourself to your team!

**Example:**
```
/teams          (see list)
/linkuser 1375980805 3    (link yourself to team #3)
/myteam         (see your stats!)
```

---

**Your bot is ready to link users to teams!** 🏈👥







