"""
Entidades para proveedores de diagramas
"""
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class DiagramProvider:
    """Representa un proveedor de diagramas (AWS, Azure, etc.)"""
    name: str
    display_name: str
    description: str
    categories: List[str]
    total_nodes: int


@dataclass
class DiagramCategory:
    """Representa una categoría dentro de un proveedor"""
    name: str
    provider: str
    nodes: List[str]
    description: Optional[str] = None


@dataclass
class DiagramNodeInfo:
    """Información detallada de un nodo"""
    name: str
    provider: str
    category: str
    icon_path: Optional[str] = None
    description: Optional[str] = None
    aliases: List[str] = None
    
    def __post_init__(self):
        if self.aliases is None:
            self.aliases = []


@dataclass
class ProvidersRegistry:
    """Registro de todos los proveedores disponibles"""
    providers: Dict[str, DiagramProvider]
    categories: Dict[str, List[DiagramCategory]]
    nodes: Dict[str, DiagramNodeInfo]
    
    def get_provider(self, name: str) -> Optional[DiagramProvider]:
        """Obtiene un proveedor por nombre"""
        return self.providers.get(name.lower())
    
    def get_categories_for_provider(self, provider_name: str) -> List[DiagramCategory]:
        """Obtiene las categorías de un proveedor"""
        return self.categories.get(provider_name.lower(), [])
    
    def get_nodes_for_category(self, provider_name: str, category_name: str) -> List[str]:
        """Obtiene los nodos de una categoría específica"""
        categories = self.get_categories_for_provider(provider_name)
        for category in categories:
            if category.name == category_name:
                return category.nodes
        return []
    
    def search_nodes(self, query: str) -> List[DiagramNodeInfo]:
        """Busca nodos por nombre o alias"""
        query_lower = query.lower()
        results = []
        
        for node in self.nodes.values():
            if (query_lower in node.name.lower() or 
                any(query_lower in alias.lower() for alias in node.aliases)):
                results.append(node)
        
        return results