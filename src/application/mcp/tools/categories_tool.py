from typing import List
from src.application.mcp.tools.base_tool import BaseTool, register_tool

class CategoriesTool(BaseTool):
    @register_tool
    def step2_get_categories(self, provider: str) -> str:
        """
        🔥 PASO 2 OBLIGATORIO: Obtiene categorías de UN proveedor específico.
        
        DEBES usar step1_list_providers() PRIMERO.
        
        Args:
            provider: Nombre exacto del proveedor (aws, azure, gcp, k8s, onprem, etc.)
        
        Returns:
            Lista de categorías del proveedor seleccionado
        """
        try:
            provider = provider.lower()
            categories = self.diagram_service.get_provider_categories(provider)
            
            if not categories:
                return f"❌ Proveedor '{provider}' no encontrado.\n\n🔥 **DEBES USAR:** step1_list_providers() para ver opciones válidas"
            
            response = f"🔥 **PASO 2: CATEGORÍAS DE {provider.upper()}**\n\n"
            for i, category in enumerate(categories, 1):
                nodes_count = len(self.diagram_service.get_category_nodes(provider, category))
                response += f"{i}. **{category}** ({nodes_count} nodos)\n"
            
            response += f"\n✅ **Total:** {len(categories)} categorías"
            response += f"\n\n🔥 **SIGUIENTE PASO OBLIGATORIO:** step3_get_nodes(\"{provider}\", \"categoria\")"
            response += f"\n💡 **Ejemplo:** step3_get_nodes(\"{provider}\", \"compute\") para ver nodos de compute"
            
            return response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"