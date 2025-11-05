#!/bin/bash
echo "Starting BB84 Full-Stack Application..."

# Start backend in background
echo "Starting backend..."
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend in background
echo "Starting frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Backend is running at: http://localhost:8000"
echo "Frontend is running at: http://localhost:5173"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for interrupt signal
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
