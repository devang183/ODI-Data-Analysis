# ODI Cricket Analytics Application

A comprehensive web application for analyzing historical ODI cricket data with interactive visualizations and detailed statistics.

## Features

- **Search**: Find and explore ODI matches with advanced filtering
- **Phase Performance**: Analyze batting and bowling performance across match phases (Powerplay, Middle, Death)
- **Dismissal Patterns**: Understand how players get dismissed most often
- **Batting Stats**: Comprehensive batting statistics and leaderboards
- **Bowling Stats**: Detailed bowling performance metrics
- **Vs Bowler**: Head-to-head matchup statistics between batters and bowlers
- **MOTM**: Man of the Match award statistics and leaderboards
- **Admin**: Database management and data validation tools

## Technology Stack

### Backend
- Python 3.8+
- Flask (Web Framework)
- PostgreSQL (Database)
- psycopg2 (PostgreSQL adapter)

### Frontend
- React 18
- Vite (Build tool)
- React Router (Navigation)
- Recharts (Data visualization)
- Axios (HTTP client)

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- PostgreSQL 12 or higher
- npm or yarn

## Database Setup

Your PostgreSQL database should already be set up with:
- Database name: `postgres`
- Table: `odiwc2023` with columns:
  - `id` (VARCHAR) - Primary key
  - `metadata` (JSONB) - Match data in JSON format

## Installation

### 1. Clone/Navigate to the Project

```bash
cd /Users/devangkankaria/Downloads/odi_data_upload
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (if not already created)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Edit backend/.env file with your database credentials
# (Already created with your credentials)
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install
```

## Running the Application

### Start the Backend Server

```bash
# From the backend directory
cd backend
source venv/bin/activate  # Activate virtual environment
python app.py
```

The backend API will run on `http://localhost:5000`

### Start the Frontend Development Server

