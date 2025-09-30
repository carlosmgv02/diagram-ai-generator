#!/bin/bash
# Installation script for Diagram AI Generator

set -e

echo "🚀 Installing Diagram AI Generator..."

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.9"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "✅ Python $python_version detected (>= 3.9 required)"
else
    echo "❌ Python 3.9+ is required. Current version: $python_version"
    exit 1
fi

# Install system dependencies (Ubuntu/Debian)
if command -v apt-get &> /dev/null; then
    echo "📦 Installing system dependencies (Ubuntu/Debian)..."
    sudo apt-get update
    sudo apt-get install -y graphviz graphviz-dev python3-pip python3-venv
fi

# Install system dependencies (macOS)
if command -v brew &> /dev/null; then
    echo "📦 Installing system dependencies (macOS)..."
    brew install graphviz
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install package with MCP support
echo "📦 Installing Diagram AI Generator with MCP support..."
pip install -e ".[mcp]"

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "🛠️  To start the MCP server:"
echo "   source venv/bin/activate"
echo "   python3 scripts/run_mcp_server.py"
echo ""
echo "🐳 To run with Docker:"
echo "   cd docker && docker-compose up -d"
echo ""
echo "📚 Check README.md for detailed usage instructions"
