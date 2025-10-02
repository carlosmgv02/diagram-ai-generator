from typing import Dict, Any
from src.application.mcp.tools.base_tool import BaseTool, register_tool
from src.application.mcp.tools.tool_constants import LANGUAGE_INSTRUCTION, MULTI_CLOUD_EXAMPLE
import json

class MultiCloudTool(BaseTool):
    @register_tool
    def create_multicloud_diagram(
        self,
        title: str,
        components: str,
        connections: str = "[]",
        layout: str = "horizontal"
    ) -> str:
        f"""
        Create a multi-cloud architecture diagram with components from different providers.
        
        {LANGUAGE_INSTRUCTION}
        
        This is a convenience tool for multi-cloud scenarios. Each component can specify
        its own provider using "component_provider".
        
        Args:
            title: Diagram title
            components: JSON array of components with component_provider field
            connections: JSON array of connections (optional)
            layout: "horizontal" or "vertical" (default: horizontal)
        
        Example components:
        {json.dumps(MULTI_CLOUD_EXAMPLE['components'], indent=2)}
        
        Returns:
            Diagram generation result
        """
        try:
            components_list = json.loads(components)
            connections_list = json.loads(connections)
            
            spec = {
                "title": title,
                "provider": "generic",  # Multi-cloud uses generic base
                "layout": layout,
                "components": components_list,
                "connections": connections_list,
                "clusters": []
            }
            
            result = self.diagram_service.create_diagram_from_spec(spec)
            
            if result['success']:
                return f"""✅ Multi-cloud diagram created!

📊 Details:
- Title: {result['title']}
- Components: {result['components_count']} (from multiple providers)
- Connections: {result['connections_count']}
- Size: {result['image_size_mb']} MB

📁 File: `{result['file_path']}`

To open: `open "{result['file_path']}"`"""
            else:
                return f"❌ Error: {result['error']}"
                
        except json.JSONDecodeError as e:
            return f"❌ Error: Invalid JSON - {str(e)}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
