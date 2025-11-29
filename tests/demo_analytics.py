"""
Demo script showing how the analytics functions work
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analytics import FantasyAnalytics
import numpy as np

def demo_power_rankings():
    """Demonstrate power ranking calculations"""
    print("🏆 Power Rankings Demo")
    print("=" * 50)
    
    analytics = FantasyAnalytics()
    
    # Example team data
    teams = [
        {
            'name': 'Team Alpha',
            'wins': 8,
            'losses': 2,
            'ties': 0,
            'points_for': 1250.5,
            'points_against': 1100.2,
            'recent_scores': [145.2, 138.7, 132.1],
            'all_scores': [145.2, 138.7, 132.1, 128.9, 125.4, 122.8, 119.5, 115.2, 112.3, 108.9]
        },
        {
            'name': 'Team Beta',
            'wins': 6,
            'losses': 4,
            'ties': 0,
            'points_for': 1200.0,
            'points_against': 1150.0,
            'recent_scores': [125.4, 118.9, 142.3],
            'all_scores': [125.4, 118.9, 142.3, 115.7, 122.1, 119.8, 116.4, 113.2, 110.8, 107.5]
        },
        {
            'name': 'Team Gamma',
            'wins': 4,
            'losses': 6,
            'ties': 0,
            'points_for': 1050.0,
            'points_against': 1200.0,
            'recent_scores': [98.7, 105.2, 112.8],
            'all_scores': [98.7, 105.2, 112.8, 108.9, 104.5, 101.2, 97.8, 94.3, 91.6, 88.9]
        }
    ]
    
    # Calculate power scores
    team_scores = []
    for team in teams:
        power_score = analytics.calculate_power_score(team)
        team_scores.append((team['name'], power_score, team))
    
    # Sort by power score
    team_scores.sort(key=lambda x: x[1], reverse=True)
    
    print("Power Rankings:")
    for rank, (name, score, team_data) in enumerate(team_scores, 1):
        win_pct = (team_data['wins'] + 0.5 * team_data['ties']) / (team_data['wins'] + team_data['losses'] + team_data['ties'])
        print(f"{rank}. {name}")
        print(f"   Record: {team_data['wins']}-{team_data['losses']}-{team_data['ties']} ({win_pct:.3f})")
        print(f"   PF: {team_data['points_for']:.1f} | PA: {team_data['points_against']:.1f}")
        print(f"   Power Score: {score:.3f}")
        print()

def demo_luck_analysis():
    """Demonstrate luck analysis calculations"""
    print("🍀 Luck Analysis Demo")
    print("=" * 50)
    
    analytics = FantasyAnalytics()
    
    teams = [
        {'name': 'Team Alpha', 'wins': 8, 'losses': 2, 'ties': 0, 'pf': 1250.5, 'pa': 1100.2},
        {'name': 'Team Beta', 'wins': 6, 'losses': 4, 'ties': 0, 'pf': 1200.0, 'pa': 1150.0},
        {'name': 'Team Gamma', 'wins': 4, 'losses': 6, 'ties': 0, 'pf': 1050.0, 'pa': 1200.0},
    ]
    
    for team in teams:
        wins = team['wins']
        losses = team['losses']
        ties = team['ties']
        pf = team['pf']
        pa = team['pa']
        
        total_games = wins + losses + ties
        actual_wins = wins + 0.5 * ties
        expected_wins = analytics.calculate_pythagorean_expectation(pf, pa, total_games)
        luck = actual_wins - expected_wins
        
        status = "🍀 Lucky" if luck > 0 else "😈 Cursed" if luck < -0.5 else "⚖️ Neutral"
        
        print(f"{team['name']}:")
        print(f"  Record: {wins}-{losses}-{ties}")
        print(f"  Expected Wins: {expected_wins:.1f}")
        print(f"  Actual Wins: {actual_wins:.1f}")
        print(f"  Luck: {luck:+.1f} {status}")
        print()

def demo_boom_bust():
    """Demonstrate boom/bust analysis"""
    print("💥 Boom/Bust Analysis Demo")
    print("=" * 50)
    
    analytics = FantasyAnalytics()
    
    # Example scoring patterns
    teams = [
        {
            'name': 'Consistent Team',
            'scores': [120, 125, 118, 122, 124, 119, 121, 123, 117, 120]
        },
        {
            'name': 'Boom/Bust Team',
            'scores': [150, 95, 145, 88, 160, 92, 155, 85, 148, 90]
        },
        {
            'name': 'Average Team',
            'scores': [110, 115, 108, 112, 118, 105, 120, 107, 114, 109]
        }
    ]
    
    for team in teams:
        metrics = analytics.calculate_boom_bust_metrics(team['scores'])
        
        print(f"{team['name']}:")
        print(f"  Ceiling (P80): {metrics['ceiling']:.1f}")
        print(f"  Floor (P20): {metrics['floor']:.1f}")
        print(f"  Spread: {metrics['spread']:.1f}")
        print(f"  Consistency: {metrics['consistency']:.3f}")
        print(f"  Avg Score: {np.mean(team['scores']):.1f}")
        print()

def demo_elo():
    """Demonstrate ELO rating updates"""
    print("⚡ ELO Rating Demo")
    print("=" * 50)
    
    analytics = FantasyAnalytics()
    
    # Initial ratings
    elo_ratings = {
        'team1': 1500,
        'team2': 1500
    }
    
    print("Initial ELO Ratings:")
    print(f"Team 1: {elo_ratings['team1']}")
    print(f"Team 2: {elo_ratings['team2']}")
    print()
    
    # Simulate some matchups
    matchups = [
        {'team1_score': 145.2, 'team2_score': 132.1},  # Team 1 wins
        {'team1_score': 118.5, 'team2_score': 125.4},  # Team 2 wins
        {'team1_score': 142.8, 'team2_score': 138.9},  # Team 1 wins
    ]
    
    for i, matchup in enumerate(matchups, 1):
        new_elo1, new_elo2 = analytics.update_elo_ratings(
            'team1', 'team2', 
            matchup['team1_score'], 
            matchup['team2_score'], 
            elo_ratings
        )
        
        change1 = new_elo1 - elo_ratings['team1']
        change2 = new_elo2 - elo_ratings['team2']
        
        print(f"Matchup {i}: Team 1 {matchup['team1_score']:.1f} - {matchup['team2_score']:.1f} Team 2")
        print(f"  Team 1: {elo_ratings['team1']:.0f} → {new_elo1:.0f} ({change1:+.0f})")
        print(f"  Team 2: {elo_ratings['team2']:.0f} → {new_elo2:.0f} ({change2:+.0f})")
        print()
        
        # Update ratings for next matchup
        elo_ratings['team1'] = new_elo1
        elo_ratings['team2'] = new_elo2

def main():
    """Run all demos"""
    print("🎮 Fantasy Football Analytics Demo")
    print("=" * 60)
    print()
    
    demo_power_rankings()
    print()
    demo_luck_analysis()
    print()
    demo_boom_bust()
    print()
    demo_elo()
    
    print("✅ Demo complete!")
    print("\nTo run the actual bot:")
    print("1. Set up your .env file with ESPN credentials")
    print("2. Run: python run_bot.py")

if __name__ == "__main__":
    main()


