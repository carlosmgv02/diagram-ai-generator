from typing import Callable, Dict, Any

tool_registry: Dict[str, Callable[..., Any]] = {}

def register_tool(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to register MCP tools automatically."""
    tool_registry[func.__name__] = func
    return func

class BaseTool:
    """Base class for all MCP tools."""
    def __init__(self, diagram_service: Any):
        self.diagram_service = diagram_service