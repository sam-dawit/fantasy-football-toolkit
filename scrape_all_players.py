"""Scrape ALL available NFL players from ESPN Fantasy Football

This script fetches comprehensive player data including:
- All positions (QB, RB, WR, TE, K, D/ST)
- Player stats, projections, and ownership percentages
- Detailed position eligibility
- Export to JSON for web app use
"""

from espn_api.football import League
import json
from datetime import datetime

try:
    from config import ESPN_S2, SWID, LEAGUE_ID, YEAR
except ImportError:
    print("❌ Error: config.py not found!")
    print("Please create config.py with your ESPN credentials.")
    exit(1)

# Fantasy positions we want to track
POSITIONS = ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST']

def scrape_all_players(league, max_players=1000):
    """
    Scrape all available players from ESPN Fantasy
    
    Args:
        league: ESPN League object
        max_players: Maximum number of players to fetch (default 1000)
    
    Returns:
        Dictionary organized by position with player data
    """
    print(f"\n🔍 Scraping ALL NFL players from ESPN Fantasy...\n")
    print(f"📊 League: {league.settings.name}")
    print(f"📅 Season: {YEAR}\n")
    
    all_players = {
        'QB': [],
        'RB': [],
        'WR': [],
        'TE': [],
        'K': [],
        'D/ST': [],
        'metadata': {
            'scraped_at': datetime.now().isoformat(),
            'league_id': LEAGUE_ID,
            'season': YEAR,
            'total_players': 0
        }
    }
    
    try:
        # Fetch free agents (available players)
        print("⏳ Fetching free agents...")
        free_agents = league.free_agents(size=max_players)
        
        print(f"✅ Found {len(free_agents)} available players\n")
        print("=" * 80)
        
        for player in free_agents:
            position = player.position
            
            # Skip if not a fantasy-relevant position
            if position not in POSITIONS:
                continue
            
            # Extract player data
            player_data = {
                'player_id': player.playerId,
                'name': player.name,
                'position': position,
                'pro_team': player.proTeam,
                'projected_points': round(getattr(player, 'projected_points', 0), 2),
                'total_points': round(getattr(player, 'total_points', 0), 2),
                'avg_points': round(getattr(player, 'avg_points', 0), 2),
                'percent_owned': round(getattr(player, 'percent_owned', 0), 2),
                'percent_started': round(getattr(player, 'percent_started', 0), 2),
                'injury_status': getattr(player, 'injuryStatus', 'ACTIVE'),
                'eligible_slots': getattr(player, 'eligibleSlots', []),
            }
            
            # Add to the appropriate position list
            all_players[position].append(player_data)
        
        # Sort each position by projected points (descending)
        for pos in POSITIONS:
            all_players[pos].sort(
                key=lambda x: x['projected_points'], 
                reverse=True
            )
        
        # Update metadata
        total = sum(len(all_players[pos]) for pos in POSITIONS)
        all_players['metadata']['total_players'] = total
        
        # Print summary
        print("\n📈 PLAYER COUNT BY POSITION:\n")
        for pos in POSITIONS:
            count = len(all_players[pos])
            top_player = all_players[pos][0]['name'] if all_players[pos] else 'None'
            print(f"{pos:6} {count:4} players  (Top: {top_player})")
        
        print(f"\n{'='*80}")
        print(f"\n✅ Total: {total} players scraped")
        
        return all_players
        
    except Exception as e:
        print(f"❌ Error scraping players: {e}")
        return None

def save_to_json(data, filename='all_nfl_players.json'):
    """
    Save player data to JSON file
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n💾 Saved to {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving to JSON: {e}")
        return False

def display_top_players(all_players, position='QB', limit=10):
    """
    Display top players for a specific position
    """
    print(f"\n🏆 TOP {limit} {position}s:\n")
    print(f"{'RANK':<6}{'NAME':<25}{'TEAM':<6}{'PROJ':<8}{'OWN%':<8}{'START%':<8}")
    print("=" * 80)
    
    for i, player in enumerate(all_players[position][:limit], 1):
        print(
            f"{i:<6}"
            f"{player['name']:<25}"
            f"{player['pro_team']:<6}"
            f"{player['projected_points']:<8.1f}"
            f"{player['percent_owned']:<8.1f}"
            f"{player['percent_started']:<8.1f}"
        )

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🏈 ESPN FANTASY FOOTBALL PLAYER SCRAPER")
    print("="*80 + "\n")
    
    # Connect to league
    try:
        league = League(
            league_id=LEAGUE_ID,
            year=YEAR,
            espn_s2=ESPN_S2,
            swid=SWID
        )
    except Exception as e:
        print(f"❌ Error connecting to league: {e}")
        print("\nMake sure your config.py has valid credentials.")
        exit(1)
    
    # Scrape all players
    all_players = scrape_all_players(league, max_players=1000)
    
    if all_players:
        # Save to JSON
        save_to_json(all_players)
        
        # Display top players by position
        for position in ['QB', 'RB', 'WR', 'TE']:
            display_top_players(all_players, position, limit=10)
        
        print("\n" + "="*80)
        print("✨ Scraping complete!")
        print("="*80 + "\n")
        print("📂 Data saved to: all_nfl_players.json")
        print("💡 Use this file in your web app to display all available players!")
        print("\n")
