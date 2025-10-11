"""
The Odds API Client - Fetch real sportsbook odds for player props
"""
import requests
import os
from typing import Dict, List, Optional
from datetime import datetime

class OddsAPI:
    """Client for The Odds API - fetches real sportsbook odds"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ODDS_API_KEY')
        self.base_url = "https://api.the-odds-api.com/v4"
        self.sport = "americanfootball_nfl"
        
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request to The Odds API"""
        if not self.api_key:
            raise ValueError("ODDS_API_KEY not set in environment")
        
        url = f"{self.base_url}/{endpoint}"
        default_params = {'apiKey': self.api_key}
        
        if params:
            default_params.update(params)
        
        try:
            response = requests.get(url, params=default_params, timeout=10)
            response.raise_for_status()
            
            # Check remaining requests
            remaining = response.headers.get('x-requests-remaining')
            if remaining:
                print(f"📊 Odds API requests remaining: {remaining}")
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Odds API error: {e}")
            return None
    
    def get_player_props(self, market: str = 'player_touchdown_scorer') -> Optional[List[Dict]]:
        """
        Get player prop odds for anytime touchdown scorers
        
        Args:
            market: Type of prop (default: 'player_touchdown_scorer')
            
        Returns:
            List of events with player props from multiple sportsbooks
        """
        endpoint = f"sports/{self.sport}/events"
        params = {
            'regions': 'us',
            'markets': market,
            'oddsFormat': 'american'
        }
        
        events = self._make_request(endpoint, params)
        
        if not events:
            return None
        
        # Get detailed odds for each event
        all_props = []
        for event in events[:5]:  # Limit to 5 games to save API calls
            event_id = event.get('id')
            if event_id:
                props = self._get_event_props(event_id, market)
                if props:
                    all_props.append({
                        'event': event,
                        'props': props
                    })
        
        return all_props
    
    def _get_event_props(self, event_id: str, market: str) -> Optional[Dict]:
        """Get prop odds for a specific event"""
        endpoint = f"sports/{self.sport}/events/{event_id}/odds"
        params = {
            'regions': 'us',
            'markets': market,
            'oddsFormat': 'american'
        }
        
        return self._make_request(endpoint, params)
    
    @staticmethod
    def american_to_probability(odds: int) -> float:
        """
        Convert American odds to implied probability
        
        Args:
            odds: American odds (e.g., -150, +200)
            
        Returns:
            Implied probability as decimal (0.0 - 1.0)
        """
        if odds < 0:
            # Favorite (negative odds)
            return abs(odds) / (abs(odds) + 100)
        else:
            # Underdog (positive odds)
            return 100 / (odds + 100)
    
    @staticmethod
    def probability_to_american(prob: float) -> int:
        """
        Convert probability to American odds
        
        Args:
            prob: Probability as decimal (0.0 - 1.0)
            
        Returns:
            American odds
        """
        if prob >= 0.5:
            # Favorite (negative odds)
            return int(-100 * prob / (1 - prob))
        else:
            # Underdog (positive odds)
            return int(100 * (1 - prob) / prob)
    
    def get_best_td_props(self, limit: int = 10) -> List[Dict]:
        """
        Get best TD scorer props across all sportsbooks
        
        Returns:
            List of players with their best odds
        """
        props = self.get_player_props()
        
        if not props:
            return []
        
        # Aggregate all player props
        player_odds = {}
        
        for game in props:
            bookmakers = game.get('props', {}).get('bookmakers', [])
            
            for bookmaker in bookmakers:
                book_name = bookmaker.get('title', 'Unknown')
                markets = bookmaker.get('markets', [])
                
                for market in markets:
                    if market.get('key') == 'player_touchdown_scorer':
                        outcomes = market.get('outcomes', [])
                        
                        for outcome in outcomes:
                            player_name = outcome.get('description', 'Unknown')
                            odds = outcome.get('price')
                            
                            if player_name and odds:
                                if player_name not in player_odds:
                                    player_odds[player_name] = []
                                
                                player_odds[player_name].append({
                                    'bookmaker': book_name,
                                    'odds': odds,
                                    'probability': self.american_to_probability(odds)
                                })
        
        # Find best odds for each player
        best_props = []
        for player, odds_list in player_odds.items():
            # Sort by best odds (highest probability for favorites, lowest for underdogs)
            odds_list.sort(key=lambda x: x['probability'], reverse=True)
            best = odds_list[0]
            
            best_props.append({
                'player': player,
                'best_odds': best['odds'],
                'best_book': best['bookmaker'],
                'probability': best['probability'],
                'all_books': odds_list[:3]  # Top 3 books
            })
        
        # Sort by probability (most likely to score)
        best_props.sort(key=lambda x: x['probability'], reverse=True)
        
        return best_props[:limit]
    
    def get_longshot_td_props(self, limit: int = 10, min_odds: int = 200) -> List[Dict]:
        """
        Get longshot TD scorer props (high payout underdogs)
        
        Args:
            limit: Number of longshots to return
            min_odds: Minimum odds to be considered a longshot (default: +200)
            
        Returns:
            List of longshot players
        """
        props = self.get_player_props()
        
        if not props:
            return []
        
        # Aggregate all player props
        player_odds = {}
        
        for game in props:
            bookmakers = game.get('props', {}).get('bookmakers', [])
            
            for bookmaker in bookmakers:
                book_name = bookmaker.get('title', 'Unknown')
                markets = bookmaker.get('markets', [])
                
                for market in markets:
                    if market.get('key') == 'player_touchdown_scorer':
                        outcomes = market.get('outcomes', [])
                        
                        for outcome in outcomes:
                            player_name = outcome.get('description', 'Unknown')
                            odds = outcome.get('price')
                            
                            # Only include longshots (positive odds above threshold)
                            if player_name and odds and odds >= min_odds:
                                if player_name not in player_odds:
                                    player_odds[player_name] = []
                                
                                player_odds[player_name].append({
                                    'bookmaker': book_name,
                                    'odds': odds,
                                    'probability': self.american_to_probability(odds)
                                })
        
        # Find best odds for each longshot
        longshot_props = []
        for player, odds_list in player_odds.items():
            # Sort by best odds (highest for longshots = most positive)
            odds_list.sort(key=lambda x: x['odds'], reverse=True)
            best = odds_list[0]
            
            longshot_props.append({
                'player': player,
                'best_odds': best['odds'],
                'best_book': best['bookmaker'],
                'probability': best['probability'],
                'all_books': odds_list[:3]
            })
        
        # Sort by odds (biggest longshots first)
        longshot_props.sort(key=lambda x: x['best_odds'], reverse=True)
        
        return longshot_props[:limit]

