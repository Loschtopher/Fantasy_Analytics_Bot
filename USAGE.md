# Fantasy Football Bot Usage Guide

## Quick Start

1. **Set up your environment** (see README.md for detailed setup)
2. **Run the bot**: `python run_bot.py`
3. **Add bot to your group chat**
4. **Start using commands!**

## Command Reference

### 🏆 Power Rankings
```
/power
```
Shows current power rankings with:
- Weighted power scores
- Win/loss records and percentages
- Points for/against
- Current streaks
- Week-over-week movement (▲▼)

**Example Output:**
```
🏆 POWER RANKINGS 🏆

1. ▲ Team Alpha (ALP)
   📊 8-2-0 (0.800) | PF: 1250.5 | PA: 1100.2
   🔥 Streak: W3 | Score: 0.847

2. ▼ Team Beta (BET)
   📊 7-3-0 (0.700) | PF: 1200.0 | PA: 1150.0
   🔥 Streak: L1 | Score: 0.723
```

### 📰 Weekly Recap
```
/recap [week]
```
- `week` (optional): Specific week number, defaults to last completed week

Shows weekly highlights:
- High and low scores
- Closest game
- Biggest blowout
- All game results

**Example Output:**
```
📰 WEEK 8 RECAP 📰

🔥 High Score: 145.2 points
❄️ Low Score: 89.4 points
⚡ Closest Game: Team Alpha vs Team Beta (2.1 pt margin)
💥 Biggest Blowout: Team Gamma by 35.7 points

All Games:
• Team Alpha 125.4 - 123.3 Team Beta
• Team Gamma 145.2 - 109.5 Team Delta
```

### 🍀 Luck Analysis
```
/luck
```
Shows Pythagorean expectation vs actual wins:
- Expected wins based on points for/against
- Actual wins comparison
- Luck rating (lucky/cursed/neutral)

**Example Output:**
```
🍀 LUCK ANALYSIS 🍀

Pythagorean expectation vs actual wins

Team Alpha (ALP)
📊 8-2-0 | Expected: 6.8 | Actual: 8.0
🎯 Luck: +1.2 🍀 Lucky

Team Beta (BET)
📊 3-7-0 | Expected: 5.2 | Actual: 3.0
🎯 Luck: -2.2 😈 Cursed
```

### 🎯 All-Play Records
```
/all [week]
```
- `week` (optional): Specific week number, defaults to season

Shows what each team's record would be if they played everyone each week.

**Example Output:**
```
🎯 SEASON ALL-PLAY 🎯

What each team's record would be if they played everyone each week

Team Alpha (ALP)
📊 45-23 (0.662)

Team Beta (BET)
📊 38-30 (0.559)
```

### 💥 Boom/Bust Analysis
```
/boom
```
Shows consistency metrics:
- Ceiling (P80) - 80th percentile performance
- Floor (P20) - 20th percentile performance
- Spread - Boom-bust range
- Consistency score

**Example Output:**
```
💥 BOOM/BUST ANALYSIS 💥

P80 = Ceiling, P20 = Floor, Spread = Boom-Bust Range

Team Alpha (ALP)
🚀 Ceiling (P80): 145.2
📉 Floor (P20): 98.7
📏 Spread: 46.5
🎯 Consistency: 0.023
```

### ⚡ ELO Ratings
```
/elo
```
Shows head-to-head strength ratings based on ELO system.

**Example Output:**
```
⚡ ELO RATINGS ⚡

Head-to-head strength ratings

1. Team Alpha (ALP)
   🎯 ELO: 1687

2. Team Beta (BET)
   🎯 ELO: 1543
```

## Advanced Features (Coming Soon)

### 😭 Start/Sit Regret
```
/regret [week]
```
Will show:
- Optimal lineup points vs actual points
- Bench efficiency percentage
- Start/sit decision analysis

### 🎲 Playoff Odds
```
/odds [@user]
```
Will show:
- Monte Carlo playoff simulations
- Championship probability
- Remaining schedule analysis

### 💪 Strength of Schedule
```
/sos
```
Will show:
- Schedule difficulty to date
- Rest-of-season strength
- ELO-based opponent analysis

### 🔥 Heat Map
```
/heat
```
Will show:
- Weekly z-score trends
- Hot and cold performance streaks
- Visual consistency tracking

### ⚔️ Rivalry Tracker
```
/rivals [@user]
```
Will show:
- Head-to-head records
- Point differentials
- Win/loss streaks between teams

## Tips for Best Results

### 1. **Use the bot regularly**
- Run `/power` weekly to see rankings changes
- Use `/recap` to discuss weekly highlights
- Check `/luck` to see who's getting lucky/unlucky

### 2. **Share insights with your league**
- Post power rankings after each week
- Discuss luck analysis - who's due for regression?
- Use all-play records to settle "easy schedule" debates

### 3. **Customize for your league**
- Adjust power ranking weights in `config.py`
- Modify auto-posting schedule
- Add custom analysis features

### 4. **Troubleshooting**
- If commands fail, check ESPN credentials
- Verify bot has proper permissions in chat
- Check logs in `bot.log` for errors

## Example Workflow

**Tuesday Morning (Auto-post):**
- Bot automatically posts power rankings at 10 AM ET

**After Games:**
- Run `/recap` to see weekly highlights
- Use `/luck` to discuss who got lucky/unlucky

**Mid-week Analysis:**
- Check `/boom` for consistency analysis
- Use `/elo` to see head-to-head strength
- Run `/all` to see all-play standings

**Playoff Push:**
- Use `/odds` for playoff probability
- Check `/sos` for remaining schedule strength
- Review `/rivals` for key matchups

## Getting Help

- Run `/help` for command list
- Check `README.md` for setup issues
- Review logs in `bot.log` for errors
- Test setup with `python test_setup.py`


