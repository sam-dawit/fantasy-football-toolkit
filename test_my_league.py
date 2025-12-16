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

# Your league configuration
LEAGUE_ID = 1830148434
YEAR = 2024

# Position mapping
POSITION_MAP = {
    'QB': 'QB', 'RB': 'RB', 'WR': 'WR', 'TE': 'TE',
    'D/ST': 'D/ST', 'K': 'K', 'FLEX': 'FLEX', 'BE': 'BE'
}

def get_my_league_data():
    """
    Fetch data from your public ESPN league
    """
    print(f"\n🏈 Connecting to league {LEAGUE_ID}...\n")
    
    try:
        # Connect to your public league (no auth needed!)
        league = League(league_id=LEAGUE_ID, year=YEAR)
        
        print(f"✅ Connected to: {league.settings.name}")
        print(f"   Teams: {len(league.teams)}")
        print(f"   Current Week: {league.current_week}")
        print("\n" + "="*70 + "\n")
        
        return league
        
    except Exception as e:
        print(f"❌ Error connecting to league: {e}")
        print("\nTroubleshooting:")
        print("  - Make sure the league is PUBLIC")
        print("  - Check the league ID is correct")
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
    print(f"🏆 {team.team_name.upper()} - ROSTER\n")
    print(f"Owner: {team.owner}")
    print(f"Record: {team.wins}-{team.losses} | Points: {team.points_for}")
    print("\n" + "-"*70 + "\n")
    
    # Get roster
    roster = team.roster
    
    if not roster:
        print("❌ No players found on this roster")
        return []
    
    players_for_app = []
    
    print(f"{'PLAYER':<25} {'POS':<6} {'TEAM':<6} {'PROJ':<8} {'ACTUAL'}")
    print("-"*70)
    
    for player in roster:
        # Get player info
        name = player.name
        position = player.position
        pro_team = player.proTeam if hasattr(player, 'proTeam') else 'FA'
        
        # Get projected points for current week
        proj_points = player.projected_points if hasattr(player, 'projected_points') else 0
        actual_points = player.points if hasattr(player, 'points') else 0
        
        print(f"{name:<25} {position:<6} {pro_team:<6} {proj_points:<8.1f} {actual_points:.1f}")
        
        # Format for your Fantasy Football Toolkit
        player_data = {
            "name": name,
            "position": position,
            "team": pro_team,
            "projected_points": proj_points,
            "last_3_avg": actual_points,  # Using current week as placeholder
            "opponent_def_rank": 16  # Default middle value
        }
        players_for_app.append(player_data)
    
    print("\n" + "="*70 + "\n")
    
    return players_for_app


def export_for_app(players, filename="my_players.json"):
    """
    Export player data in format ready for your app
    """
    with open(filename, 'w') as f:
        json.dump(players, f, indent=2)
    
    print(f"\n💾 Exported {len(players)} players to {filename}")
    print("   You can now use this data in your Fantasy Football Toolkit!\n")


if __name__ == "__main__":
    # Connect to your league
    league = get_my_league_data()
    
    if league:
        # Show all teams
        display_all_teams(league)
        
        # Get YOUR team (first team for now - you can change this)
        your_team = league.teams[0]  # Change index if needed
        
        print(f"\n🎯 Showing roster for: {your_team.team_name}")
        print(f"   (If this isn't your team, check the team list above)\n")
        
        # Display your roster
        players = display_team_roster(your_team)
        
        # Export for your app
        if players:
            export_for_app(players)
            
            print("\n✅ SUCCESS! Next steps:")
            print("   1. Check my_players.json for your exported roster")
            print("   2. You can now integrate this into app.py")
            print("   3. Run 'python app.py' to use your Fantasy Toolkit\n")
