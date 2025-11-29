"""
Find the correct field for weekly fantasy points
"""
import sys
import os
import json
from dotenv import load_dotenv

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

load_dotenv()

from espn_api import ESPNAPI

def find_points_field():
    """Show all available point-related fields for a player"""
    
    api = ESPNAPI()
    endpoint = f"seasons/{api.season}/segments/0/leagues/{api.league_id}"
    
    # Get Week 7 data (user says Stafford scored 27.1 that week)
    print("="*70)
    print("  Analyzing Week 7 - Matthew Stafford (should be 27.1 pts)")
    print("="*70)
    print()
    
    params = {'view': ['mRoster', 'mMatchupScore'], 'scoringPeriodId': 7}
    week_data = api._make_request(endpoint, params)
    
    target_id = 12483  # Matthew Stafford
    
    if 'teams' in week_data:
        for team in week_data['teams']:
            roster = team.get('roster', {})
            entries = roster.get('entries', [])
            
            for entry in entries:
                player_info = entry.get('playerPoolEntry', {}).get('player', {})
                
                if player_info.get('id') == target_id:
                    print("Found Matthew Stafford in Week 7!")
                    print()
                    print("ALL FIELDS IN ENTRY:")
                    print("-" * 70)
                    
                    # Show the entire entry structure
                    for key, value in entry.items():
                        if key == 'playerPoolEntry':
                            print(f"\n{key}:")
                            player_entry = value
                            for pk, pv in player_entry.items():
                                if pk == 'player':
                                    print(f"  player: (skipping for brevity)")
                                elif 'stat' in pk.lower() or 'point' in pk.lower() or 'score' in pk.lower():
                                    print(f"  {pk}: {pv}")
                        else:
                            print(f"{key}: {value}")
                    
                    print()
                    print("="*70)
                    print("  Likely Point Fields")
                    print("="*70)
                    
                    player_entry = entry.get('playerPoolEntry', {})
                    print()
                    print(f"appliedStatTotal: {player_entry.get('appliedStatTotal', 'N/A')}")
                    
                    # Check if there's a playerStats or stats field
                    if 'stats' in player_entry:
                        print(f"stats: {player_entry.get('stats')}")
                    
                    # Check the entry level for any scoring
                    if 'playerPoolEntry' in entry:
                        pe = entry['playerPoolEntry']
                        for key in pe.keys():
                            if any(word in key.lower() for word in ['point', 'score', 'stat', 'total']):
                                print(f"{key}: {pe[key]}")
                    
                    print()
                    print("Based on user: Week 7 should show 27.1 points")
                    print(f"appliedStatTotal shows: {player_entry.get('appliedStatTotal', 'N/A')}")
                    print()
                    
                    return

    print("Could not find Matthew Stafford in Week 7 data")

if __name__ == "__main__":
    find_points_field()

