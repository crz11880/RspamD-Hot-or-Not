#!/bin/bash
# RspamdHotOrNot - Run Script

set -e

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run install.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Using defaults."
    echo "Please copy .env.example to .env and configure it."
fi

# Parse arguments
HOST=${APP_HOST:-0.0.0.0}
PORT=${APP_PORT:-8000}
RELOAD=""

if [ "$1" == "--reload" ] || [ "$1" == "-r" ]; then
    RELOAD="--reload"
fi

echo "Starting RspamdHotOrNot..."
echo "Access the application at: http://localhost:$PORT"
echo "Press Ctrl+C to stop"
echo ""

python -m uvicorn app.main:app --host $HOST --port $PORT $RELOAD
