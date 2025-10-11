"""
Auto-posting scheduler for the Fantasy Football Bot
Handles weekly automatic posting of power rankings and other features
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from telegram import Bot
from telegram.ext import Application

from config import TELEGRAM_BOT_TOKEN, AUTO_POST_DAY, AUTO_POST_HOUR, AUTO_POST_MINUTE, ALLOWED_CHAT_IDS
from commands import CommandHandlers
from espn_api import ESPNAPI
from state_manager import StateManager
from analytics import FantasyAnalytics

logger = logging.getLogger(__name__)


class AutoPoster:
    """Handles automatic posting of weekly updates"""
    
    def __init__(self, application: Application):
        self.application = application
        self.bot = application.bot
        self.espn_api = ESPNAPI()
        self.state_manager = StateManager()
        self.analytics = FantasyAnalytics()
        self.command_handlers = CommandHandlers(self.espn_api, self.state_manager, self.analytics)
        
        # Track last posted week to avoid duplicates
        self.last_posted_week = self.state_manager.state.get('last_posted_week', 0)
    
    async def check_and_post_updates(self):
        """Check if it's time to post weekly updates"""
        try:
            current_week = self.espn_api.get_current_week()
            current_day = datetime.now().weekday()
            current_hour = datetime.now().hour
            current_minute = datetime.now().minute
            
            # Check if it's the right day and time
            if (current_day == AUTO_POST_DAY and 
                current_hour == AUTO_POST_HOUR and 
                current_minute == AUTO_POST_MINUTE and
                current_week > self.last_posted_week):
                
                await self.post_weekly_power_rankings()
                self.last_posted_week = current_week
                self.state_manager.state['last_posted_week'] = current_week
                self.state_manager._save_state()
                
                logger.info(f"Posted weekly power rankings for week {current_week}")
                
        except Exception as e:
            logger.error(f"Error in auto-posting check: {e}")
    
    async def post_weekly_power_rankings(self):
        """Post power rankings to all allowed chats"""
        try:
            # Get power rankings message
            power_message = await self.generate_power_rankings_message()
            
            # Post to all allowed chats
            for chat_id in ALLOWED_CHAT_IDS:
                if chat_id.strip():
                    try:
                        await self.bot.send_message(
                            chat_id=chat_id,
                            text=power_message,
                            parse_mode='Markdown'
                        )
                        logger.info(f"Posted power rankings to chat {chat_id}")
                    except Exception as e:
                        logger.error(f"Failed to post to chat {chat_id}: {e}")
                        
        except Exception as e:
            logger.error(f"Error posting weekly power rankings: {e}")
    
    async def generate_power_rankings_message(self) -> str:
        """Generate power rankings message for auto-posting"""
        try:
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            
            # Get previous power rankings for movement arrows
            prev_rankings = self.state_manager.get_power_rankings()
            
            # Calculate power scores for each team
            team_scores = []
            for team in teams:
                team_id = team['id']
                
                # Get team data
                team_data = {
                    'id': team_id,
                    'name': team.get('name', 'Unknown'),
                    'abbrev': team.get('abbrev', 'UNK'),
                    'wins': team.get('record', {}).get('wins', 0),
                    'losses': team.get('record', {}).get('losses', 0),
                    'ties': team.get('record', {}).get('ties', 0),
                    'points_for': team.get('pointsFor', 0),
                    'points_against': team.get('pointsAgainst', 0)
                }
                
                # Get recent scores
                recent_scores = []
                for week in range(max(1, current_week - 3), current_week):
                    matchups = self.espn_api.get_matchups(week)
                    for matchup in matchups:
                        if matchup['home']['teamId'] == team_id:
                            recent_scores.append(matchup['home']['totalPoints'])
                        elif matchup['away']['teamId'] == team_id:
                            recent_scores.append(matchup['away']['totalPoints'])
                
                team_data['recent_scores'] = recent_scores
                team_data['all_scores'] = recent_scores  # Simplified
                
                # Calculate power score
                power_score = self.analytics.calculate_power_score(team_data)
                team_scores.append((team_id, power_score, team_data))
            
            # Sort by power score
            team_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Build power rankings message
            message = f"🏆 **WEEK {current_week - 1} POWER RANKINGS** 🏆\n\n"
            
            for rank, (team_id, score, team_data) in enumerate(team_scores, 1):
                # Movement arrow
                prev_rank = prev_rankings.get(str(team_id), {}).get('rank', rank)
                if prev_rank < rank:
                    arrow = "▼"
                elif prev_rank > rank:
                    arrow = "▲"
                else:
                    arrow = "—"
                
                # Streak
                streak_type, streak_count = self.analytics.calculate_streak(team_data)
                streak_str = f"{streak_type}{streak_count}" if streak_count > 0 else "—"
                
                # Win percentage
                total_games = team_data['wins'] + team_data['losses'] + team_data['ties']
                if total_games > 0:
                    win_pct = (team_data['wins'] + 0.5 * team_data['ties']) / total_games
                    win_pct_str = f"{win_pct:.3f}"
                else:
                    win_pct_str = "0.000"
                
                message += f"{rank}. {arrow} **{team_data['name']}** ({team_data['abbrev']})\n"
                message += f"   📊 {team_data['wins']}-{team_data['losses']}-{team_data['ties']} "
                message += f"({win_pct_str}) | PF: {team_data['points_for']:.1f} | PA: {team_data['points_against']:.1f}\n"
                message += f"   🔥 Streak: {streak_str} | Score: {score:.3f}\n\n"
            
            # Update state with new rankings
            new_rankings = {}
            for rank, (team_id, score, team_data) in enumerate(team_scores, 1):
                new_rankings[str(team_id)] = {
                    'rank': rank,
                    'score': score,
                    'name': team_data['name']
                }
            self.state_manager.update_power_rankings(new_rankings)
            
            message += "🤖 *Auto-posted every Tuesday at 10 AM ET*"
            
            return message
            
        except Exception as e:
            logger.error(f"Error generating power rankings message: {e}")
            return "❌ Error generating power rankings. Please try /power manually."
    
    async def post_weekly_recap(self):
        """Post weekly recap to all allowed chats"""
        try:
            current_week = self.espn_api.get_current_week() - 1
            
            if current_week < 1:
                return
            
            # Get weekly recap
            recap_message = await self.generate_weekly_recap(current_week)
            
            # Post to all allowed chats
            for chat_id in ALLOWED_CHAT_IDS:
                if chat_id.strip():
                    try:
                        await self.bot.send_message(
                            chat_id=chat_id,
                            text=recap_message,
                            parse_mode='Markdown'
                        )
                        logger.info(f"Posted weekly recap to chat {chat_id}")
                    except Exception as e:
                        logger.error(f"Failed to post recap to chat {chat_id}: {e}")
                        
        except Exception as e:
            logger.error(f"Error posting weekly recap: {e}")
    
    async def generate_weekly_recap(self, week: int) -> str:
        """Generate weekly recap message"""
        try:
            # Get matchups for the week
            matchups = self.espn_api.get_matchups(week)
            teams = {team['id']: team for team in self.espn_api.get_teams()}
            
            if not matchups:
                return f"No matchups found for week {week}"
            
            # Analyze matchups
            all_scores = []
            game_results = []
            
            for matchup in matchups:
                home_team = teams[matchup['home']['teamId']]
                away_team = teams[matchup['away']['teamId']]
                home_score = matchup['home']['totalPoints']
                away_score = matchup['away']['totalPoints']
                
                all_scores.extend([home_score, away_score])
                
                # Determine winner and margin
                if home_score > away_score:
                    winner = home_team['name']
                    loser = away_team['name']
                    margin = home_score - away_score
                elif away_score > home_score:
                    winner = away_team['name']
                    loser = home_team['name']
                    margin = away_score - home_score
                else:
                    winner = "Tie"
                    loser = "Tie"
                    margin = 0
                
                game_results.append({
                    'home_team': home_team['name'],
                    'away_team': away_team['name'],
                    'home_score': home_score,
                    'away_score': away_score,
                    'winner': winner,
                    'margin': margin
                })
            
            # Find highlights
            high_score = max(all_scores)
            low_score = min(all_scores)
            
            closest_game = min(game_results, key=lambda x: abs(x['margin']) if x['margin'] > 0 else float('inf'))
            biggest_blowout = max(game_results, key=lambda x: x['margin'])
            
            # Build recap message
            message = f"📰 **WEEK {week} RECAP** 📰\n\n"
            message += f"🔥 **High Score:** {high_score:.1f} points\n"
            message += f"❄️ **Low Score:** {low_score:.1f} points\n"
            message += f"⚡ **Closest Game:** {closest_game['home_team']} vs {closest_game['away_team']} "
            message += f"({closest_game['margin']:.1f} pt margin)\n"
            message += f"💥 **Biggest Blowout:** {biggest_blowout['winner']} by {biggest_blowout['margin']:.1f} points\n\n"
            
            message += "**All Games:**\n"
            for game in game_results:
                message += f"• {game['home_team']} {game['home_score']:.1f} - {game['away_score']:.1f} {game['away_team']}\n"
            
            return message
            
        except Exception as e:
            logger.error(f"Error generating weekly recap: {e}")
            return f"❌ Error generating week {week} recap."
    
    async def start_scheduler(self):
        """Start the auto-posting scheduler"""
        logger.info("Starting auto-posting scheduler...")
        
        while True:
            try:
                await self.check_and_post_updates()
                # Check every minute
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(60)  # Wait a minute before retrying




