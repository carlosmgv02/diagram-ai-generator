#!/bin/bash
# Script para publicar imagen Docker en Docker Hub

set -e

echo "🐳 Publishing Diagram AI Generator to Docker Hub"
echo ""

# Variables
IMAGE_NAME="diagram-ai-generator"
DOCKER_USERNAME="carlosmgv"  # Cambia por tu usuario de Docker Hub
VERSION="1.0.0"

echo "📦 Building Docker image..."
cd "$(dirname "$0")/.."
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$VERSION -f docker/Dockerfile .
docker tag $DOCKER_USERNAME/$IMAGE_NAME:$VERSION $DOCKER_USERNAME/$IMAGE_NAME:latest

echo "🔐 Login to Docker Hub (enter your credentials)..."
docker login

echo "📤 Pushing to Docker Hub..."
docker push $DOCKER_USERNAME/$IMAGE_NAME:$VERSION
docker push $DOCKER_USERNAME/$IMAGE_NAME:latest

echo ""
echo "✅ ¡Imagen publicada exitosamente!"
echo ""
echo "🌍 Ahora cualquiera puede usar:"
echo "   docker run -d --name diagram-ai-server --rm -v ~/diagram_ai_output:/app/generated_diagrams $DOCKER_USERNAME/$IMAGE_NAME:latest tail -f /dev/null"
echo ""
echo "🔗 O con el one-liner:"
echo "   curl -sSL https://raw.githubusercontent.com/tu-usuario/diagram-ai-generator/main/scripts/one_command_install.sh | bash"
