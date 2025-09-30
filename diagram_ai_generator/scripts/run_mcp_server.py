#!/usr/bin/env python3
"""
Script para ejecutar el servidor MCP modular
"""
import sys
import os
from pathlib import Path

# Añadir el directorio del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Importar y ejecutar el servidor MCP modular
from src.application.mcp.server_modular import main

if __name__ == "__main__":
    print("🛠️  Iniciando servidor MCP modular de Diagram AI Generator...")
    main()
