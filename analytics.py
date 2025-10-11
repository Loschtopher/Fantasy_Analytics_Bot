"""
Advanced Analytics Functions for Fantasy Football
Implements power rankings, ELO, luck calculations, etc.
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from config import POWER_RANKINGS_WEIGHTS, ELO_K_FACTOR, ELO_INITIAL_RATING


class FantasyAnalytics:
    """Advanced analytics for fantasy football data"""
    
    @staticmethod
    def calculate_power_score(team_data: Dict, recent_form_weight: float = 0.25) -> float:
        """Calculate weighted power score for power rankings"""
        weights = POWER_RANKINGS_WEIGHTS
        
        # Win percentage (0-1)
        wins = team_data.get('wins', 0)
        losses = team_data.get('losses', 0)
        ties = team_data.get('ties', 0)
        total_games = wins + losses + ties
        
        if total_games == 0:
            win_pct = 0.5
        else:
            win_pct = (wins + 0.5 * ties) / total_games
        
        # Points For/Against efficiency
        pf = team_data.get('points_for', 0)
        pa = team_data.get('points_against', 0)
        
        if pa == 0:
            efficiency = 1.0
        else:
            efficiency = pf / pa
        
        # Recent form (last 3 games)
        recent_scores = team_data.get('recent_scores', [])
        if len(recent_scores) >= 3:
            recent_avg = np.mean(recent_scores[-3:])
            season_avg = np.mean(team_data.get('all_scores', []))
            if season_avg > 0:
                recent_form = recent_avg / season_avg
            else:
                recent_form = 1.0
        else:
            recent_form = 1.0
        
        # Schedule strength (from actual opponent difficulty)
        schedule_strength = team_data.get('schedule_strength', 1.0)
        
        # Calculate weighted score
        power_score = (
            win_pct * weights['win_percentage'] +
            recent_form * weights['recent_form'] +
            efficiency * weights['efficiency'] +
            schedule_strength * weights['schedule_strength']
        )
        
        return power_score
    
    @staticmethod
    def calculate_pythagorean_expectation(pf: float, pa: float, games: int) -> float:
        """Calculate expected wins using Pythagorean expectation"""
        if pa == 0:
            return games
        
        pythagorean_pct = (pf ** 2.37) / (pf ** 2.37 + pa ** 2.37)
        return pythagorean_pct * games
    
    @staticmethod
    def update_elo_ratings(team1_id: int, team2_id: int, team1_score: float, 
                          team2_score: float, current_elos: Dict) -> Tuple[float, float]:
        """
        Update ELO ratings after a matchup
        Uses higher K-factor (64 vs 32) for faster adjustment in short fantasy season
        """
        elo1 = current_elos.get(str(team1_id), ELO_INITIAL_RATING)
        elo2 = current_elos.get(str(team2_id), ELO_INITIAL_RATING)
        
        # Use higher K-factor for fantasy (64 instead of 32)
        # Fantasy seasons are short, so we want more movement per game
        K = 64
        
        # Expected scores
        expected1 = 1 / (1 + 10 ** ((elo2 - elo1) / 400))
        expected2 = 1 / (1 + 10 ** ((elo1 - elo2) / 400))
        
        # Actual scores (normalized)
        total_score = team1_score + team2_score
        if total_score == 0:
            actual1 = 0.5
            actual2 = 0.5
        else:
            actual1 = team1_score / total_score
            actual2 = team2_score / total_score
        
        # Update ratings with higher K-factor
        new_elo1 = elo1 + K * (actual1 - expected1)
        new_elo2 = elo2 + K * (actual2 - expected2)
        
        return new_elo1, new_elo2
    
    @staticmethod
    def calculate_boom_bust_metrics(scores: List[float]) -> Dict:
        """Calculate boom/bust consistency metrics"""
        if not scores:
            return {'ceiling': 0, 'floor': 0, 'spread': 0, 'consistency': 0}
        
        scores_array = np.array(scores)
        
        # P80 (ceiling) and P20 (floor)
        ceiling = np.percentile(scores_array, 80)
        floor = np.percentile(scores_array, 20)
        spread = ceiling - floor
        
        # Consistency (1 / standard deviation)
        std_dev = np.std(scores_array)
        consistency = 1 / std_dev if std_dev > 0 else 0
        
        return {
            'ceiling': round(ceiling, 1),
            'floor': round(floor, 1),
            'spread': round(spread, 1),
            'consistency': round(consistency, 3)
        }
    
    @staticmethod
    def calculate_all_play_record(team_scores: List[float], all_teams_scores: Dict) -> Tuple[int, int]:
        """Calculate all-play record (wins/losses if played everyone each week)"""
        wins = 0
        losses = 0
        
        for week_idx, team_score in enumerate(team_scores):
            week_wins = 0
            week_losses = 0
            
            for other_team_id, other_scores in all_teams_scores.items():
                if week_idx < len(other_scores):
                    other_score = other_scores[week_idx]
                    if team_score > other_score:
                        week_wins += 1
                    elif team_score < other_score:
                        week_losses += 1
            
            wins += week_wins
            losses += week_losses
        
        return wins, losses
    
    @staticmethod
    def calculate_streak(team_data: Dict) -> Tuple[str, int]:
        """Calculate current win/loss streak"""
        recent_results = team_data.get('recent_results', [])
        if not recent_results:
            return 'N/A', 0
        
        current_result = recent_results[-1]
        streak = 1
        
        # Count backwards for streak
        for result in reversed(recent_results[:-1]):
            if result == current_result:
                streak += 1
            else:
                break
        
        streak_type = 'W' if current_result == 'W' else 'L' if current_result == 'L' else 'T'
        return streak_type, streak
    
    @staticmethod
    def calculate_z_scores(scores: List[float], league_avg: float, league_std: float) -> List[float]:
        """Calculate z-scores for weekly performance"""
        if league_std == 0:
            return [0.0] * len(scores)
        
        return [(score - league_avg) / league_std for score in scores]
    
    @staticmethod
    def simulate_playoff_odds(teams_data: Dict, remaining_weeks: int, 
                            playoff_teams: int, simulations: int = 10000) -> Dict:
        """Simulate playoff odds using Monte Carlo - simulates all teams together"""
        playoff_counts = {team_id: 0 for team_id in teams_data.keys()}
        
        # Calculate real league average from actual data
        all_league_scores = []
        for team_data in teams_data.values():
            all_league_scores.extend(team_data.get('all_scores', []))
        
        league_avg = np.mean(all_league_scores) if all_league_scores else 115
        league_std = np.std(all_league_scores) if all_league_scores else 20
        
        # Run full season simulations
        for sim in range(simulations):
            # Simulate remaining games for ALL teams
            sim_records = {}
            
            for team_id, team_data in teams_data.items():
                current_wins = team_data.get('wins', 0)
                current_losses = team_data.get('losses', 0)
                current_ties = team_data.get('ties', 0)
                
                # Get scoring distribution
                all_scores = team_data.get('all_scores', [])
                if not all_scores:
                    sim_records[team_id] = {
                        'wins': current_wins,
                        'losses': current_losses,
                        'ties': current_ties
                    }
                    continue
                
                avg_score = np.mean(all_scores)
                std_score = np.std(all_scores)
                
                sim_wins = current_wins
                sim_losses = current_losses
                sim_ties = current_ties
                
                # Simulate remaining games
                for week in range(remaining_weeks):
                    # Generate random score based on team's actual distribution
                    team_score = max(0, np.random.normal(avg_score, std_score))
                    
                    # Generate random opponent score using real league average
                    opponent_score = max(0, np.random.normal(league_avg, league_std))
                    
                    if team_score > opponent_score:
                        sim_wins += 1
                    elif team_score < opponent_score:
                        sim_losses += 1
                    else:
                        sim_ties += 1
                
                sim_records[team_id] = {
                    'wins': sim_wins,
                    'losses': sim_losses,
                    'ties': sim_ties,
                    'win_pct': (sim_wins + 0.5 * sim_ties) / (sim_wins + sim_losses + sim_ties)
                }
            
            # Rank teams by win percentage
            ranked_teams = sorted(sim_records.items(), key=lambda x: x[1]['win_pct'], reverse=True)
            
            # Top N teams make playoffs
            for i, (team_id, record) in enumerate(ranked_teams):
                if i < playoff_teams:
                    playoff_counts[team_id] += 1
        
        # Convert to probabilities
        results = {team_id: count / simulations for team_id, count in playoff_counts.items()}
        
        return results
    
    @staticmethod
    def calculate_start_sit_regret(team_data: Dict, week: int) -> Dict:
        """Calculate start/sit regret for a team"""
        # This is a simplified implementation
        # In reality, would need access to lineup decisions and bench scores
        
        actual_score = team_data.get('weekly_scores', {}).get(str(week), 0)
        optimal_score = actual_score * 1.1  # Placeholder - would calculate based on bench
        
        regret = optimal_score - actual_score
        bench_efficiency = (regret / optimal_score) * 100 if optimal_score > 0 else 0
        
        return {
            'actual_score': actual_score,
            'optimal_score': optimal_score,
            'regret': regret,
            'bench_efficiency': bench_efficiency
        }
    
    @staticmethod
    def calculate_strength_of_schedule(team_data: Dict, all_teams_data: Dict, 
                                     weeks_played: int) -> Dict:
        """Calculate strength of schedule metrics"""
        opponents_scores = team_data.get('opponent_scores', [])
        
        if not opponents_scores:
            return {'sos_rating': 0, 'sos_rank': 0, 'rest_sos': 0}
        
        # Calculate average opponent score
        avg_opponent_score = np.mean(opponents_scores)
        
        # Calculate league average
        all_scores = []
        for team in all_teams_data.values():
            all_scores.extend(team.get('all_scores', []))
        
        league_avg = np.mean(all_scores) if all_scores else 100
        
        # SOS rating (opponent average vs league average)
        sos_rating = (avg_opponent_score / league_avg) - 1
        
        # Calculate SOS rank
        sos_ratings = []
        for team in all_teams_data.values():
            team_opponents = team.get('opponent_scores', [])
            if team_opponents:
                team_sos = (np.mean(team_opponents) / league_avg) - 1
                sos_ratings.append(team_sos)
        
        sos_rank = sum(1 for rating in sos_ratings if rating < sos_rating) + 1
        
        return {
            'sos_rating': round(sos_rating, 3),
            'sos_rank': sos_rank,
            'total_teams': len(sos_ratings),
            'avg_opponent_score': round(avg_opponent_score, 1),
            'league_avg': round(league_avg, 1)
        }
    
    @staticmethod
    def calculate_rivalry_metrics(team1_id: int, team2_id: int, 
                                matchup_history: List[Dict]) -> Dict:
        """Calculate rivalry metrics between two teams"""
        h2h_matchups = [m for m in matchup_history 
                       if (m.get('home_team_id') == team1_id and m.get('away_team_id') == team2_id) or
                          (m.get('home_team_id') == team2_id and m.get('away_team_id') == team1_id)]
        
        if not h2h_matchups:
            return {'record': '0-0-0', 'point_diff': 0, 'streak': 'No games', 'total_games': 0}
        
        team1_wins = 0
        team1_losses = 0
        team1_ties = 0
        point_diff = 0
        
        for matchup in h2h_matchups:
            if matchup['home_team_id'] == team1_id:
                team1_score = matchup['home_score']
                team2_score = matchup['away_score']
            else:
                team1_score = matchup['away_score']
                team2_score = matchup['home_score']
            
            point_diff += team1_score - team2_score
            
            if team1_score > team2_score:
                team1_wins += 1
            elif team1_score < team2_score:
                team1_losses += 1
            else:
                team1_ties += 1
        
        # Calculate current streak
        recent_matchups = sorted(h2h_matchups, key=lambda x: x.get('week', 0), reverse=True)
        current_streak = 0
        streak_type = 'T'
        
        for matchup in recent_matchups:
            if matchup['home_team_id'] == team1_id:
                team1_score = matchup['home_score']
                team2_score = matchup['away_score']
            else:
                team1_score = matchup['away_score']
                team2_score = matchup['home_score']
            
            if team1_score > team2_score:
                if streak_type == 'W' or current_streak == 0:
                    streak_type = 'W'
                    current_streak += 1
                else:
                    break
            elif team1_score < team2_score:
                if streak_type == 'L' or current_streak == 0:
                    streak_type = 'L'
                    current_streak += 1
                else:
                    break
            else:
                if streak_type == 'T' or current_streak == 0:
                    streak_type = 'T'
                    current_streak += 1
                else:
                    break
        
        return {
            'record': f"{team1_wins}-{team1_losses}-{team1_ties}",
            'point_diff': round(point_diff, 1),
            'streak': f"{streak_type}{current_streak}",
            'total_games': len(h2h_matchups)
        }
    
    @staticmethod
    def generate_heat_map_data(team_scores: Dict, league_avg: float, 
                             league_std: float) -> Dict:
        """Generate heat map data for weekly performance"""
        heat_data = {}
        
        for team_id, scores in team_scores.items():
            if not scores:
                continue
            
            # Calculate z-scores for each week
            z_scores = []
            for score in scores:
                if league_std > 0:
                    z_score = (score - league_avg) / league_std
                else:
                    z_score = 0
                z_scores.append(z_score)
            
            # Categorize performance
            performance_categories = []
            for z_score in z_scores:
                if z_score > 1.5:
                    category = "🔥🔥🔥"  # Exceptional
                elif z_score > 1.0:
                    category = "🔥🔥"    # Great
                elif z_score > 0.5:
                    category = "🔥"      # Good
                elif z_score > -0.5:
                    category = "😐"      # Average
                elif z_score > -1.0:
                    category = "❄️"      # Poor
                elif z_score > -1.5:
                    category = "❄️❄️"    # Very Poor
                else:
                    category = "❄️❄️❄️"  # Terrible
                
                performance_categories.append(category)
            
            # Calculate consistency score (0-1 scale, higher = more consistent)
            # Use coefficient of variation approach
            z_std = np.std(z_scores)
            # Normalize: typical z-score std is 0.5-2.0, map to 0-1 scale
            consistency = max(0, min(1, 1 - (z_std / 2.5)))
            
            heat_data[team_id] = {
                'z_scores': z_scores,
                'categories': performance_categories,
                'avg_z_score': np.mean(z_scores),
                'consistency': consistency
            }
        
        return heat_data
