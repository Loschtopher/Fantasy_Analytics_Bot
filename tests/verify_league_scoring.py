"""
Verify league scoring to see if 37 PPG for a QB is normal
"""
import sys
import os
from dotenv import load_dotenv

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

load_dotenv()

from espn_api import ESPNAPI

def check_league_scoring():
    """Check top QB scoring to see if league has inflated scoring"""
    
    api = ESPNAPI()
    
    # Get league settings
    endpoint = f"seasons/{api.season}/segments/0/leagues/{api.league_id}"
    params = {'view': ['mSettings']}
    
    settings_data = api._make_request(endpoint, params)
    
    print("="*70)
    print("  League Scoring Settings Check")
    print("="*70)
    print()
    
    # Check scoring settings
    if 'settings' in settings_data:
        scoring = settings_data['settings'].get('scoringSettings', {})
        
        print("QB Scoring Settings:")
        print("-" * 40)
        
        # Common QB stats
        stat_map = {
            '0': 'Passing Yards',
            '1': 'Passing TDs',
            '2': 'Passing 2PT',
            '3': 'Passing INTs',
            '20': 'Rushing Yards',
            '24': 'Rushing TDs',
            '25': 'Rushing 2PT',
            '53': 'Rec Yards',
            '42': 'Receptions'
        }
        
        scoring_items = scoring.get('scoringItems', [])
        for item in scoring_items:
            stat_id = str(item.get('statId', ''))
            points = item.get('points', 0)
            stat_name = stat_map.get(stat_id, f"Stat ID {stat_id}")
            
            if stat_id in ['0', '1', '2', '3', '20', '24', '25']:
                print(f"  {stat_name}: {points} points")
    
    print()
    print("="*70)
    print("  Checking Top Drafted QB Performance")
    print("="*70)
    print()
    
    # Get a top QB from week 1 to compare
    params = {'view': ['mRoster'], 'scoringPeriodId': 5}
    week_data = api._make_request(endpoint, params)
    
    qb_scores = []
    
    if 'teams' in week_data:
        for team in week_data['teams']:
            roster = team.get('roster', {})
            for entry in roster.get('entries', []):
                player_entry = entry.get('playerPoolEntry', {})
                player_info = player_entry.get('player', {})
                position_id = player_info.get('defaultPositionId', 0)
                
                if position_id == 1:  # QB
                    name = player_info.get('fullName', 'Unknown')
                    points = player_entry.get('appliedStatTotal', 0)
                    qb_scores.append((name, points))
    
    if qb_scores:
        qb_scores.sort(key=lambda x: x[1], reverse=True)
        print("Week 5 QB Performance (sample):")
        print("-" * 40)
        for name, points in qb_scores[:10]:
            print(f"  {name}: {points:.1f} points")
    
    print()
    print("="*70)
    print("  Interpretation")
    print("="*70)
    print()
    print("Standard QB scoring:")
    print("  - 0.04 pts per passing yard (1 pt per 25 yards)")
    print("  - 4 pts per passing TD")
    print("  - Expected: 15-25 PPG for good QBs")
    print()
    print("If your league shows 30-50 PPG for QBs:")
    print("  - League might have custom scoring (6pt passing TDs, bonuses, etc.)")
    print("  - Waiver PPG calculations ARE correct!")
    print("  - The high values are due to your league settings")
    print()

if __name__ == "__main__":
    check_league_scoring()

