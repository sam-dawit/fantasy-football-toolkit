# 🏈 Fantasy Football Toolkit

MVP fantasy football analytics tool with player scoring and start/sit recommendations based on projected points, recent performance, and matchup difficulty.

## 📋 Features

- **Player Selection Interface**: Clean, responsive UI to select multiple players
- **Smart Scoring Algorithm**: Weighted scoring system considering:
  - Projected points (40%)
  - Last 3 games average (35%)
  - Opponent defense rank (25%)
- **Start/Sit Recommendations**: Automated recommendations ranked by composite score
- **Real-time Analysis**: Instant feedback on your lineup decisions

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sam-dawit/fantasy-football-toolkit.git
   cd fantasy-football-toolkit
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

   3. **Configure ESPN Authentication** (Required for private leagues)
```bash
cp config.py.example config.py
```

Then edit `config.py` and add your ESPN credentials:
- Log into ESPN Fantasy Football in your browser
- Open Developer Tools (F12 or right-click → Inspect)
- Go to Application tab (Chrome) or Storage tab (Firefox)
- Click on Cookies → fantasy.espn.com
- Find 'espn_s2' and 'SWID' cookies and copy their values to config.py

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   Navigate to: http://localhost:5000
   ```

## 📁 Project Structure

```
fantasy-football-toolkit/
├── app.py                 # Flask backend with scoring logic
├── templates/
│   └── index.html        # Frontend interface
└── README.md
```

## 🎯 How It Works

### Scoring Algorithm

Each player receives a composite score calculated as:

```python
score = (0.4 × projected_points) + 
        (0.35 × last_3_game_avg) + 
        (0.25 × matchup_factor)
```

Where:
- **Projected Points**: Fantasy points projection for this week
- **Last 3 Game Average**: Recent performance trend
- **Matchup Factor**: Opponent defense ranking (inverted, so easier matchups score higher)

### Recommendations

- Players are ranked by their composite score
- Top 50% = **Start**
- Bottom 50% = **Bench**
- Minimum 2 players selected to get recommendations

## 🔧 API Endpoints

### GET `/api/players`
Returns all available players with their stats.

**Response:**
```json
[
  {
    "name": "Patrick Mahomes",
    "position": "QB",
    "team": "KC",
    "projected_points": 24.5,
    "last_3_avg": 26.2,
    "opponent_def_rank": 28
  }
]
```

### POST `/api/analyze`
Analyzes selected players and returns ranked recommendations.

**Request Body:**
```json
{
  "players": ["Patrick Mahomes", "Josh Allen", "Christian McCaffrey"]
}
```

**Response:**
```json
{
  "analyzed_players": [
    {
      "name": "Patrick Mahomes",
      "position": "QB",
      "team": "KC",
      "score": 25.45,
      "recommendation": "Start"
    }
  ],
  "total_selected": 3
}
```

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with gradient design

## 📈 Future Enhancements (Beyond MVP)

- [ ] Integrate real fantasy API (ESPN, Yahoo, Sleeper)
- [ ] Add weather data for outdoor games
- [ ] Include injury reports
- [ ] Historical accuracy tracking
- [ ] User accounts and saved lineups
- [ ] Trade analyzer tool
- [ ] Weekly waiver wire recommendations

## 🤝 Contributing

This is an MVP project. Feel free to fork and expand with:
- Additional data sources
- More sophisticated ML models
- Mobile-responsive improvements
- Position-specific scoring adjustments

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Sam Dawit**
- GitHub: [@sam-dawit](https://github.com/sam-dawit)

---

**Built as part of a portfolio project to demonstrate:**
- Full-stack web development
- RESTful API design
- Data-driven decision making
- Sports analytics application
