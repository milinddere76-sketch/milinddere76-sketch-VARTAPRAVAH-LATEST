#!/bin/bash

# VartaPravah Broadcast System Startup Script

set -e

echo "================================"
echo "VartaPravah TV Broadcast System"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please copy .env.example to .env and fill in your YouTube Stream Key"
    echo "cp .env.example .env"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  docker-compose not found, trying 'docker compose'..."
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

echo "✅ Docker is installed"
echo ""

# Build images
echo "🏗️  Building Docker images..."
$COMPOSE_CMD build

echo ""
echo "🚀 Starting VartaPravah services..."
$COMPOSE_CMD up -d

echo ""
echo "✅ Services started!"
echo ""
echo "📊 Monitor logs with:"
echo "   $COMPOSE_CMD logs -f app"
echo ""
echo "📡 API available at: http://localhost:8000"
echo "📖 API documentation: http://localhost:8000/docs"
echo ""
echo "🛑 To stop services:"
echo "   $COMPOSE_CMD down"
echo ""