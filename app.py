from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Sample player data (in a real app, this would come from an API)
SAMPLE_PLAYERS = [
    {"name": "Patrick Mahomes", "position": "QB", "team": "KC", 
     "projected_points": 24.5, "last_3_avg": 26.2, "opponent_def_rank": 28},
    {"name": "Josh Allen", "position": "QB", "team": "BUF", 
     "projected_points": 23.8, "last_3_avg": 22.1, "opponent_def_rank": 15},
    {"name": "Christian McCaffrey", "position": "RB", "team": "SF", 
     "projected_points": 22.3, "last_3_avg": 24.8, "opponent_def_rank": 12},
    {"name": "Derrick Henry", "position": "RB", "team": "BAL", 
     "projected_points": 18.5, "last_3_avg": 19.3, "opponent_def_rank": 20},
    {"name": "CeeDee Lamb", "position": "WR", "team": "DAL", 
     "projected_points": 16.8, "last_3_avg": 18.2, "opponent_def_rank": 22},
    {"name": "Tyreek Hill", "position": "WR", "team": "MIA", 
     "projected_points": 17.2, "last_3_avg": 15.9, "opponent_def_rank": 18},
    {"name": "Travis Kelce", "position": "TE", "team": "KC", 
     "projected_points": 14.5, "last_3_avg": 13.8, "opponent_def_rank": 25},
    {"name": "George Kittle", "position": "TE", "team": "SF", 
     "projected_points": 12.3, "last_3_avg": 11.5, "opponent_def_rank": 16},
]

def calculate_player_score(player):
    """
    Calculate a composite score for each player based on:
    - Projected points (weight: 0.4)
    - Last 3 game average (weight: 0.35)
    - Opponent defense rank (weight: 0.25, lower rank = easier matchup)
    """
    w1 = 0.4  # projected points weight
    w2 = 0.35  # recent performance weight
    w3 = 0.25  # matchup weight
    
    # For opponent defense, invert the rank (lower rank = higher score)
    # Normalize to 0-32 scale where higher = easier matchup
    matchup_score = (32 - player['opponent_def_rank'])
    
    score = (
        w1 * player['projected_points'] +
        w2 * player['last_3_avg'] +
        w3 * matchup_score
    )
    
    return round(score, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/players', methods=['GET'])
def get_players():
    """Return all available players"""
    return jsonify(SAMPLE_PLAYERS)

@app.route('/api/analyze', methods=['POST'])
def analyze_players():
    """
    Analyze selected players and return recommendations
    Expected input: {"players": [player names]}
    """
    data = request.get_json()
    selected_names = data.get('players', [])
    
    # Filter and score selected players
    selected_players = [
        p for p in SAMPLE_PLAYERS 
        if p['name'] in selected_names
    ]
    
    # Calculate scores
    for player in selected_players:
        player['score'] = calculate_player_score(player)
    
    # Sort by score (descending)
    selected_players.sort(key=lambda x: x['score'], reverse=True)
    
    # Determine start/sit recommendations
    # Simple rule: top 50% start, bottom 50% bench
    midpoint = len(selected_players) // 2
    
    for i, player in enumerate(selected_players):
        if i < midpoint or len(selected_players) <= 2:
            player['recommendation'] = 'Start'
        else:
            player['recommendation'] = 'Bench'
    
    return jsonify({
        'analyzed_players': selected_players,
        'total_selected': len(selected_players)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
