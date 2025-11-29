"""
Find where actual player fantasy points are stored
Check matchup data which has the real scores
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

def find_actual_points():
    """Find the actual fantasy points for Stafford"""
    
    api = ESPNAPI()
    endpoint = f"seasons/{api.season}/segments/0/leagues/{api.league_id}"
    
    target_id = 12483  # Matthew Stafford
    target_name = "Matthew Stafford"
    
    print("="*70)
    print(f"  Finding Actual Points for {target_name}")
    print("="*70)
    print()
    
    # Check multiple weeks to see pattern
    for week_num in [7, 10]:
        print(f"\n{'='*70}")
        print(f"  Week {week_num}")
        print(f"{'='*70}\n")
        
        # Get roster data with more views
        params = {
            'view': ['mMatchup', 'mRoster', 'mTeam', 'mMatchupScore'],
            'scoringPeriodId': week_num
        }
        
        week_data = api._make_request(endpoint, params)
        
        # Find which team has Stafford
        team_with_stafford = None
        
        if 'teams' in week_data:
            for team in week_data['teams']:
                roster = team.get('roster', {})
                entries = roster.get('entries', [])
                
                for entry in entries:
                    player_info = entry.get('playerPoolEntry', {}).get('player', {})
                    if player_info.get('id') == target_id:
                        team_with_stafford = team
                        team_id = team.get('id')
                        team_name = team.get('name', 'Unknown')
                        
                        print(f"Found {target_name} on: {team_name} (ID: {team_id})")
                        print()
                        
                        # Show roster entry info
                        player_entry = entry.get('playerPoolEntry', {})
                        print(f"appliedStatTotal (roster): {player_entry.get('appliedStatTotal', 'N/A')}")
                        
                        # Check if there's actual scoring in the entry
                        if 'playerPoolEntry' in entry:
                            pe = entry['playerPoolEntry']
                            if 'appliedStats' in pe:
                                print(f"appliedStats: {pe.get('appliedStats')}")
                        
                        break
                
                if team_with_stafford:
                    break
        
        # Now check matchup data for this team
        if 'schedule' in week_data:
            for matchup in week_data['schedule']:
                matchup_period = matchup.get('matchupPeriodId')
                
                if matchup_period != week_num:
                    continue
                
                home_team_id = matchup.get('home', {}).get('teamId')
                away_team_id = matchup.get('away', {}).get('teamId')
                
                if home_team_id == team_with_stafford.get('id'):
                    print(f"\nMatchup Data (Home Team):")
                    home = matchup.get('home', {})
                    print(f"  Total Team Points: {home.get('totalPoints', 'N/A')}")
                    
                    # Check rosterForCurrentScoringPeriod
                    if 'rosterForCurrentScoringPeriod' in home:
                        print(f"\n  Roster Entries:")
                        for entry in home['rosterForCurrentScoringPeriod'].get('entries', []):
                            player_info = entry.get('playerPoolEntry', {}).get('player', {})
                            if player_info.get('id') == target_id:
                                player_entry = entry.get('playerPoolEntry', {})
                                print(f"    {target_name}:")
                                print(f"      appliedStatTotal: {player_entry.get('appliedStatTotal', 'N/A')}")
                                
                                # Look for actual points
                                for key, value in player_entry.items():
                                    if 'stat' in key.lower() or 'point' in key.lower():
                                        print(f"      {key}: {value}")
                
                elif away_team_id == team_with_stafford.get('id'):
                    print(f"\nMatchup Data (Away Team):")
                    away = matchup.get('away', {})
                    print(f"  Total Team Points: {away.get('totalPoints', 'N/A')}")
                    
                    if 'rosterForCurrentScoringPeriod' in away:
                        print(f"\n  Roster Entries:")
                        for entry in away['rosterForCurrentScoringPeriod'].get('entries', []):
                            player_info = entry.get('playerPoolEntry', {}).get('player', {})
                            if player_info.get('id') == target_id:
                                player_entry = entry.get('playerPoolEntry', {})
                                print(f"    {target_name}:")
                                print(f"      appliedStatTotal: {player_entry.get('appliedStatTotal', 'N/A')}")
                                
                                for key, value in player_entry.items():
                                    if 'stat' in key.lower() or 'point' in key.lower():
                                        print(f"      {key}: {value}")
    
    print()
    print("="*70)
    print("  Summary")
    print("="*70)
    print()
    print("User says Week 7 Stafford scored: 27.1 points")
    print("We're seeing appliedStatTotal: 36.2")
    print()
    print("This confirms appliedStatTotal is NOT the actual fantasy points!")
    print("Need to find the correct field...")

if __name__ == "__main__":
    find_actual_points()

