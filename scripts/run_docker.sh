#!/bin/bash
# Docker run script for Diagram AI Generator

set -e

echo "🐳 Starting Diagram AI Generator with Docker..."

# Create necessary directories
mkdir -p generated_diagrams

# Build and run with Docker Compose
cd docker

echo "📦 Building Docker image..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "✅ Diagram AI Generator is starting!"
echo ""
echo "📊 Generated diagrams will be saved to: ./generated_diagrams/"
echo "📋 Container logs: docker-compose logs -f diagram-ai-generator"
echo "🔍 Check status: docker-compose ps"
echo "🛑 Stop services: docker-compose down"
echo ""
echo "⏳ Waiting a moment for the server to stabilize..."
sleep 3
echo "📋 Current container status:"
docker-compose ps
