#!/bin/bash

# Setup script for macOS/Linux

echo "========================================"
echo "Kids Coloring Page Generator - Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Upgrading pip..."
python -m pip install --upgrade pip

echo "[4/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[5/5] Setting up environment file..."
if [ ! -f .env ]; then
    cp env.example .env
    echo "Created .env file. Please edit it and add your API keys!"
else
    echo ".env file already exists. Skipping..."
fi

# Create necessary directories
mkdir -p static/uploads
mkdir -p static/outputs

echo ""
echo "========================================"
echo "Setup Complete! ✓"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "   - Get Stability AI key: https://platform.stability.ai/"
echo "   - Get OpenAI key (optional): https://platform.openai.com/"
echo "2. Run the application:"
echo "   - source venv/bin/activate"
echo "   - python run.py"
echo ""

