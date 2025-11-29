# 🎰 REAL SPORTSBOOK ODDS INTEGRATION

## ✅ What I Just Built

I've created **The Odds API** integration to fetch **REAL sportsbook odds** for player touchdown props from DraftKings, FanDuel, BetMGM, and more!

---

## 📁 New Files Created

### `odds_api.py`
A complete API client that:
- ✅ Fetches real-time anytime TD scorer odds
- ✅ Compares odds across multiple sportsbooks
- ✅ Converts American odds to probabilities
- ✅ Finds best value bets
- ✅ Identifies longshot opportunities

---

## 🔑 **STEP 1: Get Your FREE API Key**

1. Go to: **https://the-odds-api.com/**
2. Click "**Get API Key**" (top right)
3. Sign up with your email
4. Verify your email
5. Copy your API key

**Free Tier:**
- ✅ **500 requests/month**
- ✅ Real-time odds
- ✅ Multiple sportsbooks
- ✅ No credit card required

---

## 🔧 **STEP 2: Add API Key to `.env`**

Open your `.env` file and add:

```bash
# The Odds API Configuration
ODDS_API_KEY=your_actual_api_key_here
```

**Example:**
```bash
ODDS_API_KEY=abc123def456ghi789jkl012mno345pqr678
```

---

## 🎯 **STEP 3: Commands Will Automatically Use Real Odds!**

Once you add the API key, the parlay commands will:

### **Before (Synthetic Odds):**
```
1. Jahmyr Gibbs (RB)
   Detroit Lions | 65% 🔒 Lock
```

### **After (Real Odds):**
```
1. Jahmyr Gibbs (RB)
   DraftKings: -150 (60.0%) 🔒 Lock
   FanDuel: -140 (58.3%)
   BetMGM: -155 (60.8%)
```

---

## 💡 **How It Works**

### `/parlay` - Safe TD Parlay
- Fetches odds from all major sportsbooks
- Finds the **3 players with highest TD probability**
- Shows **best odds** for each player
- Calculates **real parlay payout**

**Example:**
```
🏈 SAFE TD PARLAY - REAL ODDS 🏈

💰 Live sportsbook odds from DraftKings, FanDuel, BetMGM
Showing the 3 most likely touchdown scorers

3-LEG ANYTIME TD PARLAY:

1. Christian McCaffrey
   DraftKings: -180 (64.3%) 🔒 Lock

2. Tyreek Hill
   FanDuel: -120 (54.5%) ✅ Strong

3. Travis Kelce
   BetMGM: +110 (47.6%) ⚖️ Solid

📊 Combined Probability: 16.7%
💰 Parlay Payout: +498

✅ Recommendation: Good value for a 3-leg parlay!
```

### `/yolo` - Longshot TD Parlay
- Finds **high-payout underdogs** (+200 odds or better)
- Shows **biggest longshots** with TD potential
- Massive payout potential

**Example:**
```
🎰 YOLO TD PARLAY - REAL ODDS 🎰

💎 Longshot touchdown scorers for BIG payouts
High-risk, high-reward picks

3-LEG LONGSHOT PARLAY:

1. Rome Odunze (WR)
   DraftKings: +450 (18.2%) 💎 Longshot

2. Dalton Kincaid (TE)
   FanDuel: +380 (20.8%) 💎 Longshot

3. Jaylen Warren (RB)
   BetMGM: +320 (23.8%) 💎 Longshot

📊 Combined Probability: 0.9%
💰 Parlay Payout: +10,832

🚀 YOLO SPECIAL - Hit this and you're RICH!
```

---

## 🛡️ **Fallback System**

If the API key is missing or you hit the request limit:
- Commands will show a message: "⚠️ Using estimated odds (real odds unavailable)"
- Commands still work, just with synthetic odds
- No errors or crashes!

---

## 📊 **API Usage Tips**

### Managing Your 500 Requests/Month:
- Each `/parlay` command = **~6-10 requests** (fetches multiple games)
- Each `/yolo` command = **~6-10 requests**
- **Budget:** ~50-80 parlay checks per month

### Best Practices:
1. ✅ Use commands **Thursday-Sunday** (when games are happening)
2. ✅ Check odds **once per day** before games
3. ✅ Avoid spamming commands (you'll hit the limit fast!)
4. ❌ Don't use during offseason (no games = no odds)

---

## 🚀 **Ready to Test?**

Once you add your API key to `.env`:

1. Restart the bot
2. Type `/parlay` in Telegram
3. You should see **REAL SPORTSBOOK ODDS**! 🎉

---

## 🆘 **Troubleshooting**

### "Odds API unavailable"
- ✅ Check your API key in `.env`
- ✅ Make sure you have requests left (500/month limit)
- ✅ Check if it's gameweek (odds only available during NFL season)

### "Error fetching odds"
- ✅ Check your internet connection
- ✅ Verify API key is correct
- ✅ Try again in a few minutes

### "No games available"
- ✅ It's probably offseason or bye week
- ✅ Odds only available when NFL games are scheduled

---

## 🎯 **What's Next?**

Once you have real odds working:
1. Share the parlays with your league! 🏈
2. Track which picks hit 🎯
3. Brag when you nail a longshot 💰

**The bot will automatically use real odds when available, and fall back to synthetic odds if not!**







