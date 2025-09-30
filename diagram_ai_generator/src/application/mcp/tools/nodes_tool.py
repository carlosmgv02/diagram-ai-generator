from typing import List
from src.application.mcp.tools.base_tool import BaseTool, register_tool

class NodesTool(BaseTool):
    @register_tool
    def step3_get_nodes(self, provider: str, category: str) -> str:
        """
        🔥 PASO 3 OBLIGATORIO: Obtiene TODOS los nodos de una categoría específica.
        
        DEBES usar step2_get_categories() PRIMERO.
        
        Args:
            provider: Proveedor (aws, azure, gcp, k8s, etc.)
            category: Categoría exacta (compute, network, database, etc.)
        
        Returns:
            Lista completa de nodos para usar en create_diagram_from_json
        """
        try:
            provider = provider.lower()
            nodes = self.diagram_service.get_category_nodes(provider, category)
            
            if not nodes:
                return f"❌ No se encontraron nodos para {provider}/{category}\n\n🔥 **DEBES USAR:** step2_get_categories(\"{provider}\") para ver categorías válidas"
            
            response = f"🔥 **PASO 3: NODOS DE {provider.upper()}/{category.upper()}**\n\n"
            for i, node in enumerate(nodes, 1):
                response += f"{i}. **{node}**\n"
            
            response += f"\n✅ **Total:** {len(nodes)} nodos disponibles"
            response += f"\n\n🔥 **USAR ESTOS NOMBRES EXACTOS EN create_diagram_from_json**"
            response += f"\n💡 **Formato JSON:** {{\"type\": \"{nodes[0] if nodes else 'NombreNodo'}\", \"category\": \"{category}\"}}"
            
            response += f"\n\n✅ **¡FLUJO COMPLETADO! Ahora puedes usar create_diagram_from_json()**"
            
            return response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"