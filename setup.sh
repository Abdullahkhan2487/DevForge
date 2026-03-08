#!/bin/bash

# DevForge Setup Script
# This script sets up the entire DevForge system

set -e

echo "🚀 DevForge Setup Script"
echo "========================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

echo "✅ All prerequisites are installed"
echo ""

# Setup Backend
echo "🔧 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your OPENAI_API_KEY"
fi

cd ..
echo "✅ Backend setup complete"
echo ""

# Setup Frontend
echo "🎨 Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cp .env.local.example .env.local
fi

cd ..
echo "✅ Frontend setup complete"
echo ""

# Create generated_projects directory
if [ ! -d "generated_projects" ]; then
    mkdir -p generated_projects
    echo "✅ Created generated_projects directory"
fi

# Summary
echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo ""
echo "1. Add your OpenAI API key to backend/.env"
echo "   OPENAI_API_KEY=sk-your-key-here"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open your browser to http://localhost:3000"
echo ""
echo "For more information, see:"
echo "  - docs/GETTING_STARTED.md"
echo "  - docs/SETUP.md"
echo ""
echo "Happy building! 🚀"
