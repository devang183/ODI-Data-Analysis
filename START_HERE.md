# 🚀 START HERE - ODI Cricket Analytics

## ✅ Port Issue Fixed!

The application now runs on **port 5001** (instead of 5000) to avoid conflicts with macOS AirPlay.

## Quick Start (2 Easy Steps)

### Step 1: Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate
python app.py
```

✅ Backend will run on **http://localhost:5001**

### Step 2: Start Frontend (Terminal 2)

```bash
cd frontend
npm install  # Only needed first time
npm run dev
```

✅ Frontend will run on **http://localhost:3000**

## 🌐 Open the App

Navigate to: **http://localhost:3000**

## 🎯 What You Can Do

### 1. Search Matches
- Filter by team (e.g., India, Australia)
- Filter by venue
- Date range filtering
- View complete match details

### 2. Batting Statistics
**Try these players:**
- SR Tendulkar (Sachin Tendulkar)
- V Sehwag (Virender Sehwag)
- RT Ponting (Ricky Ponting)
- KC Sangakkara
- BC Lara (Brian Lara)

**What you'll see:**
- Total runs, matches, average
- Strike rate, 4s, 6s
- Innings-by-innings breakdown
- Top batsmen leaderboard

### 3. Bowling Statistics
**Try these bowlers:**
- M Muralitharan
- Wasim Akram
- GD McGrath (Glenn McGrath)
- Waqar Younis
- SM Pollock (Shaun Pollock)

**What you'll see:**
- Wickets, economy, average
- Bowling strike rate
- Match-by-match figures
- Top bowlers leaderboard

### 4. Phase Performance
**Analyze performance by overs:**
- Powerplay: 0-10 overs
- Middle: 11-40 overs
- Death: 41-50 overs

Works for both batting and bowling!

### 5. Dismissal Patterns
See how batsmen get out:
- Caught, Bowled, LBW, Run Out
- Pie chart visualization
- Which bowlers dismiss them most

### 6. Batter vs Bowler
**Try famous matchups:**
- Sachin Tendulkar vs Shoaib Akhtar
- Virender Sehwag vs Brett Lee
- Ricky Ponting vs Harbhajan Singh

**See:**
- Head-to-head stats
- Every encounter
- Who won the battle

### 7. Man of the Match (MOTM)
- Top award winners
- Player award history
- When and where they won

### 8. Admin Dashboard
- Database overview
- 2,491 total matches
- All teams and players
- Data validation

## 📊 Sample Queries

1. **Find all India vs Pakistan matches:**
   - Go to Search → Select "India" or "Pakistan"

2. **Who has the most MOTM awards?**
   - Go to MOTM → Check leaderboard

3. **How does Sachin perform in death overs?**
   - Go to Phase Performance → Select "SR Tendulkar"

4. **Batting average of top 20 players:**
   - Go to Batting Stats → Sort by "Best Average"

## 🛑 Stopping the Servers

Press `Ctrl+C` in each terminal to stop the servers.

## ❓ Troubleshooting

### Backend Issues

**"Port already in use"**
- Port 5001 is now being used (fixed!)
- If still issues, check: `lsof -ti:5001 | xargs kill -9`

**"Can't connect to database"**
- Make sure PostgreSQL is running
- Database: `postgres`, Table: `odiwc2023`

**"Module not found"**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Issues

**"Dependencies missing"**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**"Port 3000 in use"**
- Close other apps using port 3000
- Or change port in `vite.config.js`

## 📱 Features

✅ Search & filter 2,491 ODI matches
✅ Interactive charts and graphs
✅ Player career statistics
✅ Phase-wise performance analysis
✅ Dismissal pattern analysis
✅ Head-to-head comparisons
✅ MOTM awards tracking
✅ Share functionality
✅ Mobile responsive

## 📚 More Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Detailed quick start guide
- **[README.md](README.md)** - Complete documentation
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical overview

## 🎉 You're All Set!

The application is ready to use. Enjoy exploring ODI cricket statistics!

---

**Current Status:**
- ✅ Backend running on port 5001
- ✅ Database connected (2,491 matches)
- ✅ All APIs tested and working
- ✅ Ready for frontend launch!
