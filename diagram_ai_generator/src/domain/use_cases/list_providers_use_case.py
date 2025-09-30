"""
Caso de uso para listar proveedores y nodos disponibles
"""
from typing import List, Optional

from ..entities.provider import DiagramProvider, DiagramCategory, DiagramNodeInfo
from ..repositories.diagram_repository import DiagramRepository


class ListProvidersUseCase:
    """Caso de uso para listar proveedores de diagramas"""
    
    def __init__(self, diagram_repository: DiagramRepository):
        self.diagram_repository = diagram_repository
    
    def get_all_providers(self) -> List[DiagramProvider]:
        """
        Obtiene todos los proveedores disponibles
        
        Returns:
            List[DiagramProvider]: Lista de proveedores
        """
        registry = self.diagram_repository.get_providers_registry()
        return list(registry.providers.values())
    
    def get_provider_categories(self, provider_name: str) -> List[DiagramCategory]:
        """
        Obtiene las categorías de un proveedor específico
        
        Args:
            provider_name: Nombre del proveedor
            
        Returns:
            List[DiagramCategory]: Lista de categorías
        """
        registry = self.diagram_repository.get_providers_registry()
        return registry.get_categories_for_provider(provider_name)
    
    def get_category_nodes(self, provider_name: str, category_name: str) -> List[str]:
        """
        Obtiene los nodos de una categoría específica
        
        Args:
            provider_name: Nombre del proveedor
            category_name: Nombre de la categoría
            
        Returns:
            List[str]: Lista de nombres de nodos
        """
        registry = self.diagram_repository.get_providers_registry()
        return registry.get_nodes_for_category(provider_name, category_name)
    
    def search_nodes(self, query: str, provider_filter: Optional[str] = None) -> List[DiagramNodeInfo]:
        """
        Busca nodos por nombre o alias
        
        Args:
            query: Término de búsqueda
            provider_filter: Filtrar por proveedor específico (opcional)
            
        Returns:
            List[DiagramNodeInfo]: Lista de nodos encontrados
        """
        registry = self.diagram_repository.get_providers_registry()
        results = registry.search_nodes(query)
        
        if provider_filter:
            results = [node for node in results if node.provider.lower() == provider_filter.lower()]
        
        return results
    
    def get_provider_summary(self) -> dict:
        """
        Obtiene un resumen de todos los proveedores
        
        Returns:
            dict: Resumen con estadísticas de proveedores
        """
        providers = self.get_all_providers()
        
        total_providers = len(providers)
        total_nodes = sum(provider.total_nodes for provider in providers)
        
        provider_stats = {}
        for provider in providers:
            categories = self.get_provider_categories(provider.name)
            provider_stats[provider.name] = {
                "display_name": provider.display_name,
                "total_nodes": provider.total_nodes,
                "categories_count": len(categories),
                "categories": [cat.name for cat in categories]
            }
        
        return {
            "total_providers": total_providers,
            "total_nodes": total_nodes,
            "providers": provider_stats
        }