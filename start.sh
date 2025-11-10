#!/bin/bash

# ODI Cricket Analytics - Startup Script

echo "=========================================="
echo "ODI Cricket Analytics Application"
echo "=========================================="
echo ""

# Check if backend virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Backend
echo "Starting Backend Server..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Check if backend is running
if ps -p $BACKEND_PID > /dev/null; then
    echo "✓ Backend running on http://localhost:5000"
else
    echo "✗ Backend failed to start"
    exit 1
fi

# Start Frontend
echo "Starting Frontend Server..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 3

# Check if frontend is running
if ps -p $FRONTEND_PID > /dev/null; then
    echo "✓ Frontend running on http://localhost:3000"
else
    echo "✗ Frontend failed to start"
    kill $BACKEND_PID
    exit 1
fi

echo ""
echo "=========================================="
echo "Application is running!"
echo "Backend:  http://localhost:5001"
echo "Frontend: http://localhost:3000"
echo "=========================================="
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for processes
wait
