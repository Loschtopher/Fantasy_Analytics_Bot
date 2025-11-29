"""
Command Handlers for Telegram Fantasy Football Analytics Bot
Implements all the bot commands with rich formatting
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from espn_api import ESPNAPI
from state_manager import StateManager
from analytics import FantasyAnalytics


class CommandHandlers:
    """Handles all bot commands"""
    
    def __init__(self, espn_api: ESPNAPI, state_manager: StateManager, analytics: FantasyAnalytics):
        self.espn_api = espn_api
        self.state_manager = state_manager
        self.analytics = analytics
    
    async def power_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /power command - Power Rankings"""
        try:
            # Get current teams and matchups
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            
            # Get previous power rankings for movement arrows
            prev_rankings = self.state_manager.get_power_rankings()
            
            # First pass: collect all team data including opponent scores
            all_teams_data = {}
            for team in teams:
                team_id = team['id']
                record = team.get('record', {}).get('overall', {})
                
                # Get all scores and opponent scores for the season
                all_scores = []
                opponent_scores = []
                recent_scores = []
                recent_results = []
                
                for week in range(1, current_week):
                    matchups = self.espn_api.get_matchups(week)
                    for matchup in matchups:
                        if matchup['home']['teamId'] == team_id:
                            score = matchup['home']['totalPoints']
                            opp_score = matchup['away']['totalPoints']
                            all_scores.append(score)
                            opponent_scores.append(opp_score)
                            
                            # Track recent for last 3 weeks
                            if week >= current_week - 3:
                                recent_scores.append(score)
                                if score > opp_score:
                                    recent_results.append('W')
                                elif score < opp_score:
                                    recent_results.append('L')
                                else:
                                    recent_results.append('T')
                            break
                        elif matchup['away']['teamId'] == team_id:
                            score = matchup['away']['totalPoints']
                            opp_score = matchup['home']['totalPoints']
                            all_scores.append(score)
                            opponent_scores.append(opp_score)
                            
                            # Track recent for last 3 weeks
                            if week >= current_week - 3:
                                recent_scores.append(score)
                                if score > opp_score:
                                    recent_results.append('W')
                                elif score < opp_score:
                                    recent_results.append('L')
                                else:
                                    recent_results.append('T')
                            break
                
                all_teams_data[team_id] = {
                    'all_scores': all_scores,
                    'opponent_scores': opponent_scores,
                    'recent_results': recent_results,
                    'name': team.get('name', 'Unknown'),
                    'abbrev': team.get('abbrev', 'UNK')
                }
            
            # Second pass: calculate power scores with real SOS
            team_scores = []
            for team in teams:
                team_id = team['id']
                record = team.get('record', {}).get('overall', {})
                
                # Calculate SOS for this team
                sos_metrics = self.analytics.calculate_strength_of_schedule(
                    all_teams_data[team_id], 
                    all_teams_data, 
                    current_week - 1
                )
                
                team_data = {
                    'id': team_id,
                    'name': team.get('name', 'Unknown'),
                    'abbrev': team.get('abbrev', 'UNK'),
                    'wins': record.get('wins', 0),
                    'losses': record.get('losses', 0),
                    'ties': record.get('ties', 0),
                    'points_for': record.get('pointsFor', 0),
                    'points_against': record.get('pointsAgainst', 0),
                    'recent_scores': all_teams_data[team_id]['all_scores'][-3:] if len(all_teams_data[team_id]['all_scores']) >= 3 else all_teams_data[team_id]['all_scores'],
                    'all_scores': all_teams_data[team_id]['all_scores'],
                    'recent_results': all_teams_data[team_id]['recent_results'],
                    'schedule_strength': abs(sos_metrics['sos_rating'])  # Use real SOS from ESPN data
                }
                
                # Calculate power score
                power_score = self.analytics.calculate_power_score(team_data)
                team_scores.append((team_id, power_score, team_data))
            
            # Sort by power score
            team_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Build power rankings message
            message = "🏆 **POWER RANKINGS** 🏆\n\n"
            message += "📈 *Rankings based on: Win%, Recent Form, Scoring Efficiency, Schedule Strength*\n"
            message += "▲ = Moved up | ▼ = Moved down | — = No change\n\n"
            
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
                
                # Calculate Points Per Game
                ppg = team_data['points_for'] / total_games if total_games > 0 else 0
                
                message += f"{rank}. {arrow} **{team_data['name']}** ({team_data['abbrev']})\n"
                message += f"   📊 {team_data['wins']}-{team_data['losses']}-{team_data['ties']} "
                message += f"({win_pct_str}) | PF: {team_data['points_for']:.1f} | PA: {team_data['points_against']:.1f}\n"
                message += f"   🔥 Streak: {streak_str} | PPG: {ppg:.1f}\n\n"
            
            # Update state with new rankings
            new_rankings = {}
            for rank, (team_id, score, team_data) in enumerate(team_scores, 1):
                new_rankings[str(team_id)] = {
                    'rank': rank,
                    'score': score,
                    'name': team_data['name']
                }
            self.state_manager.update_power_rankings(new_rankings)
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Error generating power rankings: {str(e)}")
    
    async def recap_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /recap command - Weekly Recap"""
        try:
            # Get week from command args, default to last completed week
            week = None
            if context.args:
                try:
                    week = int(context.args[0])
                except ValueError:
                    await update.message.reply_text("Invalid week number. Usage: /recap [week]")
                    return
            
            if not week:
                week = self.espn_api.get_current_week() - 1  # Last completed week
            
            if week < 1:
                await update.message.reply_text("No completed weeks yet!")
                return
            
            # Get matchups for the week
            matchups = self.espn_api.get_matchups(week)
            teams = {team['id']: team for team in self.espn_api.get_teams()}
            
            if not matchups:
                await update.message.reply_text(f"No matchups found for week {week}")
                return
            
            # Analyze matchups
            all_scores = []
            game_results = []
            score_to_team = {}  # Track which team scored what
            
            for matchup in matchups:
                home_team = teams[matchup['home']['teamId']]
                away_team = teams[matchup['away']['teamId']]
                home_score = matchup['home']['totalPoints']
                away_score = matchup['away']['totalPoints']
                
                all_scores.extend([home_score, away_score])
                score_to_team[home_score] = home_team['name']
                score_to_team[away_score] = away_team['name']
                
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
            high_scorer = score_to_team.get(high_score, 'Unknown')
            low_scorer = score_to_team.get(low_score, 'Unknown')
            
            closest_game = min(game_results, key=lambda x: abs(x['margin']) if x['margin'] > 0 else float('inf'))
            biggest_blowout = max(game_results, key=lambda x: x['margin'])
            
            # Build recap message
            message = f"📰 **WEEK {week} RECAP** 📰\n\n"
            message += f"🔥 **High Score:** {high_scorer} ({high_score:.1f} pts)\n"
            message += f"❄️ **Low Score:** {low_scorer} ({low_score:.1f} pts)\n"
            message += f"⚡ **Closest Game:** {closest_game['home_team']} vs {closest_game['away_team']} "
            message += f"({closest_game['margin']:.1f} pt margin)\n"
            message += f"💥 **Biggest Blowout:** {biggest_blowout['winner']} by {biggest_blowout['margin']:.1f} points\n\n"
            
            message += "**All Games:**\n"
            for game in game_results:
                message += f"• {game['home_team']} {game['home_score']:.1f} - {game['away_score']:.1f} {game['away_team']}\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Error generating recap: {str(e)}")
    
    async def season_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /season command - Season Highlights"""
        try:
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            
            if current_week <= 1:
                await update.message.reply_text("No completed weeks yet!")
                return
            
            # Track season-long stats
            all_time_scores = []
            team_high_scores = {}
            team_low_scores = {}
            closest_games = []
            biggest_blowouts = []
            
            # Go through all weeks
            for week in range(1, current_week):
                matchups = self.espn_api.get_matchups(week)
                
                for matchup in matchups:
                    home_id = matchup['home']['teamId']
                    away_id = matchup['away']['teamId']
                    home_score = matchup['home']['totalPoints']
                    away_score = matchup['away']['totalPoints']
                    
                    home_team = next((t for t in teams if t['id'] == home_id), None)
                    away_team = next((t for t in teams if t['id'] == away_id), None)
                    
                    if not home_team or not away_team:
                        continue
                    
                    home_name = home_team.get('name', 'Unknown')
                    away_name = away_team.get('name', 'Unknown')
                    
                    # Track all scores
                    all_time_scores.append({
                        'team': home_name,
                        'score': home_score,
                        'week': week
                    })
                    all_time_scores.append({
                        'team': away_name,
                        'score': away_score,
                        'week': week
                    })
                    
                    # Track team highs/lows
                    if home_name not in team_high_scores or home_score > team_high_scores[home_name]['score']:
                        team_high_scores[home_name] = {'score': home_score, 'week': week}
                    if home_name not in team_low_scores or home_score < team_low_scores[home_name]['score']:
                        team_low_scores[home_name] = {'score': home_score, 'week': week}
                    
                    if away_name not in team_high_scores or away_score > team_high_scores[away_name]['score']:
                        team_high_scores[away_name] = {'score': away_score, 'week': week}
                    if away_name not in team_low_scores or away_score < team_low_scores[away_name]['score']:
                        team_low_scores[away_name] = {'score': away_score, 'week': week}
                    
                    # Track close games and blowouts
                    margin = abs(home_score - away_score)
                    winner = home_name if home_score > away_score else away_name
                    
                    if margin > 0:
                        closest_games.append({
                            'teams': f"{home_name} vs {away_name}",
                            'margin': margin,
                            'week': week
                        })
                        biggest_blowouts.append({
                            'winner': winner,
                            'margin': margin,
                            'week': week,
                            'matchup': f"{home_name} vs {away_name}"
                        })
            
            # Find season highlights
            highest_score = max(all_time_scores, key=lambda x: x['score'])
            lowest_score = min(all_time_scores, key=lambda x: x['score'])
            closest = min(closest_games, key=lambda x: x['margin'])
            biggest_blowout = max(biggest_blowouts, key=lambda x: x['margin'])
            
            # Build season recap message
            message = "🏆 **SEASON HIGHLIGHTS** 🏆\n\n"
            message += "📊 *Top moments from the entire season*\n\n"
            
            message += f"🔥 **Highest Score of Season:**\n"
            message += f"   {highest_score['team']}: {highest_score['score']:.1f} pts (Week {highest_score['week']})\n\n"
            
            message += f"❄️ **Lowest Score of Season:**\n"
            message += f"   {lowest_score['team']}: {lowest_score['score']:.1f} pts (Week {lowest_score['week']})\n\n"
            
            message += f"⚡ **Closest Game:**\n"
            message += f"   {closest['teams']} - {closest['margin']:.1f} pt margin (Week {closest['week']})\n\n"
            
            message += f"💥 **Biggest Blowout:**\n"
            message += f"   {biggest_blowout['winner']} won by {biggest_blowout['margin']:.1f} pts (Week {biggest_blowout['week']})\n\n"
            
            # Show league scoring stats
            avg_score = sum(s['score'] for s in all_time_scores) / len(all_time_scores) if all_time_scores else 0
            message += f"📈 **League Avg:** {avg_score:.1f} pts/game\n"
            message += f"📊 **Total Games:** {len(all_time_scores)} performances through Week {current_week - 1}"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in season_command: {error_details}")
            await update.message.reply_text(f"Error generating season highlights: {str(e)}\nCheck console for details.")
    
    async def parlay_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /parlay command - Safe Touchdown Parlay"""
        try:
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            
            # Get roster data for all teams to find TD-likely players
            message = f"🏈 **SAFE TD PARLAY - WEEK {current_week}** 🏈\n\n"
            message += "🎯 *Players most likely to score touchdowns*\n"
            message += "Based on position, usage, and team scoring\n\n"
            
            td_candidates = []
            
            # Get each team's roster
            for team in teams:
                team_id = team['id']
                team_name = team.get('name', 'Unknown')
                
                # Get roster
                endpoint = f"seasons/{self.espn_api.season}/segments/0/leagues/{self.espn_api.league_id}"
                params = {
                    'view': ['mRoster'],
                    'scoringPeriodId': current_week
                }
                
                try:
                    week_data = self.espn_api._make_request(endpoint, params)
                    
                    if 'teams' not in week_data:
                        continue
                    
                    team_data = next((t for t in week_data['teams'] if t['id'] == team_id), None)
                    if not team_data or 'roster' not in team_data:
                        continue
                    
                    roster = team_data['roster']
                    if 'entries' not in roster:
                        continue
                    
                    # Find RBs and top WRs (most likely TD scorers)
                    for entry in roster['entries']:
                        slot_id = entry.get('lineupSlotId')
                        player_entry = entry.get('playerPoolEntry', {})
                        player_info = player_entry.get('player', {})
                        
                        player_name = player_info.get('fullName', 'Unknown')
                        position_id = player_info.get('defaultPositionId', 0)
                        
                        # Position IDs: 2=RB, 4=WR, 6=TE
                        # Lineup Slots: 20=Bench, 21=IR, others=Starting
                        
                        # Only include starters
                        if slot_id in [20, 21]:  # Skip bench and IR
                            continue
                        
                        # Only RBs, WRs, and TEs
                        if position_id not in [2, 4, 6]:
                            continue
                        
                        position_name = {2: 'RB', 4: 'WR', 6: 'TE'}.get(position_id, 'FLEX')
                        
                        # TD Probability (RBs highest, then TEs, then WRs)
                        if position_id == 2:  # RB
                            td_prob = 65  # RBs score most TDs
                        elif position_id == 6:  # TE
                            td_prob = 45  # TEs decent TD chance
                        else:  # WR
                            td_prob = 50  # WRs good TD chance
                        
                        td_candidates.append({
                            'name': player_name,
                            'position': position_name,
                            'team': team_name,
                            'td_prob': td_prob
                        })
                
                except Exception as e:
                    print(f"Error getting roster for team {team_id}: {e}")
                    continue
            
            # Sort by TD probability
            td_candidates.sort(key=lambda x: x['td_prob'], reverse=True)
            
            if len(td_candidates) < 3:
                await update.message.reply_text("⏳ Not enough player data available for parlays yet!")
                return
            
            # Build 3-leg safe parlay (top TD threats)
            message += "**3-LEG ANYTIME TD PARLAY:**\n"
            combined_prob = 1.0
            
            for i, player in enumerate(td_candidates[:3], start=1):
                combined_prob *= (player['td_prob'] / 100)
                
                if player['td_prob'] >= 60:
                    status = "🔒 Lock"
                elif player['td_prob'] >= 50:
                    status = "✅ Strong"
                else:
                    status = "⚠️ Decent"
                
                message += f"{i}. **{player['name']}** ({player['position']})\n"
                message += f"   {player['team']} | {player['td_prob']}% {status}\n\n"
            
            parlay_prob = combined_prob * 100
            payout_odds = 100 / parlay_prob if parlay_prob > 0 else 999
            
            message += f"💵 **Parlay Probability: {parlay_prob:.1f}%**\n"
            message += f"📊 **Estimated Payout: {payout_odds:.1f} to 1**\n\n"
            
            if parlay_prob >= 15:
                message += "✅ **RECOMMENDED** - Strong TD candidates!"
            elif parlay_prob >= 10:
                message += "⚠️ **RISKY** - Decent but not guaranteed"
            else:
                message += "🚫 **SKIP** - Too many longshots"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in parlay_command: {error_details}")
            await update.message.reply_text(f"Error generating TD parlay: {str(e)}\nCheck console for details.")
    
    async def yolo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /yolo command - Longshot TD Parlay"""
        try:
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            
            # Get roster data for all teams to find longshot TD scorers
            message = f"🎰 **YOLO TD PARLAY - WEEK {current_week}** 🎰\n\n"
            message += "💎 *Longshot touchdown scorers for BIG payouts!*\n"
            message += "WR2s, backup RBs, TEs with boom potential\n\n"
            
            longshot_candidates = []
            
            # Get each team's roster
            for team in teams:
                team_id = team['id']
                team_name = team.get('name', 'Unknown')
                
                # Get roster
                endpoint = f"seasons/{self.espn_api.season}/segments/0/leagues/{self.espn_api.league_id}"
                params = {
                    'view': ['mRoster'],
                    'scoringPeriodId': current_week
                }
                
                try:
                    week_data = self.espn_api._make_request(endpoint, params)
                    
                    if 'teams' not in week_data:
                        continue
                    
                    team_data = next((t for t in week_data['teams'] if t['id'] == team_id), None)
                    if not team_data or 'roster' not in team_data:
                        continue
                    
                    roster = team_data['roster']
                    if 'entries' not in roster:
                        continue
                    
                    # Find bench/flex players (longshot TD scorers)
                    for entry in roster['entries']:
                        slot_id = entry.get('lineupSlotId')
                        player_entry = entry.get('playerPoolEntry', {})
                        player_info = player_entry.get('player', {})
                        
                        player_name = player_info.get('fullName', 'Unknown')
                        position_id = player_info.get('defaultPositionId', 0)
                        
                        # Position IDs: 2=RB, 4=WR, 6=TE
                        # Look for: Flex (23), WR (4), RB (2), TE (6) slots
                        
                        # Skip IR and QBs/K/DST
                        if slot_id == 21 or position_id not in [2, 4, 6]:
                            continue
                        
                        # Focus on bench players and FLEX (longshots)
                        if slot_id == 20:  # Bench
                            td_prob = 25  # Bench players = longshot
                        elif slot_id == 23:  # FLEX
                            td_prob = 35  # FLEX = medium longshot
                        elif position_id == 6:  # TE starters
                            td_prob = 40  # TEs = decent longshot
                        else:
                            continue  # Skip main RB/WR starters (save for /parlay)
                        
                        position_name = {2: 'RB', 4: 'WR', 6: 'TE'}.get(position_id, 'FLEX')
                        
                        longshot_candidates.append({
                            'name': player_name,
                            'position': position_name,
                            'team': team_name,
                            'td_prob': td_prob
                        })
                
                except Exception as e:
                    print(f"Error getting roster for team {team_id}: {e}")
                    continue
            
            # Sort by TD probability (highest longshots first)
            longshot_candidates.sort(key=lambda x: x['td_prob'], reverse=True)
            
            if len(longshot_candidates) < 3:
                await update.message.reply_text("⏳ Not enough player data for YOLO parlays yet!")
                return
            
            # Build 3-leg longshot parlay
            message += "**3-LEG LONGSHOT TD PARLAY:**\n"
            combined_prob = 1.0
            
            for i, player in enumerate(longshot_candidates[:3], start=1):
                combined_prob *= (player['td_prob'] / 100)
                
                if player['td_prob'] >= 35:
                    status = "⚡ Live"
                elif player['td_prob'] >= 25:
                    status = "🎲 Longshot"
                else:
                    status = "💎 Moon Shot"
                
                message += f"{i}. **{player['name']}** ({player['position']})\n"
                message += f"   {player['team']} | {player['td_prob']}% {status}\n\n"
            
            parlay_prob = combined_prob * 100
            payout_odds = 100 / parlay_prob if parlay_prob > 0 else 999
            
            message += f"🎰 **Parlay Probability: {parlay_prob:.1f}%**\n"
            message += f"💰 **Estimated Payout: {payout_odds:.0f} to 1** 🚀\n\n"
            
            if parlay_prob >= 5:
                message += "🔥 **YOLO-WORTHY** - Not impossible!"
            elif parlay_prob >= 2:
                message += "🎲 **SPICY** - Pray to the fantasy gods"
            else:
                message += "💎 **MOON SHOT** - You miss 100% of shots you don't take!"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in yolo_command: {error_details}")
            await update.message.reply_text(f"Error generating YOLO TD parlay: {str(e)}\nCheck console for details.")
    
    async def luck_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /luck command - Luck Analysis"""
        try:
            teams = self.espn_api.get_teams()
            
            luck_data = []
            for team in teams:
                record = team.get('record', {}).get('overall', {})
                wins = record.get('wins', 0)
                losses = record.get('losses', 0)
                ties = record.get('ties', 0)
                pf = record.get('pointsFor', 0)
                pa = record.get('pointsAgainst', 0)
                
                total_games = wins + losses + ties
                if total_games == 0:
                    continue
                
                actual_wins = wins + 0.5 * ties
                expected_wins = self.analytics.calculate_pythagorean_expectation(pf, pa, total_games)
                luck = actual_wins - expected_wins
                
                luck_data.append({
                    'name': team.get('name', 'Unknown'),
                    'abbrev': team.get('abbrev', 'UNK'),
                    'actual_wins': actual_wins,
                    'expected_wins': expected_wins,
                    'luck': luck,
                    'record': f"{wins}-{losses}-{ties}"
                })
            
            # Sort by luck (most lucky to most cursed)
            luck_data.sort(key=lambda x: x['luck'], reverse=True)
            
            message = "🍀 **LUCK ANALYSIS** 🍀\n\n"
            message += "📊 *Based on points scored vs points against*\n"
            message += "Expected wins = How many wins you 'should' have based on scoring\n"
            message += "Luck = Actual wins - Expected wins\n"
            message += "Ranked from luckiest (#1) to most cursed\n\n"
            
            for rank, team in enumerate(luck_data, start=1):
                if team['luck'] > 0:
                    status = "🍀 Lucky"
                elif team['luck'] < -0.5:
                    status = "😈 Cursed"
                else:
                    status = "⚖️ Neutral"
                
                message += f"**#{rank}. {team['name']}** ({team['abbrev']})\n"
                message += f"📊 {team['record']} | Expected: {team['expected_wins']:.1f} | Actual: {team['actual_wins']:.1f}\n"
                message += f"🎯 Luck: {team['luck']:+.1f} {status}\n\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in luck_command: {error_details}")
            await update.message.reply_text(f"Error generating luck analysis: {str(e)}\nCheck console for details.")
    
    async def all_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /all command - All-Play Records"""
        try:
            # Get week from command args, default to season
            week = None
            if context.args:
                try:
                    week = int(context.args[0])
                except ValueError:
                    await update.message.reply_text("Invalid week number. Usage: /all [week]")
                    return
            
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            
            if week:
                # Single week all-play
                matchups = self.espn_api.get_matchups(week)
                if not matchups:
                    await update.message.reply_text(f"No matchups found for week {week}")
                    return
                
                # Get scores for the week
                week_scores = {}
                for matchup in matchups:
                    home_id = matchup['home']['teamId']
                    away_id = matchup['away']['teamId']
                    week_scores[home_id] = matchup['home']['totalPoints']
                    week_scores[away_id] = matchup['away']['totalPoints']
                
                # Calculate all-play for the week
                all_play_data = []
                for team in teams:
                    team_id = team['id']
                    if team_id not in week_scores:
                        continue
                    
                    team_score = week_scores[team_id]
                    wins = sum(1 for score in week_scores.values() if team_score > score)
                    losses = sum(1 for score in week_scores.values() if team_score < score)
                    
                    all_play_data.append({
                        'name': team.get('name', 'Unknown'),
                        'abbrev': team.get('abbrev', 'UNK'),
                        'wins': wins,
                        'losses': losses,
                        'score': team_score
                    })
                
                message = f"🎯 **WEEK {week} ALL-PLAY** 🎯\n\n"
                
            else:
                # Season all-play
                message = "🎯 **SEASON ALL-PLAY** 🎯\n\n"
                message += "📊 *Your record if you played EVERYONE each week*\n"
                message += "Removes schedule luck - shows true team strength\n"
                message += "Win every time you outscore a team, lose when you don't\n\n"
                
                # Get all team scores for the season
                all_team_scores = {}
                for team in teams:
                    team_id = team['id']
                    scores = []
                    
                    for week_num in range(1, current_week):
                        matchups = self.espn_api.get_matchups(week_num)
                        for matchup in matchups:
                            if matchup['home']['teamId'] == team_id:
                                scores.append(matchup['home']['totalPoints'])
                                break
                            elif matchup['away']['teamId'] == team_id:
                                scores.append(matchup['away']['totalPoints'])
                                break
                    
                    all_team_scores[team_id] = scores
                
                # Calculate all-play records
                all_play_data = []
                for team in teams:
                    team_id = team['id']
                    team_scores = all_team_scores[team_id]
                    
                    wins, losses = self.analytics.calculate_all_play_record(team_scores, all_team_scores)
                    
                    record = team.get('record', {}).get('overall', {})
                    all_play_data.append({
                        'name': team.get('name', 'Unknown'),
                        'abbrev': team.get('abbrev', 'UNK'),
                        'wins': wins,
                        'losses': losses,
                        'score': record.get('pointsFor', 0)
                    })
            
            # Sort by wins
            all_play_data.sort(key=lambda x: x['wins'], reverse=True)
            
            for rank, team in enumerate(all_play_data, start=1):
                win_pct = team['wins'] / (team['wins'] + team['losses']) if (team['wins'] + team['losses']) > 0 else 0
                win_pct_display = f"{win_pct * 100:.1f}%"
                message += f"**#{rank}. {team['name']}** ({team['abbrev']})\n"
                message += f"📊 {team['wins']}-{team['losses']} ({win_pct_display})\n\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in all_command: {error_details}")
            await update.message.reply_text(f"Error generating all-play records: {str(e)}\nCheck console for details.")
    
    async def boom_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /boom command - Boom/Bust Analysis"""
        try:
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            
            boom_data = []
            for team in teams:
                team_id = team['id']
                
                # Get all team scores for the season
                team_scores = []
                for week in range(1, current_week):
                    matchups = self.espn_api.get_matchups(week)
                    for matchup in matchups:
                        if matchup['home']['teamId'] == team_id:
                            team_scores.append(matchup['home']['totalPoints'])
                            break
                        elif matchup['away']['teamId'] == team_id:
                            team_scores.append(matchup['away']['totalPoints'])
                            break
                
                if not team_scores:
                    continue
                
                metrics = self.analytics.calculate_boom_bust_metrics(team_scores)
                
                boom_data.append({
                    'name': team.get('name', 'Unknown'),
                    'abbrev': team.get('abbrev', 'UNK'),
                    'ceiling': metrics['ceiling'],
                    'floor': metrics['floor'],
                    'spread': metrics['spread'],
                    'consistency': metrics['consistency'],
                    'avg_score': np.mean(team_scores),
                    'games_played': len(team_scores)
                })
            
            # Sort by consistency (most consistent first)
            boom_data.sort(key=lambda x: x['consistency'], reverse=True)
            
            message = "💥 **BOOM/BUST ANALYSIS** 💥\n\n"
            message += "📊 *Measures scoring consistency vs volatility*\n"
            message += "Ceiling (P80) = Your top 20% of scores\n"
            message += "Floor (P20) = Your bottom 20% of scores\n"
            message += "Spread = How consistent you are (lower = more consistent)\n"
            message += "Ranked by most consistent teams\n\n"
            
            for rank, team in enumerate(boom_data, start=1):
                # Categorize team type
                if team['spread'] > 40:
                    team_type = "🎢 High Variance"
                elif team['spread'] > 25:
                    team_type = "📊 Moderate Variance"
                else:
                    team_type = "🎯 Consistent"
                
                # Consistency rating
                if team['consistency'] > 0.05:
                    consistency_rating = "🟢 Very Consistent"
                elif team['consistency'] > 0.03:
                    consistency_rating = "🟡 Consistent"
                else:
                    consistency_rating = "🔴 Inconsistent"
                
                message += f"**#{rank}. {team['name']}** ({team['abbrev']})\n"
                message += f"📊 Avg: {team['avg_score']:.1f} | Games: {team['games_played']}\n"
                message += f"🚀 Ceiling (P80): {team['ceiling']:.1f}\n"
                message += f"📉 Floor (P20): {team['floor']:.1f}\n"
                message += f"📏 Spread: {team['spread']:.1f} | {team_type}\n"
                message += f"🎯 {consistency_rating}\n\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Error generating boom/bust analysis: {str(e)}")
    
    async def regret_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /regret command - Perfect Lineup Analysis"""
        try:
            from optimal_lineup import calculate_optimal_lineup
            
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            
            if current_week <= 1:
                await update.message.reply_text("No completed weeks yet!")
                return
            
            regret_data = []
            
            for team in teams:
                team_id = team['id']
                actual_wins = 0
                actual_losses = 0
                actual_ties = 0
                optimal_wins = 0
                optimal_losses = 0
                optimal_ties = 0
                total_regret = 0
                games_played = 0
                
                # Go through each week
                for week in range(1, current_week):
                    # Get roster data for this week
                    endpoint = f"seasons/{self.espn_api.season}/segments/0/leagues/{self.espn_api.league_id}"
                    params = {
                        'view': ['mMatchup', 'mRoster'],
                        'scoringPeriodId': week
                    }
                    
                    week_data = self.espn_api._make_request(endpoint, params)
                    
                    # Find this team's data
                    team_roster = None
                    team_actual_score = 0
                    opponent_score = 0
                    
                    if 'teams' in week_data:
                        for t in week_data['teams']:
                            if t['id'] == team_id:
                                team_roster = t.get('roster', {})
                                # Get matchup score
                                matchups = self.espn_api.get_matchups(week)
                                for matchup in matchups:
                                    if matchup['home']['teamId'] == team_id:
                                        team_actual_score = matchup['home']['totalPoints']
                                        opponent_score = matchup['away']['totalPoints']
                                        break
                                    elif matchup['away']['teamId'] == team_id:
                                        team_actual_score = matchup['away']['totalPoints']
                                        opponent_score = matchup['home']['totalPoints']
                                        break
                                break
                    
                    if not team_roster:
                        continue
                    
                    # Calculate optimal lineup
                    optimal_result = calculate_optimal_lineup(team_roster)
                    team_optimal_score = optimal_result['optimal_score']
                    week_regret = optimal_result['regret']
                    
                    # Calculate actual result
                    if team_actual_score > opponent_score:
                        actual_wins += 1
                    elif team_actual_score < opponent_score:
                        actual_losses += 1
                    else:
                        actual_ties += 1
                    
                    # Calculate optimal result (what would have happened with optimal lineup)
                    if team_optimal_score > opponent_score:
                        optimal_wins += 1
                    elif team_optimal_score < opponent_score:
                        optimal_losses += 1
                    else:
                        optimal_ties += 1
                    
                    total_regret += week_regret
                    games_played += 1
                
                # Calculate games that could have been won with optimal lineup
                games_gained = optimal_wins - actual_wins
                
                regret_data.append({
                    'name': team.get('name', 'Unknown'),
                    'abbrev': team.get('abbrev', 'UNK'),
                    'actual_record': f"{actual_wins}-{actual_losses}-{actual_ties}",
                    'optimal_record': f"{optimal_wins}-{optimal_losses}-{optimal_ties}",
                    'actual_wins': actual_wins,
                    'optimal_wins': optimal_wins,
                    'games_gained': games_gained,
                    'total_regret': total_regret,
                    'avg_regret': total_regret / games_played if games_played > 0 else 0
                })
            
            # Sort by games that could have been gained
            regret_data.sort(key=lambda x: x['games_gained'], reverse=True)
            
            message = "😭 **PERFECT LINEUP ANALYSIS** 😭\n\n"
            message += "🤔 *What if you played the perfect lineup every week?*\n"
            message += "Analyzes each position: if WR on bench scored more, counts the points lost\n"
            message += "Shows your actual record vs what it would be with optimal lineups\n"
            message += "Ranked by most wins lost due to lineup decisions\n\n"
            
            for rank, team in enumerate(regret_data, start=1):
                games_gained = team['games_gained']
                
                if games_gained >= 3:
                    status = "😭😭😭 Brutal losses"
                elif games_gained >= 2:
                    status = "😤😤 Major regret"
                elif games_gained >= 1:
                    status = "😐 Some regret"
                elif games_gained == 0:
                    status = "✅ Perfect decisions"
                else:
                    status = "🎯 Over-performed"
                
                message += f"**#{rank}. {team['name']}** ({team['abbrev']})\n"
                message += f"📊 Actual: {team['actual_record']} | Perfect: {team['optimal_record']}\n"
                message += f"💔 Games Lost: {games_gained:+d} | {status}\n"
                message += f"📉 Avg Regret: {team['avg_regret']:.1f} pts/week\n\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in regret_command: {error_details}")
            await update.message.reply_text(f"Error generating regret analysis: {str(e)}\nCheck console for details.")
    
    async def waiver_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /waiver command - Best Undrafted Waiver Wire Pickups"""
        try:
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            
            if current_week <= 2:
                await update.message.reply_text("Not enough weeks to analyze waiver pickups yet!")
                return
            
            # STEP 1: Get Week 1 rosters to identify drafted players
            drafted_players = set()
            
            endpoint = f"seasons/{self.espn_api.season}/segments/0/leagues/{self.espn_api.league_id}"
            params = {'view': ['mRoster'], 'scoringPeriodId': 1}
            
            try:
                week1_data = self.espn_api._make_request(endpoint, params)
                
                if 'teams' in week1_data:
                    for team in week1_data['teams']:
                        roster = team.get('roster', {})
                        entries = roster.get('entries', [])
                        
                        for entry in entries:
                            player_entry = entry.get('playerPoolEntry', {})
                            player_info = player_entry.get('player', {})
                            player_id = player_info.get('id')
                            
                            if player_id:
                                drafted_players.add(player_id)
                
                print(f"📊 Found {len(drafted_players)} drafted players")
            except Exception as e:
                print(f"Error getting Week 1 rosters: {e}")
                await update.message.reply_text("Error accessing draft data. Try again!")
                return
            
            # STEP 2: Track waiver pickups (players NOT in Week 1)
            waiver_pickups = {}  # player_id -> {name, position, team_owner, total_points, added_week, last_seen_week}
            
            # Go through weeks 2+ to find waiver additions
            # IMPORTANT: Must use matchup data to get ACTUAL fantasy points scored
            for week in range(2, current_week):
                params = {'view': ['mMatchup', 'mTeam'], 'scoringPeriodId': week}
                
                try:
                    week_data = self.espn_api._make_request(endpoint, params)
                    
                    if 'schedule' not in week_data:
                        continue
                    
                    # Process matchups to get actual fantasy points
                    for matchup in week_data['schedule']:
                        matchup_period = matchup.get('matchupPeriodId')
                        
                        if matchup_period != week:
                            continue
                        
                        # Check both home and away teams
                        for team_key in ['home', 'away']:
                            team_data = matchup.get(team_key, {})
                            team_id = team_data.get('teamId')
                            
                            # Get team name from teams list
                            team_name = 'Unknown'
                            if 'teams' in week_data:
                                for t in week_data['teams']:
                                    if t.get('id') == team_id:
                                        team_name = t.get('name', 'Unknown')
                                        break
                            
                            # Get roster with ACTUAL points from matchup
                            roster_entries = team_data.get('rosterForCurrentScoringPeriod', {}).get('entries', [])
                            
                            for entry in roster_entries:
                                player_entry = entry.get('playerPoolEntry', {})
                                player_info = player_entry.get('player', {})
                                
                                player_id = player_info.get('id')
                                if not player_id:
                                    continue
                                
                                # ONLY track players who were NOT drafted (not in Week 1)
                                if player_id in drafted_players:
                                    continue
                                
                                player_name = player_info.get('fullName', 'Unknown')
                                position_id = player_info.get('defaultPositionId', 0)
                                
                                # Get position name (ESPN position IDs)
                                position_map = {1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'D/ST', 17: 'K'}
                                position = position_map.get(position_id, 'FLEX')
                                
                                # Get ACTUAL fantasy points from matchup data
                                weekly_points = player_entry.get('appliedStatTotal', 0)
                                
                                # Track waiver pickup
                                if player_id not in waiver_pickups:
                                    waiver_pickups[player_id] = {
                                        'name': player_name,
                                        'position': position,
                                        'team': team_name,
                                        'total_points': 0,
                                        'added_week': week,
                                        'last_seen_week': week
                                    }
                                
                                # Sum up weekly points
                                waiver_pickups[player_id]['total_points'] += weekly_points
                                waiver_pickups[player_id]['last_seen_week'] = week
                                
                                # Update team owner (in case player was traded/picked up by different team)
                                waiver_pickups[player_id]['team'] = team_name
                
                except Exception as e:
                    print(f"Error getting week {week} matchup data: {e}")
                    continue
            
            print(f"💎 Found {len(waiver_pickups)} waiver pickups")
            
            # Debug: Show a few examples with realistic PPG
            if waiver_pickups:
                print("\n📊 Waiver Pickup Calculations (showing top 3):")
                sorted_samples = sorted(waiver_pickups.items(), 
                                      key=lambda x: x[1]['total_points'], 
                                      reverse=True)[:3]
                for player_id, stats in sorted_samples:
                    weeks = stats['last_seen_week'] - stats['added_week'] + 1
                    ppg = stats['total_points'] / weeks if weeks > 0 else 0
                    print(f"  {stats['name']} ({stats['position']}): {stats['total_points']:.1f} pts / {weeks} weeks = {ppg:.1f} PPG")
                print()
            
            if not waiver_pickups:
                await update.message.reply_text("No waiver pickups found yet! Everyone still has their drafted players.")
                return
            
            # STEP 3: Find top waiver gems
            top_gems = []
            for player_id, stats in waiver_pickups.items():
                # Calculate weeks on roster (from when added to last seen)
                # This counts ALL weeks they were on a roster, not just weeks they scored
                weeks_on_roster = stats['last_seen_week'] - stats['added_week'] + 1
                
                # Must have been on roster for at least 2 weeks and scored at least 1 point total
                if weeks_on_roster >= 2 and stats['total_points'] > 0:
                    # PPG = total points / weeks on roster
                    ppg = stats['total_points'] / weeks_on_roster
                    top_gems.append({
                        'name': stats['name'],
                        'position': stats['position'],
                        'team': stats['team'],
                        'total_points': stats['total_points'],
                        'ppg': ppg,
                        'weeks_played': weeks_on_roster,
                        'added_week': stats['added_week']
                    })
            
            # Sort by PPG
            top_gems.sort(key=lambda x: x['ppg'], reverse=True)
            
            # Build message
            message = "💎 **WAIVER WIRE GEMS** 💎\n\n"
            message += "🔥 *Best UNDRAFTED pickups (not drafted in Week 1)*\n"
            message += "Ranked by Points Per Game\n\n"
            
            if not top_gems:
                message += "No waiver gems yet! All pickups have been busts so far. 😅"
            else:
                for rank, player in enumerate(top_gems[:10], 1):  # Top 10
                    ppg = player['ppg']
                    total = player['total_points']
                    weeks = player['weeks_played']
                    added = player['added_week']
                    pos = player['position']
                    
                    # Determine gem level
                    if ppg >= 20:
                        status = "💎 ELITE FIND"
                    elif ppg >= 15:
                        status = "🔥 STUD PICKUP"
                    elif ppg >= 10:
                        status = "⭐ SOLID ADD"
                    elif ppg >= 7:
                        status = "✅ DECENT"
                    else:
                        status = "📊 DEPTH"
                    
                    message += f"**#{rank}. {player['name']}** ({pos})\n"
                    message += f"   {status}\n"
                    message += f"   Owner: {player['team']}\n"
                    message += f"   {ppg:.1f} PPG ({total:.1f} pts in {weeks} weeks)\n"
                    message += f"   🆕 Added Week {added}\n\n"
            
            message += "\n💡 **TIP:** These were all FREE pickups that paid off!"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in waiver_command: {error_details}")
            await update.message.reply_text(f"Error generating waiver wire analysis: {str(e)}\nCheck console for details.")
    
    async def odds_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /odds command - Playoff Odds"""
        try:
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            playoff_start_week = self.espn_api.get_playoff_start_week()
            playoff_teams = self.espn_api.get_playoff_teams()
            
            remaining_weeks = playoff_start_week - current_week
            
            if remaining_weeks <= 0:
                await update.message.reply_text("Playoffs have already started!")
                return
            
            # Prepare team data for simulation
            teams_data = {}
            for team in teams:
                team_id = team['id']
                
                # Get team scores for the season
                team_scores = []
                for week in range(1, current_week):
                    matchups = self.espn_api.get_matchups(week)
                    for matchup in matchups:
                        if matchup['home']['teamId'] == team_id:
                            team_scores.append(matchup['home']['totalPoints'])
                            break
                        elif matchup['away']['teamId'] == team_id:
                            team_scores.append(matchup['away']['totalPoints'])
                            break
                
                record = team.get('record', {}).get('overall', {})
                teams_data[team_id] = {
                    'wins': record.get('wins', 0),
                    'losses': record.get('losses', 0),
                    'ties': record.get('ties', 0),
                    'all_scores': team_scores,
                    'name': team.get('name', 'Unknown'),
                    'abbrev': team.get('abbrev', 'UNK')
                }
            
            # Run Monte Carlo simulation
            playoff_odds = self.analytics.simulate_playoff_odds(
                teams_data, remaining_weeks, playoff_teams, simulations=5000
            )
            
            # Sort by playoff odds
            odds_data = []
            for team_id, odds in playoff_odds.items():
                team_info = teams_data.get(team_id, {})
                odds_data.append({
                    'name': team_info.get('name', 'Unknown'),
                    'abbrev': team_info.get('abbrev', 'UNK'),
                    'odds': odds,
                    'wins': team_info.get('wins', 0),
                    'losses': team_info.get('losses', 0)
                })
            
            odds_data.sort(key=lambda x: x['odds'], reverse=True)
            
            message = "🎲 **PLAYOFF ODDS** 🎲\n\n"
            message += f"🔮 *Simulated 5,000 possible season outcomes!*\n"
            message += f"Based on your scoring patterns & remaining schedule\n"
            message += f"{remaining_weeks} weeks left to play\n"
            message += "Ranked by highest playoff chances\n\n"
            
            for rank, team in enumerate(odds_data, start=1):
                odds_percent = team['odds'] * 100
                record = f"{team['wins']}-{team['losses']}"
                
                if odds_percent > 80:
                    status = "🔒 Lock"
                elif odds_percent > 50:
                    status = "📈 Likely"
                elif odds_percent > 25:
                    status = "⚖️ Bubble"
                else:
                    status = "📉 Unlikely"
                
                message += f"**#{rank}. {team['name']}** ({team['abbrev']})\n"
                message += f"📊 {record} | {odds_percent:.1f}% {status}\n\n"
            
            message += f"*Based on {5000} simulations of remaining schedule*\n"
            message += f"*Playoffs start Week {playoff_start_week} ({playoff_teams} teams)*"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Error generating playoff odds: {str(e)}")
    
    async def sos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sos command - Strength of Schedule"""
        try:
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            
            # Prepare team data for SOS calculation
            teams_data = {}
            for team in teams:
                team_id = team['id']
                
                # Get opponent scores for each week
                opponent_scores = []
                team_scores = []
                
                for week in range(1, current_week):
                    matchups = self.espn_api.get_matchups(week)
                    for matchup in matchups:
                        if matchup['home']['teamId'] == team_id:
                            team_score = matchup['home']['totalPoints']
                            opponent_score = matchup['away']['totalPoints']
                            team_scores.append(team_score)
                            opponent_scores.append(opponent_score)
                            break
                        elif matchup['away']['teamId'] == team_id:
                            team_score = matchup['away']['totalPoints']
                            opponent_score = matchup['home']['totalPoints']
                            team_scores.append(team_score)
                            opponent_scores.append(opponent_score)
                            break
                
                teams_data[team_id] = {
                    'opponent_scores': opponent_scores,
                    'all_scores': team_scores,
                    'name': team.get('name', 'Unknown'),
                    'abbrev': team.get('abbrev', 'UNK'),
                    'wins': team.get('record', {}).get('overall', {}).get('wins', 0),
                    'losses': team.get('record', {}).get('overall', {}).get('losses', 0)
                }
            
            # Calculate SOS for each team
            sos_data = []
            for team_id, team_data in teams_data.items():
                sos_metrics = self.analytics.calculate_strength_of_schedule(
                    team_data, teams_data, current_week - 1
                )
                
                sos_data.append({
                    'name': team_data['name'],
                    'abbrev': team_data['abbrev'],
                    'sos_rating': sos_metrics['sos_rating'],
                    'sos_rank': sos_metrics['sos_rank'],
                    'total_teams': sos_metrics['total_teams'],
                    'avg_opponent_score': sos_metrics['avg_opponent_score'],
                    'league_avg': sos_metrics['league_avg'],
                    'wins': team_data['wins'],
                    'losses': team_data['losses']
                })
            
            # Sort by SOS rating (higher = harder schedule)
            sos_data.sort(key=lambda x: x['sos_rating'], reverse=True)
            
            message = "💪 **STRENGTH OF SCHEDULE** 💪\n\n"
            message += f"📊 *How tough has your schedule been?*\n"
            message += f"Based on opponent scoring through Week {current_week - 1}\n"
            message += "Higher SOS = Tougher opponents\n"
            message += "Ranked from hardest schedule to easiest\n\n"
            
            for rank, team in enumerate(sos_data, start=1):
                sos_percent = (team['sos_rating'] * 100)
                
                if sos_percent > 5:
                    difficulty = "😰 Brutal"
                elif sos_percent > 2:
                    difficulty = "😤 Tough"
                elif sos_percent > -2:
                    difficulty = "😐 Average"
                elif sos_percent > -5:
                    difficulty = "😊 Easy"
                else:
                    difficulty = "😎 Cakewalk"
                
                record = f"{team['wins']}-{team['losses']}"
                
                message += f"**#{rank}. {team['name']}** ({team['abbrev']})\n"
                message += f"📊 {record} | {team['sos_rank']}/{team['total_teams']} SOS Rank\n"
                message += f"📈 Opp Avg: {team['avg_opponent_score']:.1f} | {sos_percent:+.1f}% vs league\n"
                message += f"🎯 {difficulty}\n\n"
            
            message += f"*League Average: {sos_data[0]['league_avg']:.1f} points*\n"
            message += "*Positive % = Harder than average schedule*"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Error generating strength of schedule: {str(e)}")
    
    async def heat_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /heat command - Heat Map"""
        try:
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            
            # Collect all team scores for league averages
            all_scores = []
            team_scores = {}
            
            for team in teams:
                team_id = team['id']
                scores = []
                
                for week in range(1, current_week):
                    matchups = self.espn_api.get_matchups(week)
                    for matchup in matchups:
                        if matchup['home']['teamId'] == team_id:
                            score = matchup['home']['totalPoints']
                            scores.append(score)
                            all_scores.append(score)
                            break
                        elif matchup['away']['teamId'] == team_id:
                            score = matchup['away']['totalPoints']
                            scores.append(score)
                            all_scores.append(score)
                            break
                
                team_scores[team_id] = scores
            
            # Calculate league averages
            league_avg = np.mean(all_scores) if all_scores else 100
            league_std = np.std(all_scores) if all_scores else 20
            
            # Generate heat map data
            heat_data = self.analytics.generate_heat_map_data(team_scores, league_avg, league_std)
            
            message = "🔥 **WEEKLY HEAT MAP** 🔥\n\n"
            message += f"📈 *Week-by-week performance vs league average*\n"
            message += f"🔥 = Hot week (above average) | ❄️ = Cold week (below average)\n"
            message += f"**Consistency score:** Higher = More predictable (0.5+ is very consistent, 0.2- is volatile)\n"
            message += f"Showing weeks 1-{current_week - 1}\n\n"
            
            # Sort teams by average z-score
            team_heat_data = []
            for team in teams:
                team_id = team['id']
                if team_id in heat_data:
                    team_heat_data.append({
                        'name': team.get('name', 'Unknown'),
                        'abbrev': team.get('abbrev', 'UNK'),
                        'heat_data': heat_data[team_id],
                        'avg_z_score': heat_data[team_id]['avg_z_score']
                    })
            
            team_heat_data.sort(key=lambda x: x['avg_z_score'], reverse=True)
            
            for rank, team in enumerate(team_heat_data, start=1):
                avg_z = team['avg_z_score']
                consistency = team['heat_data']['consistency']
                
                if avg_z > 1.0:
                    trend = "🔥 On Fire"
                elif avg_z > 0.5:
                    trend = "📈 Heating Up"
                elif avg_z > -0.5:
                    trend = "😐 Consistent"
                elif avg_z > -1.0:
                    trend = "📉 Cooling Off"
                else:
                    trend = "❄️ Ice Cold"
                
                message += f"**#{rank}. {team['name']}** ({team['abbrev']})\n"
                message += f"📊 Avg Z-Score: {avg_z:+.2f} | {trend}\n"
                
                # Show last 5 weeks of performance
                categories = team['heat_data']['categories']
                recent_categories = categories[-5:] if len(categories) >= 5 else categories
                
                if recent_categories:
                    message += f"🔥 Recent: {' '.join(recent_categories)}\n"
                
                # Explain consistency score (0-1 scale)
                if consistency > 0.75:
                    consistency_label = "🎯 Very Consistent"
                elif consistency > 0.6:
                    consistency_label = "✅ Consistent"
                elif consistency > 0.4:
                    consistency_label = "⚠️ Variable"
                else:
                    consistency_label = "🎲 Volatile"
                
                message += f"🎯 Consistency: {consistency:.3f} ({consistency_label})\n\n"
            
            message += f"*League Avg: {league_avg:.1f} pts | Std Dev: {league_std:.1f}*\n"
            message += "*🔥🔥🔥 Exceptional | 🔥🔥 Great | 🔥 Good | 😐 Average | ❄️ Poor*"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Error generating heat map: {str(e)}")
    
    async def rivals_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /rivals command - Rivalry Tracker"""
        try:
            teams = self.espn_api.get_teams()
            current_week = self.espn_api.get_current_week()
            
            # Build matchup history
            matchup_history = []
            for week in range(1, current_week):
                matchups = self.espn_api.get_matchups(week)
                for matchup in matchups:
                    matchup_history.append({
                        'week': week,
                        'home_team_id': matchup['home']['teamId'],
                        'away_team_id': matchup['away']['teamId'],
                        'home_score': matchup['home']['totalPoints'],
                        'away_score': matchup['away']['totalPoints']
                    })
            
            # Find top rivalries (most games played)
            rivalry_data = []
            
            for i, team1 in enumerate(teams):
                for j, team2 in enumerate(teams[i+1:], i+1):
                    team1_id = team1['id']
                    team2_id = team2['id']
                    
                    # Calculate rivalry metrics
                    rivalry_metrics = self.analytics.calculate_rivalry_metrics(
                        team1_id, team2_id, matchup_history
                    )
                    
                    if rivalry_metrics['total_games'] > 0:
                        rivalry_data.append({
                            'team1': {
                                'id': team1_id,
                                'name': team1.get('name', 'Unknown'),
                                'abbrev': team1.get('abbrev', 'UNK')
                            },
                            'team2': {
                                'id': team2_id,
                                'name': team2.get('name', 'Unknown'),
                                'abbrev': team2.get('abbrev', 'UNK')
                            },
                            'metrics': rivalry_metrics
                        })
            
            # Sort by total games played (most intense rivalries first)
            rivalry_data.sort(key=lambda x: x['metrics']['total_games'], reverse=True)
            
            message = "⚔️ **RIVALRY TRACKER** ⚔️\n\n"
            message += "🔥 *Who owns who in head-to-head matchups?*\n"
            message += "Shows your record vs each opponent & current streaks\n"
            message += "Ranked by most games played (biggest rivalries)\n\n"
            
            # Show top 5 rivalries
            for rank, rivalry in enumerate(rivalry_data[:5], start=1):
                team1 = rivalry['team1']
                team2 = rivalry['team2']
                metrics = rivalry['metrics']
                
                # Determine rivalry intensity
                games_played = metrics['total_games']
                point_diff = abs(metrics['point_diff'])
                
                if games_played >= 5 and point_diff < 20:
                    intensity = "🔥 Intense"
                elif games_played >= 3 and point_diff < 30:
                    intensity = "⚡ Rivalry"
                else:
                    intensity = "👥 Matchup"
                
                message += f"**#{rank}. {team1['name']} vs {team2['name']}**\n"
                message += f"📊 {metrics['record']} | {metrics['point_diff']:+.1f} pt diff\n"
                message += f"🔥 Streak: {metrics['streak']} | {intensity}\n"
                message += f"📅 {games_played} games played\n\n"
            
            if not rivalry_data:
                message += "No head-to-head matchups found yet.\n"
                message += "Rivalries will appear as teams play each other.\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in rivals_command: {error_details}")
            await update.message.reply_text(f"Error generating rivalry tracker: {str(e)}\nCheck console for details.")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command - Command List"""
        try:
            message = "🤖 **FANTASY FOOTBALL ANALYTICS BOT** 🤖\n\n"
            
            message += "**👤 Personal Commands:**\n"
            message += "/pickteam - Pick your team (one-click setup!)\n"
            message += "/myteam - Your team's stats and record\n\n"
            
            message += "**📊 League Analytics:**\n"
            message += "/power - Power rankings (who's really best?)\n"
            message += "/luck - Who's lucky vs unlucky?\n"
            message += "/waiver - Best waiver wire pickups\n"
            message += "/odds - Playoff chances (Monte Carlo!)\n\n"
            
            message += "**📈 Performance:**\n"
            message += "/boom - Consistency vs volatility\n"
            message += "/heat - Performance trends over time\n"
            message += "/sos - Strength of schedule\n"
            message += "/all [week] - All-play records\n\n"
            
            message += "**🎮 Weekly Info:**\n"
            message += "/recap [week] - Week highlights\n"
            message += "/season - Season highlights & records\n"
            message += "/regret - Perfect lineup analysis\n"
            message += "/rivals - Head-to-head tracker\n\n"
            
            message += "**🎰 TD Parlay Picks:**\n"
            message += "/parlay - Safe anytime TD parlay (top RBs/WRs)\n"
            message += "/yolo - Longshot TD parlay (sleepers & boom)\n\n"
            
            message += "**💡 Tip:** Most commands work without arguments!\n"
            message += "Start with `/pickteam` to link your team!\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Error showing help: {str(e)}")
