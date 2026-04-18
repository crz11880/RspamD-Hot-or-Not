#!/bin/bash
# RspamdHotOrNot - Installation Script

set -e

echo "═══════════════════════════════════════════════════════════════"
echo "  RspamdHotOrNot - Installation"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "• Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi

# Activate virtual environment
echo "• Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "• Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install dependencies
echo "• Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "• Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created (please review and update)"
else
    echo "✓ .env file exists"
fi

# Create directories
echo "• Creating data directories..."
mkdir -p data/db
mkdir -p data/emails
echo "✓ Data directories created"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Installation complete!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Review and update .env file:"
echo "     nano .env"
echo ""
echo "  3. Start the application:"
echo "     python -m uvicorn app.main:app --reload"
echo ""
echo "  4. Access the web interface:"
echo "     http://localhost:8000"
echo ""
echo "  5. Login with default credentials:"
echo "     Username: admin"
echo "     Password: password123"
echo ""
echo "Security reminder: Change the default password and SECRET_KEY!"
echo ""
