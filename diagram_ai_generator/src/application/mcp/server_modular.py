"""
Servidor MCP modular para Diagram AI Generator
"""
import sys
import asyncio
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    print("❌ MCP no está disponible. Instala con: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Añadir el directorio del proyecto al path para importaciones relativas
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.application.services.diagram_service import DiagramService
from src.application.mcp.tools.registry import ToolRegistry

# Crear instancia del servicio de diagramas
diagram_service = DiagramService()

# Crear instancia del registro de herramientas
tool_registry = ToolRegistry(diagram_service)

# Crear instancia del servidor MCP
mcp = FastMCP("diagram-ai-generator")

# Registrar todas las herramientas dinámicamente
for tool_name, tool_method in tool_registry.get_tool_methods().items():
    mcp.tool()(tool_method)

# Función principal para ejecutar el servidor
def main():
    """Función principal para ejecutar el servidor MCP"""
    try:
        # Ejecutar el servidor MCP - esto bloquea hasta que se cierre
        mcp.run()
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(f"Error en el servidor: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    main()