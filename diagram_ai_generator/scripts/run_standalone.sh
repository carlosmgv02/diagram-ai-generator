#!/bin/bash
# Script para ejecutar Diagram AI Generator como servidor standalone sin instalación

set -e

echo "🚀 Diagram AI Generator - Standalone Server"
echo "Sin instalación requerida - Solo Docker!"
echo ""

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Instálalo desde: https://www.docker.com/"
    exit 1
fi

# Crear directorio para diagramas si no existe
DIAGRAMS_DIR="$HOME/Documents/diagram_ai_output"
mkdir -p "$DIAGRAMS_DIR"

echo "📁 Diagramas se guardarán en: $DIAGRAMS_DIR"
echo ""

# Construir imagen si no existe
IMAGE_NAME="diagram-ai-generator:latest"
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
    echo "📦 Construyendo imagen Docker..."
    docker build -t $IMAGE_NAME -f docker/Dockerfile .
    echo "✅ Imagen construida exitosamente"
    echo ""
fi

echo "🚀 Iniciando servidor MCP..."
echo "💡 Para conectar desde Claude Desktop, usa:"
echo '   "command": "docker", "args": ["exec", "-i", "diagram-ai-server", "python3", "-m", "src.application.mcp.server_modular"]'
echo ""

# Ejecutar contenedor como servidor persistente
docker run -d \
    --name diagram-ai-server \
    --rm \
    -v "$DIAGRAMS_DIR":/app/generated_diagrams \
    -p 8080:8080 \
    $IMAGE_NAME \
    tail -f /dev/null

echo "✅ Servidor iniciado como contenedor: diagram-ai-server"
echo ""
echo "📋 Comandos útiles:"
echo "   - Ver logs: docker logs -f diagram-ai-server"
echo "   - Conectar MCP: docker exec -i diagram-ai-server python3 -m src.application.mcp.server_modular"
echo "   - Detener: docker stop diagram-ai-server"
echo ""
echo "🔗 Configuración para Claude Desktop:"
echo '{
    "mcpServers": {
        "diagram-ai-generator": {
            "command": "docker",
            "args": ["exec", "-i", "diagram-ai-server", "python3", "-m", "src.application.mcp.server_modular"]
        }
    }
}'
echo ""
echo "⏳ Servidor corriendo en background. Usa 'docker stop diagram-ai-server' para detener."
