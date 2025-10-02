from src.application.mcp.tools.base_tool import BaseTool, register_tool
from src.application.mcp.tools.tool_constants import LANGUAGE_INSTRUCTION

class NodesTool(BaseTool):
    @register_tool
    def get_category_nodes(self, provider: str, category: str) -> str:
        f"""
        Get ALL nodes/icons available for a specific provider category.
        
        {LANGUAGE_INSTRUCTION}
        
        This is STEP 3 of the recommended workflow. Use get_provider_categories() first.
        
        Args:
            provider: Provider name (aws, azure, gcp, k8s, etc.)
            category: Exact category name (compute, network, database, etc.)
        
        Returns:
            Complete list of nodes to use in create_diagram_from_json with exact names
        """
        try:
            provider = provider.lower()
            nodes = self.diagram_service.get_category_nodes(provider, category)
            
            if not nodes:
                return f"❌ No nodes found for {provider}/{category}\n\n➡️ USE: get_provider_categories(\"{provider}\") to see valid categories"
            
            response = f"🎨 NODES FOR {provider.upper()}/{category.upper()}\n\n"
            for i, node in enumerate(nodes, 1):
                response += f"{i}. **{node}**\n"
            
            response += f"\n✅ Total: {len(nodes)} nodes available"
            response += f"\n\n⚠️  USE THESE EXACT NAMES in create_diagram_from_json"
            response += f"\n💡 JSON format: {{\"type\": \"{nodes[0] if nodes else 'NodeName'}\", \"category\": \"{category}\"}}"
            
            response += f"\n\n✅ WORKFLOW COMPLETE! Now use create_diagram_from_json()"
            
            return response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
