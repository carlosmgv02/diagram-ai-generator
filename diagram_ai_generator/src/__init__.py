"""
Diagram AI Generator - Professional architecture diagram generator with MCP support

A powerful tool for generating beautiful, accurate diagrams with provider-specific icons 
for AWS, Azure, GCP, Kubernetes, and more.
"""

__version__ = "1.0.0"
__author__ = "Diagram AI Generator Team"
__email__ = "contact@diagram-ai.com"
__description__ = "Professional AI-powered architecture diagram generator with MCP server support"

# Expose main components
from .application.services.diagram_service import DiagramService
from .application.mcp.server_modular import main as run_mcp_server

__all__ = [
    "DiagramService",
    "run_mcp_server",
    "__version__",
]
