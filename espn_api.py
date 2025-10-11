"""
ESPN Fantasy Football API Client
Handles authentication and data retrieval from ESPN's private API
"""
import requests
import json
from typing import Dict, List, Optional, Any
from config import ESPN_LEAGUE_ID, ESPN_SWID, ESPN_S2, ESPN_BASE_URL, ESPN_SEASON


class ESPNAPI:
    """Client for ESPN Fantasy Football API"""
    
    def __init__(self):
        self.league_id = ESPN_LEAGUE_ID
        self.swid = ESPN_SWID
        self.s2 = ESPN_S2
        self.base_url = ESPN_BASE_URL
        self.season = ESPN_SEASON
        
        # Set up session with cookies
        self.session = requests.Session()
        self.session.cookies.set('SWID', self.swid)
        self.session.cookies.set('espn_s2', self.s2)
        
        # Set headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make authenticated request to ESPN API"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {}
    
    def get_league_info(self) -> Dict:
        """Get basic league information"""
        endpoint = f"seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {'view': 'mTeam'}
        return self._make_request(endpoint, params)
    
    def get_teams(self) -> List[Dict]:
        """Get all teams in the league"""
        endpoint = f"seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {'view': 'mTeam'}
        
        data = self._make_request(endpoint, params)
        if 'teams' in data:
            return data['teams']
        return []
    
    def get_matchups(self, week: int) -> List[Dict]:
        """Get matchups for a specific week"""
        endpoint = f"seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {
            'view': ['mMatchup', 'mMatchupScore']
        }
        
        data = self._make_request(endpoint, params)
        if 'schedule' in data:
            return [matchup for matchup in data['schedule'] 
                   if matchup.get('matchupPeriodId') == week]
        return []
    
    def get_team_scores(self, week: Optional[int] = None) -> Dict[int, List[float]]:
        """Get all team scores for a week or entire season"""
        teams_data = self.get_teams()
        team_scores = {}
        
        for team in teams_data:
            team_id = team['id']
            scores = []
            
            # Get scores for each week
            if week:
                # Single week
                matchups = self.get_matchups(week)
                for matchup in matchups:
                    if matchup['home']['teamId'] == team_id:
                        scores.append(matchup['home']['totalPoints'])
                    elif matchup['away']['teamId'] == team_id:
                        scores.append(matchup['away']['totalPoints'])
            else:
                # Entire season
                for week_num in range(1, 18):  # Assume max 17 weeks
                    matchups = self.get_matchups(week_num)
                    for matchup in matchups:
                        if matchup['home']['teamId'] == team_id:
                            scores.append(matchup['home']['totalPoints'])
                        elif matchup['away']['teamId'] == team_id:
                            scores.append(matchup['away']['totalPoints'])
            
            team_scores[team_id] = scores
        
        return team_scores
    
    def get_current_week(self) -> int:
        """Get the current matchup period"""
        endpoint = f"seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {'view': 'mStatus'}
        
        data = self._make_request(endpoint, params)
        if 'status' in data:
            return data['status'].get('currentMatchupPeriod', 1)
        return 1
    
    def get_playoff_teams(self) -> int:
        """Get number of playoff teams"""
        endpoint = f"seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {'view': 'mSettings'}
        
        data = self._make_request(endpoint, params)
        if 'settings' in data:
            return data['settings'].get('playoffTeamCount', 6)
        return 6
    
    def get_playoff_start_week(self) -> int:
        """Get playoff start week"""
        endpoint = f"seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {'view': 'mSettings'}
        
        data = self._make_request(endpoint, params)
        if 'settings' in data:
            return data['settings'].get('playoffMatchupPeriodId', 15)
        return 15
    
    def get_team_roster(self, team_id: int, week: int) -> Dict:
        """Get team roster for a specific week"""
        endpoint = f"seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {
            'view': ['mRoster', 'mMatchup'],
            'scoringPeriodId': week
        }
        
        data = self._make_request(endpoint, params)
        # This would need to be enhanced based on ESPN API structure
        return data
    
    def get_player_projections(self, week: int) -> Dict:
        """Get player projections for a week"""
        endpoint = f"seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {
            'view': 'mMatchup',
            'scoringPeriodId': week
        }
        
        data = self._make_request(endpoint, params)
        return data
    
    def get_league_settings(self) -> Dict:
        """Get league settings and scoring"""
        endpoint = f"seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {'view': 'mSettings'}
        
        data = self._make_request(endpoint, params)
        return data.get('settings', {})
    
    def get_team_stats(self, team_id: int) -> Dict:
        """Get detailed team statistics"""
        teams = self.get_teams()
        for team in teams:
            if team['id'] == team_id:
                return team
        return {}
    
    def get_weekly_standings(self, week: int) -> List[Dict]:
        """Get standings for a specific week"""
        teams = self.get_teams()
        standings = []
        
        for team in teams:
            standings.append({
                'team_id': team['id'],
                'name': team.get('name', 'Unknown'),
                'abbrev': team.get('abbrev', 'UNK'),
                'wins': team.get('record', {}).get('wins', 0),
                'losses': team.get('record', {}).get('losses', 0),
                'ties': team.get('record', {}).get('ties', 0),
                'points_for': team.get('pointsFor', 0),
                'points_against': team.get('pointsAgainst', 0)
            })
        
        # Sort by wins, then points for
        standings.sort(key=lambda x: (x['wins'], x['points_for']), reverse=True)
        return standings
