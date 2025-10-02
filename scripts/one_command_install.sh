#!/bin/bash
# One-command install para Diagram AI Generator
# Uso: curl -sSL https://raw.githubusercontent.com/tu-usuario/diagram-ai-generator/main/scripts/one_command_install.sh | bash

set -e

echo "🚀 Diagram AI Generator - One Command Install"
echo "Installing without any dependencies..."
echo ""

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker requerido. Instala desde: https://www.docker.com/"
    echo "   macOS: brew install --cask docker"
    echo "   Ubuntu: sudo apt-get install docker.io"
    echo "   Windows: Download from docker.com"
    exit 1
fi

# Crear directorio
INSTALL_DIR="$HOME/.diagram-ai-generator"
DIAGRAMS_DIR="$HOME/diagram_ai_output"
mkdir -p "$INSTALL_DIR" "$DIAGRAMS_DIR"

# Descargar imagen desde Docker Hub (cuando esté publicada)
echo "📦 Descargando imagen..."
docker pull carlosmgv/diagram-ai-generator:latest || {
    echo "⚠️  Imagen no encontrada en Docker Hub, construyendo localmente..."
    
    # Clonar repo temporalmente
    TEMP_DIR=$(mktemp -d)
    git clone https://github.com/tu-usuario/diagram-ai-generator.git "$TEMP_DIR"
    cd "$TEMP_DIR"
    docker build -t carlosmgv/diagram-ai-generator:latest -f docker/Dockerfile .
    cd - && rm -rf "$TEMP_DIR"
}

# Crear script de ejecución
cat > "$INSTALL_DIR/run.sh" << 'EOF'
#!/bin/bash
DIAGRAMS_DIR="$HOME/diagram_ai_output"
mkdir -p "$DIAGRAMS_DIR"

echo "🚀 Starting Diagram AI Generator..."
docker run -d \
    --name diagram-ai-server \
    --rm \
    -v "$DIAGRAMS_DIR":/app/generated_diagrams \
    carlosmgv/diagram-ai-generator:latest \
    tail -f /dev/null

echo "✅ Server started! Configure Claude Desktop with:"
echo '{
    "mcpServers": {
        "diagram-ai-generator": {
            "command": "docker",
            "args": ["exec", "-i", "diagram-ai-server", "python3", "-m", "src.application.mcp.server_modular"]
        }
    }
}'
EOF

chmod +x "$INSTALL_DIR/run.sh"

# Crear alias
echo "alias diagram-ai='$INSTALL_DIR/run.sh'" >> ~/.bashrc
echo "alias diagram-ai='$INSTALL_DIR/run.sh'" >> ~/.zshrc 2>/dev/null || true

echo ""
echo "✅ ¡Instalación completada!"
echo ""
echo "🚀 Para usar:"
echo "   1. Ejecuta: diagram-ai"
echo "   2. Configura Claude Desktop con el JSON mostrado"
echo "   3. ¡Crear diagramas!"
echo ""
echo "📁 Diagramas en: $DIAGRAMS_DIR"
echo "🛑 Detener: docker stop diagram-ai-server"
