from src.application.mcp.tools.base_tool import BaseTool, register_tool
from src.application.mcp.tools.tool_constants import LANGUAGE_INSTRUCTION

class CategoriesTool(BaseTool):
    @register_tool
    def get_provider_categories(self, provider: str) -> str:
        f"""
        Get all categories available for a specific cloud provider.
        
        {LANGUAGE_INSTRUCTION}
        
        This is STEP 2 of the recommended workflow. Use list_providers() first.
        
        Args:
            provider: Exact provider name (aws, azure, gcp, k8s, onprem, etc.)
        
        Returns:
            List of categories for the selected provider
        """
        try:
            provider = provider.lower()
            categories = self.diagram_service.get_provider_categories(provider)
            
            if not categories:
                return f"❌ Provider '{provider}' not found.\n\n➡️ USE: list_providers() to see valid options"
            
            response = f"📂 CATEGORIES FOR {provider.upper()}\n\n"
            for i, category in enumerate(categories, 1):
                nodes_count = len(self.diagram_service.get_category_nodes(provider, category))
                response += f"{i}. **{category}** ({nodes_count} nodes)\n"
            
            response += f"\n✅ Total: {len(categories)} categories"
            response += f"\n\n➡️  NEXT STEP: get_category_nodes(\"{provider}\", \"category\")"
            response += f"\n💡 Example: get_category_nodes(\"{provider}\", \"compute\") for compute nodes"
            
            return response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
