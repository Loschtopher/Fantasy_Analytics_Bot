"""
State Management for Fantasy Football Bot
Handles persistence of power rankings, ELO ratings, weekly scores, etc.
"""
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from config import STATE_FILE


class StateManager:
    """Manages persistent state for the fantasy football bot"""
    
    def __init__(self):
        self.state_file = STATE_FILE
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Load state from JSON file"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Return default state
        return {
            'power_rankings': {},
            'elo_ratings': {},
            'weekly_scores': {},
            'last_updated': None,
            'version': '1.0'
        }
    
    def _save_state(self):
        """Save state to JSON file"""
        self.state['last_updated'] = datetime.now().isoformat()
        
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"Failed to save state: {e}")
    
    def get_power_rankings(self) -> Dict:
        """Get current power rankings"""
        return self.state.get('power_rankings', {})
    
    def update_power_rankings(self, rankings: Dict):
        """Update power rankings"""
        self.state['power_rankings'] = rankings
        self._save_state()
    
    def get_elo_ratings(self) -> Dict:
        """Get current ELO ratings"""
        return self.state.get('elo_ratings', {})
    
    def update_elo_ratings(self, ratings: Dict):
        """Update ELO ratings"""
        self.state['elo_ratings'] = ratings
        self._save_state()
    
    def get_weekly_scores(self) -> Dict:
        """Get weekly scores history"""
        return self.state.get('weekly_scores', {})
    
    def update_weekly_scores(self, week: int, scores: Dict):
        """Update weekly scores for a specific week"""
        if 'weekly_scores' not in self.state:
            self.state['weekly_scores'] = {}
        
        self.state['weekly_scores'][str(week)] = scores
        self._save_state()
    
    def get_team_data(self, team_id: int) -> Dict:
        """Get cached team data"""
        return self.state.get('teams', {}).get(str(team_id), {})
    
    def update_team_data(self, team_id: int, data: Dict):
        """Update cached team data"""
        if 'teams' not in self.state:
            self.state['teams'] = {}
        
        self.state['teams'][str(team_id)] = data
        self._save_state()
    
    def get_last_update_time(self) -> Optional[str]:
        """Get last update timestamp"""
        return self.state.get('last_updated')
    
    def clear_old_data(self, weeks_to_keep: int = 17):
        """Clear old weekly data to keep state file manageable"""
        weekly_scores = self.state.get('weekly_scores', {})
        current_week = max([int(w) for w in weekly_scores.keys()] + [1])
        
        # Keep only recent weeks
        weeks_to_delete = []
        for week_str in weekly_scores.keys():
            week_num = int(week_str)
            if week_num < current_week - weeks_to_keep:
                weeks_to_delete.append(week_str)
        
        for week in weeks_to_delete:
            del weekly_scores[week]
        
        self._save_state()


