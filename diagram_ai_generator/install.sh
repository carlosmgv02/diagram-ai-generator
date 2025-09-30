#!/bin/bash

# Diagram AI Generator - Script de Instalación
# Este script instala y configura Diagram AI Generator

set -e

echo "🎨 Diagram AI Generator - Instalación"
echo "===================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.8 o superior."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION detectado"

# Verificar Graphviz
if ! command -v dot &> /dev/null; then
    echo "⚠️  Graphviz no está instalado. Intentando instalar..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y graphviz
        elif command -v yum &> /dev/null; then
            sudo yum install -y graphviz
        elif command -v pacman &> /dev/null; then
            sudo pacman -S graphviz
        else
            echo "❌ No se pudo instalar Graphviz automáticamente. Instálalo manualmente."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install graphviz
        else
            echo "❌ Homebrew no está instalado. Instala Graphviz manualmente."
            exit 1
        fi
    else
        echo "❌ OS no soportado para instalación automática de Graphviz."
        exit 1
    fi
fi

echo "✅ Graphviz instalado"

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate
echo "✅ Entorno virtual activado"

# Instalar dependencias
echo "📦 Instalando dependencias..."
if command -v bun &> /dev/null; then
    echo "🚀 Usando bun para instalar dependencias Python..."
    bun install
else
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Instalar el paquete en modo desarrollo
pip install -e .

echo "✅ Dependencias instaladas"

# Configurar archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "⚙️  Configurando archivo .env..."
    cp .env.example .env
    echo ""
    echo "📝 IMPORTANTE: Edita el archivo .env y añade tu API key de OpenAI:"
    echo "   OPENAI_API_KEY=tu_api_key_aqui"
    echo ""
fi

# Crear directorio de salida por defecto
mkdir -p diagrams_output

echo ""
echo "🎉 ¡Instalación completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Edita el archivo .env y añade tu API key de OpenAI"
echo "2. Activa el entorno virtual: source venv/bin/activate"
echo "3. Prueba la instalación: diagram-ai --help"
echo ""
echo "🚀 Ejemplo de uso:"
echo "   diagram-ai generate \"aplicación web con load balancer y base de datos\""
echo ""
echo "📚 Para más información, consulta README.md"