#!/bin/bash
# Script simple para ejecutar Diagram AI Generator con Docker (sin instalación)

echo "🚀 Diagram AI Generator - Docker Mode"
echo "No installation required!"
echo ""

# Crear directorio para diagramas si no existe
mkdir -p ~/diagram_ai_output

# Ejecutar con Docker directamente desde Docker Hub (cuando lo publiques)
echo "📦 Pulling and running from Docker Hub..."
docker run -it --rm \
  -v ~/diagram_ai_output:/app/generated_diagrams \
  -p 8080:8080 \
  carlosmgv/diagram-ai-generator:latest

echo ""
echo "✅ Diagrams saved to: ~/diagram_ai_output/"
echo "🔗 MCP Server running on port 8080"
