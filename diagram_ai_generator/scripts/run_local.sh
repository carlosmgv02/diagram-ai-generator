#!/bin/bash
# Script para ejecutar el servidor MCP localmente (sin Docker)

set -e

echo "🏠 Ejecutando Diagram AI Generator localmente..."

# Verificar que estamos en el directorio correcto
if [ ! -f "src/application/mcp/server_modular.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

# Verificar dependencias
echo "🔍 Verificando dependencias..."
python3 -c "import diagrams, PIL; print('✅ Dependencias básicas OK')" || {
    echo "❌ Faltan dependencias. Instala con: pip install -r requirements.txt"
    exit 1
}

# Verificar MCP
python3 -c "import mcp; print('✅ MCP disponible')" || {
    echo "⚠️  MCP no está disponible. El servidor se ejecutará en modo debug."
}

# Crear directorio de salida
mkdir -p generated_diagrams

# Mostrar información
echo ""
echo "📋 Información del servidor:"
echo "   - Puerto: No aplica (MCP usa stdin/stdout)"
echo "   - Diagramas: ./generated_diagrams/"
echo "   - Logs: Consola actual"
echo ""

# Ejecutar el servidor
echo "🚀 Iniciando servidor MCP..."
echo "💡 Para conectar desde Claude Desktop:"
echo "   Comando: python3 $(pwd)/scripts/run_mcp_server.py"
echo ""
echo "⏳ Presiona Ctrl+C para detener"
echo "----------------------------------------"

python3 scripts/run_mcp_server.py
