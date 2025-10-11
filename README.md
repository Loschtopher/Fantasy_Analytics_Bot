# Telegram Fantasy Football Analytics Bot

A powerful Telegram bot that provides advanced analytics for your ESPN Fantasy Football league, going far beyond what the ESPN app offers.

## Features

### 🏆 Power Rankings (`/power`)
- **Weighted power scores** based on win%, recent form, efficiency, and schedule strength
- **Week-over-week movement** with ▲▼ arrows showing ranking changes
- **Current win/loss streaks** and team momentum
- **Auto-posted every Tuesday** at 10 AM ET

### 📰 Weekly Recap (`/recap [week]`)
- **High and low scores** for the week with team names
- **Closest game** with margin of victory
- **Biggest blowout** showing largest point differential
- **Complete game results** with scores for all matchups

### 🍀 Luck Analysis (`/luck`)
- **Pythagorean expectation** vs actual wins using points for/against
- **Luck ratings** identifying lucky and cursed teams
- **Expected vs actual performance** with statistical analysis
- **Regression indicators** for future performance

### 🎯 All-Play Records (`/all [week]`)
- **Season all-play**: What each team's record would be if they played everyone each week
- **Weekly all-play**: Single week performance against all teams
- **True team strength** independent of schedule luck

### 💥 Boom/Bust Analysis (`/boom`)
- **Ceiling (P80) and floor (P20)** performance metrics
- **Boom-bust spread** showing consistency vs variance
- **Consistency ratings** identifying reliable vs volatile teams
- **Team categorization** (High Variance, Consistent, etc.)

### 😭 Start/Sit Regret (`/regret [week]`)
- **Optimal lineup analysis** vs actual lineup decisions
- **Bench efficiency percentage** showing missed opportunities
- **Start/sit regret metrics** with point differentials
- **Weekly decision analysis** for lineup optimization

### ⚡ ELO Ratings (`/elo`)
- **Head-to-head strength ratings** using ELO system
- **Dynamic rating updates** based on matchup results
- **Competitive balance analysis** across the league
- **Strength-based rankings** independent of schedule

### 🎲 Playoff Odds (`/odds`)
- **Monte Carlo simulations** (5,000 iterations) of remaining schedule
- **Playoff probability** based on scoring distributions
- **Championship odds** with realistic projections
- **Remaining schedule analysis** for playoff push

### 💪 Strength of Schedule (`/sos`)
- **Schedule difficulty to date** with opponent strength ratings
- **SOS rankings** showing easiest/hardest schedules
- **Opponent scoring averages** vs league average
- **Schedule impact analysis** on team records

### 🔥 Heat Map (`/heat`)
- **Weekly z-score trends** showing performance consistency
- **Hot and cold streaks** with visual indicators (🔥❄️)
- **Performance categorization** (Exceptional, Great, Good, Average, Poor)
- **Trend analysis** with consistency metrics

### ⚔️ Rivalry Tracker (`/rivals`)
- **Head-to-head records** between all team pairs
- **Point differentials** and win/loss streaks
- **Rivalry intensity ratings** based on games played and competitiveness
- **Top rivalries** ranked by matchup frequency and closeness

## Setup

### Prerequisites
- Python 3.8+
- Telegram Bot Token (from @BotFather)
- ESPN Fantasy Football League access
- ESPN SWID and S2 cookies

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd telegram-fantasy-football-analytics
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ALLOWED_CHAT_IDS=chat_id_1,chat_id_2
   ESPN_LEAGUE_ID=your_league_id
   ESPN_SWID=your_swid_cookie
   ESPN_S2=your_s2_cookie
   ```

4. **Get ESPN Credentials**
   
   **League ID**: Found in your ESPN league URL
   - URL format: `https://fantasy.espn.com/football/league?leagueId=123456`
   - League ID is the number at the end
   
   **SWID and S2 Cookies**:
   1. Log into your ESPN Fantasy Football league in your browser
   2. Open Developer Tools (F12)
   3. Go to Application/Storage → Cookies
   4. Find `SWID` and `espn_s2` cookies
   5. Copy their values

5. **Get Telegram Bot Token**
   1. Message @BotFather on Telegram
   2. Use `/newbot` command
   3. Follow instructions to create your bot
   4. Copy the bot token

6. **Get Chat IDs**
   1. Add your bot to your group chat
   2. Send a message in the chat
   3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   4. Find the chat ID in the response

### Running the Bot

```bash
python bot.py
```

The bot will start and begin responding to commands in your configured chat(s).

## Configuration

### Auto-Posting
The bot can automatically post power rankings every Tuesday at 10 AM ET. Configure in `config.py`:

```python
AUTO_POST_DAY = 1  # Tuesday (0=Monday, 1=Tuesday, etc.)
AUTO_POST_HOUR = 10  # 10 AM ET
AUTO_POST_MINUTE = 0
```

### Power Rankings Weights
Customize the power rankings calculation in `config.py`:

```python
POWER_RANKINGS_WEIGHTS = {
    'win_percentage': 0.4,
    'recent_form': 0.25,
    'efficiency': 0.2,
    'schedule_strength': 0.15
}
```

## Usage

### Basic Commands
- `/power` - Get current power rankings
- `/recap` - Weekly recap (defaults to last completed week)
- `/help` - Show all available commands

### Advanced Commands
- `/recap 5` - Recap for week 5
- `/all 8` - All-play records for week 8
- `/odds @username` - Playoff odds for specific user

### Command Examples

```
/power
🏆 POWER RANKINGS 🏆

1. ▲ Team Alpha (ALP)
   📊 8-2-0 (0.800) | PF: 1250.5 | PA: 1100.2
   🔥 Streak: W3 | Score: 0.847

2. ▼ Team Beta (BET)
   📊 7-3-0 (0.700) | PF: 1200.0 | PA: 1150.0
   🔥 Streak: L1 | Score: 0.723
```

## File Structure

```
├── bot.py              # Main bot application
├── commands.py         # Command handlers
├── espn_api.py         # ESPN API client
├── analytics.py        # Analytics calculations
├── state_manager.py    # State persistence
├── config.py          # Configuration settings
├── requirements.txt    # Python dependencies
├── env.example        # Environment variables template
├── state.json         # Persistent state (created at runtime)
└── README.md          # This file
```

## Data Storage

The bot stores persistent data in `state.json`:
- Power rankings history (for ▲▼ movement)
- ELO ratings
- Weekly scores and projections
- Cached team data

## Troubleshooting

### Common Issues

1. **"Error generating power rankings"**
   - Check ESPN credentials (SWID, S2, League ID)
   - Verify league is active and accessible

2. **Bot not responding**
   - Check Telegram bot token
   - Verify chat IDs are correct
   - Ensure bot is added to the chat

3. **"No matchups found"**
   - League may not have started yet
   - Check if week number is valid

### Getting Help

1. Check the logs in `bot.log`
2. Verify all environment variables are set correctly
3. Test ESPN API access manually
4. Check Telegram bot permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This bot is for personal use only. Please respect ESPN's terms of service and rate limits. The bot uses ESPN's private API which may change without notice.
