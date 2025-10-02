from typing import Dict, List, Type
from src.application.mcp.tools.base_tool import BaseTool
from src.application.mcp.tools.providers_tool import ProvidersTool
from src.application.mcp.tools.categories_tool import CategoriesTool
from src.application.mcp.tools.nodes_tool import NodesTool
from src.application.mcp.tools.diagram_tool import DiagramTool
from src.application.mcp.tools.multicloud_tool import MultiCloudTool
from src.application.services.diagram_service import DiagramService


class ToolRegistry:
    def __init__(self, diagram_service: DiagramService):
        self.diagram_service = diagram_service
        self._tools: Dict[str, BaseTool] = {}
        self._register_all_tools()

    def _register_all_tools(self):
        """Registers all tool classes."""
        tool_classes: List[Type[BaseTool]] = [
            ProvidersTool,
            CategoriesTool,
            NodesTool,
            DiagramTool,
            MultiCloudTool,
        ]
        for tool_class in tool_classes:
            instance = tool_class(self.diagram_service)
            self._tools[tool_class.__name__] = instance

    def get_tool_methods(self) -> Dict[str, callable]:
        """Returns a dictionary of all registered tool methods."""
        methods = {}
        for tool_instance in self._tools.values():
            for name in dir(tool_instance):
                # Include all methods that don't start with underscore and are registered
                if not name.startswith("_") and hasattr(getattr(tool_instance, name), '_is_mcp_tool'):
                    method = getattr(tool_instance, name)
                    if callable(method):
                        methods[name] = method
        return methods