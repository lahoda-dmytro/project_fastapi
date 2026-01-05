#!/bin/bash

# Start FastAPI backend
echo "Starting FastAPI backend..."
source venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Start React frontend
echo "Starting React frontend..."
cd frontend
if command -v npm >/dev/null 2>&1; then
  npm run dev &
  FRONTEND_PID=$!
else
  echo "error: npm not found. please start the frontend manually in the /frontend directory using 'npm run dev'"
fi

# Handle exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM EXIT

wait
