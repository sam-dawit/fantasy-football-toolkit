"""ESPN Fantasy Football API Guide

This file demonstrates how to use ESPN's hidden/undocumented API
to fetch NFL player data for fantasy football.

NO AUTHENTICATION NEEDED for public player data!
"""

import requests
import json

# ESPN API Base URLs
ESPN_API_BASE = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl"
ESPN_API_V2 = "https://fantasy.espn.com/apis/v3/games/ffl"


def get_all_nfl_players(year=2024, limit=50):
    """
    Fetch all NFL players available in ESPN Fantasy Football
    
    Args:
        year: NFL season year
        limit: Number of players to fetch (max varies, try 500+)
    
    Returns:
        List of player dictionaries with stats
    """
    url = f"{ESPN_API_V2}/seasons/{year}/players"
    
    params = {
        "view": "players_wl",  # wl = "watchlist" view, returns available players
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Process player data
        players = []
        for player in data[:limit]:  # Limit results
            player_info = {
                "id": player.get("id"),
                "name": player.get("fullName"),
                "position": player.get("defaultPositionId"),  # 1=QB, 2=RB, 3=WR, 4=TE
                "team": player.get("proTeamId"),
                "projected_points": player.get("player", {}).get("stats", [{}])[0].get("appliedTotal", 0)
            }
            players.append(player_info)
        
        return players
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching players: {e}")
        return []


def get_players_with_projections(league_id, year=2024, week=1):
    """
    Get players with weekly projections from a specific league
    
    Args:
        league_id: Your ESPN league ID (from URL)
        year: Season year
        week: Week number for projections
    
    Returns:
        List of players with projection data
    """
    url = f"{ESPN_API_BASE}/seasons/{year}/segments/0/leagues/{league_id}"
    
    params = {
        "view": "kona_player_info",
        "scoringPeriodId": week
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        return data.get("players", [])
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


def search_player_by_name(name, year=2024):
    """
    Search for a specific player by name
    
    Args:
        name: Player name (partial match works)
        year: Season year
    
    Returns:
        List of matching players
    """
    all_players = get_all_nfl_players(year=year, limit=500)
    
    # Filter by name (case-insensitive)
    matches = [p for p in all_players if name.lower() in p["name"].lower()]
    
    return matches


# Position ID mapping
POSITION_MAP = {
    1: "QB",
    2: "RB",
    3: "WR",
    4: "TE",
    5: "K",
    16: "D/ST"
}

# NFL Team ID mapping (partial - ESPN uses numeric IDs)
TEAM_MAP = {
    1: "ATL", 2: "BUF", 3: "CHI", 4: "CIN", 5: "CLE",
    6: "DAL", 7: "DEN", 8: "DET", 9: "GB", 10: "TEN",
    11: "IND", 12: "KC", 13: "LV", 14: "LAR", 15: "MIA",
    16: "MIN", 17: "NE", 18: "NO", 19: "NYG", 20: "NYJ",
    21: "PHI", 22: "ARI", 23: "PIT", 24: "LAC", 25: "SF",
    26: "SEA", 27: "TB", 28: "WAS", 29: "CAR", 30: "JAX",
    33: "BAL", 34: "HOU"
}


if __name__ == "__main__":
    # Example usage
    print("🏈 ESPN Fantasy Football API Demo\n")
    
    # 1. Get top 10 players
    print("Fetching top 10 NFL players...")
    players = get_all_nfl_players(year=2024, limit=10)
    
    for player in players:
        position = POSITION_MAP.get(player["position"], "UNK")
        team = TEAM_MAP.get(player["team"], "FA")
        print(f"{player['name']:25} | {position:4} | {team:3} | Proj: {player['projected_points']}")
    
    print("\n" + "="*60 + "\n")
    
    # 2. Search for a player
    print("Searching for 'Mahomes'...")
    results = search_player_by_name("Mahomes", year=2024)
    
    for player in results:
        position = POSITION_MAP.get(player["position"], "UNK")
        team = TEAM_MAP.get(player["team"], "FA")
        print(f"Found: {player['name']} - {position} - {team}")
    
    print("\n✅ API working! You can now integrate this into your app.")
