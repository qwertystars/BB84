#!/bin/bash
set -e

echo "Building BB84 Application for Render deployment..."

# Get the script's directory and navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Install frontend dependencies and build
echo "Installing frontend dependencies..."
cd frontend
npm install

echo "Building frontend..."
npm run build

cd ..

echo "Build completed successfully!"
echo "Frontend assets are in: frontend/dist"
