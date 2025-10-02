import json
from typing import Optional
from src.application.mcp.tools.base_tool import BaseTool, register_tool
from src.application.mcp.tools.tool_constants import (
    LANGUAGE_INSTRUCTION,
    SINGLE_CLOUD_EXAMPLE,
    MULTI_CLOUD_EXAMPLE,
    RECOMMENDED_WORKFLOW
)

class DiagramTool(BaseTool):
    @register_tool
    def create_diagram_from_json(
        self,
        diagram_spec: str,
        title: Optional[str] = None
    ) -> str:
        f"""
        Create an architecture diagram from a JSON specification.
        
        {LANGUAGE_INSTRUCTION}
        
        {RECOMMENDED_WORKFLOW}

        Args:
            diagram_spec: JSON specification of the diagram. Required format:
            
            SINGLE-CLOUD EXAMPLE:
            {json.dumps(SINGLE_CLOUD_EXAMPLE, indent=2)}
            
            MULTI-CLOUD EXAMPLE (use component_provider for each component):
            {json.dumps(MULTI_CLOUD_EXAMPLE, indent=2)}
            
            IMPORTANT:
            - Use "clusters" (NOT "children")
            - Use exact node names from get_category_nodes()
            - Connections support: color, style, label
            - Layouts: "horizontal" or "vertical"
            
            title: Optional diagram title (overrides spec title)
        
        Returns:
            Diagram generation result with file path and details
        """
        try:
            # Parsear la especificación JSON
            spec = json.loads(diagram_spec)
            
            # Agregar título si se proporciona
            if title:
                spec['title'] = title
            
            # Generar el diagrama
            result = self.diagram_service.create_diagram_from_spec(spec)
            
            if result['success']:
                response = f"""✅ Diagram created successfully!

📊 Details:
- Title: {result['title']}
- Provider: {result['provider']}
- Components: {result['components_count']}
- Connections: {result['connections_count']}
- Size: {result['image_size_mb']} MB

📁 File saved at: `{result['file_path']}`

To open: `open "{result['file_path']}"`

🖼️ Image saved locally (use the 'open' command above to view)"""
                
                return response
            else:
                return f"❌ Error: {result['error']}"
                
        except json.JSONDecodeError as e:
            return f"❌ Error: Invalid JSON - {str(e)}"
        except Exception as e:
            return f"❌ Error generating diagram: {str(e)}"