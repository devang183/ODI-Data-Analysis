# Quick Start Guide

## Get Started in 3 Steps

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 2. Start the Backend

```bash
cd backend
source venv/bin/activate  # Virtual environment is already set up
python app.py
```

Backend will run on http://localhost:5000

### 3. Start the Frontend (in a new terminal)

```bash
cd frontend
npm run dev
```

Frontend will run on http://localhost:3000

## That's it!

Open your browser and go to http://localhost:3000

## One-Line Startup (Optional)

You can also use the provided startup script:

```bash
chmod +x start.sh
./start.sh
```

This will start both backend and frontend together.

## What's Already Set Up

✅ PostgreSQL database with 2,491 ODI matches
✅ Backend API with all endpoints
✅ Frontend React application
✅ Python virtual environment with dependencies

## Quick Test

Once the application is running, try:

1. **Search**: Filter matches by team or venue
2. **Batting Stats**: Select a player like "V Sehwag" or "SR Tendulkar"
3. **Bowling Stats**: Try "M Muralitharan" or "Wasim Akram"
4. **Phase Performance**: Analyze any player's performance by phase
5. **MOTM**: Check Man of the Match leaderboard

## Troubleshooting

### Backend won't start?
- Make sure PostgreSQL is running
- Check if port 5000 is available
- Verify database credentials in `backend/.env`

### Frontend won't start?
- Run `npm install` in the frontend directory
- Check if port 3000 is available
- Try deleting `node_modules` and running `npm install` again

### Can't connect to database?
Your database credentials are already configured in `backend/.env`:
- Host: localhost
- Database: postgres
- User: devangkankaria

## Next Steps

Explore the full documentation in [README.md](README.md) for:
- Complete API documentation
- Feature details
- Development guide
- Advanced configuration

## Sample Queries to Try

1. **Search for India vs Pakistan matches**
   - Go to Search
   - Select "India" or "Pakistan" as team

2. **Find top run scorers**
   - Go to Batting Stats
   - Check the leaderboard

3. **Analyze Sachin Tendulkar's phase performance**
   - Go to Phase Performance
   - Select "SR Tendulkar"
   - View stats by match phase

4. **Check dismissal patterns**
   - Go to Dismissal Patterns
   - Select any batsman
   - See how they get out most often

Enjoy analyzing ODI cricket data!
