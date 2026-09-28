#!/bin/bash

# Smart Customer Support Chatbot - macOS/Linux Setup Script
# Run this script from the project root directory

set -e  # Exit on error

echo ""
echo "========================================"
echo "Smart Customer Support Chatbot Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

echo "[1/7] Checking Python version..."
python3 --version
echo ""

# Step 1: Create virtual environment
echo "[2/7] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
else
    python3 -m venv venv
    echo "Virtual environment created."
fi
echo ""

# Step 2: Activate virtual environment
echo "[3/7] Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated."
echo ""

# Step 3: Upgrade pip
echo "[4/7] Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel
echo ""

# Step 4: Install requirements
echo "[5/7] Installing dependencies from requirements.txt..."
echo "This may take 5-10 minutes..."
if pip install -r requirements.txt; then
    echo "All dependencies installed successfully."
else
    echo "WARNING: Some dependencies failed to install."
    echo "Attempting to install core dependencies individually..."
    pip install fastapi uvicorn python-dotenv pydantic pydantic-settings sqlalchemy
fi
echo ""

# Step 5: Download spaCy model
echo "[6/7] Downloading spaCy model (en_core_web_sm)..."
echo "This may take 2-3 minutes..."
if python -m spacy download en_core_web_sm; then
    echo "spaCy model downloaded successfully."
else
    echo "WARNING: spaCy model download failed."
    echo "The app will work in fallback mode without advanced NLP."
fi
echo ""

# Step 6: Create .env file
echo "[7/7] Setting up environment configuration..."
if [ -f ".env" ]; then
    echo ".env file already exists."
else
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo ".env file created from .env.example"
    else
        echo "WARNING: .env.example not found. Please create .env manually."
    fi
fi
echo ""

echo "========================================"
echo "✓ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Start the backend server:"
echo "   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. In a new terminal, start the HTTP server:"
echo "   python -m http.server 8080"
echo ""
echo "3. Open your browser and visit:"
echo "   http://localhost:8080/frontend/index.html"
echo ""
echo "4. To test the API, use curl:"
echo "   curl http://localhost:8000/health"
echo ""
echo "For detailed instructions, see SETUP_AND_RUN.md"
echo ""