```bash
# From the frontend directory (in a new terminal)
cd frontend
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Use the sidebar navigation to access different features:
   - **Search**: Filter and search for matches
   - **Phase Performance**: Analyze player performance by match phase
   - **Dismissal Patterns**: View how players get dismissed
   - **Batting Stats**: Explore batting statistics and leaderboards
   - **Bowling Stats**: View bowling performance metrics
   - **Vs Bowler**: Compare head-to-head matchups
   - **MOTM**: See Man of the Match award winners
   - **Admin**: Access database overview and validation tools

## API Endpoints

### Search
- `GET /api/search/matches` - Search matches with filters
- `GET /api/search/players` - Get all players
- `GET /api/search/teams` - Get all teams
- `GET /api/search/venues` - Get all venues
- `GET /api/search/seasons` - Get all seasons
- `GET /api/search/match/:id` - Get match details

### Batting Stats
- `GET /api/batting-stats/player/:name` - Get player batting stats
- `GET /api/batting-stats/player/:name/innings` - Get player innings list
- `GET /api/batting-stats/leaderboard` - Get batting leaderboard

### Bowling Stats
- `GET /api/bowling-stats/player/:name` - Get player bowling stats
- `GET /api/bowling-stats/player/:name/spells` - Get bowling spells
- `GET /api/bowling-stats/leaderboard` - Get bowling leaderboard

### Phase Performance
- `GET /api/phase-performance/player/:name` - Get batting phase performance
- `GET /api/phase-performance/player/:name/bowling` - Get bowling phase performance

### Dismissal Patterns
- `GET /api/dismissal-patterns/player/:name` - Get dismissal patterns
- `GET /api/dismissal-patterns/player/:name/by-phase` - Get dismissals by phase

### Vs Bowler
- `GET /api/vs-bowler/batter/:batter/bowler/:bowler` - Get head-to-head stats

### MOTM
- `GET /api/motm/player/:name` - Get player MOTM awards
- `GET /api/motm/leaderboard` - Get MOTM leaderboard

### Admin
- `GET /api/admin/stats/overview` - Get database overview
- `GET /api/admin/data/validate` - Validate data integrity

## Project Structure

```
odi_data_upload/
├── backend/
│   ├── api/
│   │   ├── search.py
│   │   ├── batting_stats.py
│   │   ├── bowling_stats.py
│   │   ├── phase_performance.py
│   │   ├── dismissal_patterns.py
│   │   ├── vs_bowler.py
│   │   ├── motm.py
│   │   └── admin.py
│   ├── models/
│   │   └── database.py
│   ├── utils/
│   │   └── helpers.py
│   ├── app.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout.jsx
│   │   ├── pages/
│   │   │   ├── Search.jsx
│   │   │   ├── BattingStats.jsx
│   │   │   ├── BowlingStats.jsx
│   │   │   ├── PhasePerformance.jsx
│   │   │   ├── DismissalPatterns.jsx
│   │   │   ├── VsBowler.jsx
│   │   │   ├── MOTM.jsx
│   │   │   └── Admin.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   ├── index.css
│   │   │   ├── App.css
│   │   │   └── Layout.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── odis_male_json/        # JSON data files
├── upload_jsons_improved.py
└── README.md
```

## Database Schema

The application uses a PostgreSQL database with JSONB storage for flexible querying:

```sql
CREATE TABLE odiwc2023 (
    id VARCHAR PRIMARY KEY,
    metadata JSONB NOT NULL
);
```

The metadata JSONB field contains the complete match data including:
- Match information (date, venue, teams, outcome)
- Player registry
- Ball-by-ball data
- Innings details
- Officials and event information

## Features in Detail

### Search
- Filter matches by team, venue, season, date range
- View detailed match information
- Paginated results

### Phase Performance
- Analyze performance in Powerplay (0-10 overs)
- Middle overs (11-40 overs)
- Death overs (41-50 overs)
- Visual charts for easy comparison

### Dismissal Patterns
- Pie charts showing dismissal distribution
- Bowler-specific dismissal patterns
- Phase-wise dismissal analysis

### Batting Stats
- Career statistics for any player
- Innings-by-innings breakdown
- Leaderboards with multiple sorting options
- Team-specific performance

### Bowling Stats
- Comprehensive bowling metrics
- Match-by-match bowling figures
- Economy rate and strike rate analysis
- Wicket distribution

### Vs Bowler
- Head-to-head matchup statistics
- Match-by-match encounter details
- Strike rate and average comparisons

### MOTM
- Man of the Match award history
- Player-wise award counts
- Match details for each award

### Admin
- Database statistics overview
- Data validation tools
- Team and player counts

## Development

### Adding New Features

1. **Backend**: Add new API endpoints in `backend/api/`
2. **Frontend**: Create new page components in `frontend/src/pages/`
3. **API Service**: Add API functions in `frontend/src/services/api.js`
4. **Routing**: Update routes in `frontend/src/App.jsx`

### Building for Production

```bash
# Build frontend
cd frontend
npm run build

# The build files will be in frontend/dist/
# Serve with any static file server
```

## Troubleshooting

### Backend Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check database credentials in `backend/.env`
   - Ensure database and table exist

2. **Module Not Found**
   - Activate virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

1. **Cannot Connect to API**
   - Verify backend is running on port 5000
   - Check proxy configuration in `vite.config.js`

2. **Dependencies Error**
   - Delete `node_modules` and `package-lock.json`
   - Run `npm install` again

## Data Format

The application expects JSON data in the Cricsheet format:
```json
{
  "meta": { ... },
  "info": {
    "teams": ["Team A", "Team B"],
    "dates": ["2023-01-01"],
    "venue": "Stadium Name",
    ...
  },
  "innings": [
    {
      "team": "Team A",
      "overs": [
        {
          "over": 0,
          "deliveries": [
            {
              "batter": "Player Name",
              "bowler": "Player Name",
              "runs": { ... },
              ...
            }
          ]
        }
      ]
    }
  ]
}
```

## Contributing

Feel free to extend this application with additional features:
- Player comparison tools
- Team statistics
- Tournament analysis
- Predictive analytics
- Advanced visualizations

## License

This project is for educational and analytical purposes.

## Contact

For questions or issues, please create an issue in the repository.
