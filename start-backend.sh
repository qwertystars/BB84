#!/bin/bash
echo "Starting BB84 Backend Server..."
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
