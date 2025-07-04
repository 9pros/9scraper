#!/bin/bash

# 9Scraper Development Setup Script
# This script sets up the development environment

set -e

echo "🛠️  Setting up 9Scraper Development Environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before continuing."
    echo "Press Enter when ready..."
    read
fi

# Start development services
echo "🔨 Starting development services..."
docker-compose -f docker-compose.dev.yml up -d --build

# Wait for services
echo "⏳ Waiting for services..."
sleep 20

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install Node dependencies
echo "📦 Installing Node dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "🎉 Development environment setup completed!"
echo ""
echo "🚀 To start development:"
echo "   Backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "   Frontend: cd frontend && npm run dev"
echo "   Worker: cd backend && celery -A app.core.celery_app worker --loglevel=info"
echo ""
