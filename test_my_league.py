"""Test script for YOUR specific ESPN Fantasy Football league

League ID: 1830148434 (your public league)

This script will:
1. Connect to your league using the espn-api library
2. Fetch all teams and rosters
3. Display your team's players
4. Format data for the Fantasy Football Toolkit
"""

from espn_api.football import League
import json

# Import authentication from config.py
try:
    from config import ESPN_S2, SWID, LEAGUE_ID, YEAR
except ImportError:
    print("❌ Error: config.py not found!")
    print("\nPlease create a config.py file with:")
    print("ESPN_S2 = 'your_espn_s2_cookie'")
    print("SWID = 'your_swid_cookie'")
    print("LEAGUE_ID = 1830148434")
    print("YEAR = 2024")
    exit(1)

# Position mapping
POSITION_MAP = {
    'QB': 'QB', 'RB': 'RB', 'WR': 'WR', 'TE': 'TE',
    'D/ST': 'D/ST', 'K': 'K', 'FLEX': 'FLEX', 'BE': 'BE'
}

def get_my_league_data():
    """
    Fetch data from your ESPN league with authentication
    """
    print(f"\n🏈 Connecting to league {LEAGUE_ID}...\n")
    
    try:
        # Connect to your league with authentication
        league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=ESPN_S2, swid=SWID)
        
        print(f"✅ Connected to: {league.settings.name}")
        print(f"   Teams: {len(league.teams)}")
        print(f"   Current Week: {league.current_week}")
        print("\n" + "="*70 + "\n")
        
        return league
        
    except Exception as e:
        print(f"❌ Error connecting to league: {e}")
        print("\nTroubleshooting:")
        print("  - Check your ESPN_S2 and SWID cookies in config.py")
        print("  - Make sure you're a member of this league")
        print("  - Try accessing the league in your browser first")
        return None

def display_all_teams(league):
    """
    Display all teams in the league
    """
    print("📋 ALL TEAMS IN YOUR LEAGUE:\n")
    
    for i, team in enumerate(league.teams, 1):
        print(f"{i}. {team.team_name}")
        print(f"   Owner: {team.owner}")
        print(f"   Record: {team.wins}-{team.losses}")
        print(f"   Points For: {team.points_for}")
        print()
    
    print("="*70 + "\n")

def display_team_roster(team, show_all=False):
    """
    Display a specific team's roster
    """
    print(f"⚡ {team.team_name} ROSTER:\n")
    
    roster = team.roster if show_all else [p for p in team.roster if p.lineupSlot != 'BE']
    
    for player in roster:
        pos = POSITION_MAP.get(player.position, player.position)
        print(f"  {pos:8} {player.name:25} ({player.proTeam})")
    
    print("\n" + "="*70 + "\n")

def export_for_app(league):
    """
    Format data for the Fantasy Football Toolkit web app
    """
    print("📦 EXPORTING DATA FOR WEB APP...\n")
    
    my_team = league.teams[0]  # Assuming first team is yours, adjust if needed
    
    players_data = []
    for player in my_team.roster:
        if player.lineupSlot != 'BE':  # Only active players
            players_data.append({
                'name': player.name,
                'position': POSITION_MAP.get(player.position, player.position),
                'team': player.proTeam,
                'projected': getattr(player, 'projected_points', 0),
                'actual': getattr(player, 'points', 0)
            })
    
    # Save to JSON file
    with open('my_players.json', 'w') as f:
        json.dump(players_data, f, indent=2)
    
    print(f"✅ Saved {len(players_data)} players to my_players.json")
    print("\nYou can now use this file with the Fantasy Football Toolkit!")
    print("="*70 + "\n")

if __name__ == "__main__":
    # Connect to league
    league = get_my_league_data()
    
    if league:
        # Display all teams
        display_all_teams(league)
        
        # Display your team's roster (first team by default)
        if league.teams:
            display_team_roster(league.teams[0], show_all=True)
        
        # Export data for the web app
        export_for_app(league)
    
    print("✨ Done!\n")
