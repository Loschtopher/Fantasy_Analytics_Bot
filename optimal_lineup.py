"""
Calculate optimal lineup from roster data
"""
from typing import Dict, List

# ESPN Lineup Slot IDs
LINEUP_SLOTS = {
    0: 'QB',
    2: 'RB',
    4: 'WR',
    6: 'TE',
    16: 'D/ST',
    17: 'K',
    23: 'FLEX',  # RB/WR/TE
    20: 'Bench',
    21: 'IR'
}

def calculate_optimal_lineup(roster_data: Dict) -> Dict:
    """
    Calculate the optimal lineup score from roster data
    
    Args:
        roster_data: Team roster data from ESPN API
        
    Returns:
        Dict with actual_score, optimal_score, and regret
    """
    if 'entries' not in roster_data:
        return {'actual_score': 0, 'optimal_score': 0, 'regret': 0}
    
    players = roster_data['entries']
    
    # Group players by their actual slot and score
    starters = []
    bench = []
    
    for entry in players:
        slot_id = entry.get('lineupSlotId')
        player_entry = entry.get('playerPoolEntry', {})
        points = player_entry.get('appliedStatTotal', 0)
        eligible_slots = player_entry.get('player', {}).get('eligibleSlots', [])
        player_name = player_entry.get('player', {}).get('fullName', 'Unknown')
        
        player_data = {
            'name': player_name,
            'slot_id': slot_id,
            'points': points,
            'eligible_slots': eligible_slots
        }
        
        if slot_id == 20:  # Bench
            bench.append(player_data)
        elif slot_id != 21:  # Not IR
            starters.append(player_data)
    
    # Calculate actual score (sum of starters)
    actual_score = sum(p['points'] for p in starters)
    
    # Calculate optimal score
    # For each starting slot, check if any bench player would have been better
    optimal_score = actual_score
    lineup_swaps = []
    
    for starter in starters:
        best_bench_upgrade = None
        max_upgrade = 0
        
        # Check if any bench player could play this slot and scored more
        for bench_player in bench:
            if starter['slot_id'] in bench_player['eligible_slots']:
                upgrade = bench_player['points'] - starter['points']
                if upgrade > max_upgrade:
                    max_upgrade = upgrade
                    best_bench_upgrade = bench_player
        
        if best_bench_upgrade:
            lineup_swaps.append({
                'slot': LINEUP_SLOTS.get(starter['slot_id'], f'Slot {starter["slot_id"]}'),
                'started': starter['name'],
                'started_points': starter['points'],
                'should_start': best_bench_upgrade['name'],
                'bench_points': best_bench_upgrade['points'],
                'regret': max_upgrade
            })
    
    # Total optimal is actual + all possible upgrades
    total_regret = sum(swap['regret'] for swap in lineup_swaps)
    optimal_score = actual_score + total_regret
    
    return {
        'actual_score': actual_score,
        'optimal_score': optimal_score,
        'regret': total_regret,
        'swaps': lineup_swaps
    }







