"""
Servidor MCP para Diagram AI Generator
Proporciona herramientas para listar proveedores, categorías y nodos de diagramas
"""
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from ...domain.use_cases.list_providers_use_case import ListProvidersUseCase
from ...infrastructure.adapters.diagrams_repository import DiagramsRepository


# Crear servidor MCP
mcp = FastMCP("Diagram AI Generator")

# Inicializar dependencias
diagram_repository = DiagramsRepository()
list_providers_use_case = ListProvidersUseCase(diagram_repository)


class ProviderInfo(BaseModel):
    """Información de un proveedor"""
    name: str
    display_name: str
    total_nodes: int
    categories_count: int
    categories: List[str]


class CategoryInfo(BaseModel):
    """Información de una categoría"""
    name: str
    provider: str
    nodes_count: int
    nodes: List[str]


class NodeInfo(BaseModel):
    """Información de un nodo"""
    name: str
    provider: str
    category: str
    description: Optional[str] = None


@mcp.tool()
def list_all_providers() -> List[ProviderInfo]:
    """
    Lista todos los proveedores de diagramas disponibles.
    
    Returns:
        Lista de proveedores con su información básica.
    """
    summary = list_providers_use_case.get_provider_summary()
    
    providers = []
    for provider_name, stats in summary['providers'].items():
        providers.append(ProviderInfo(
            name=provider_name,
            display_name=stats['display_name'],
            total_nodes=stats['total_nodes'],
            categories_count=stats['categories_count'],
            categories=stats['categories']
        ))
    
    return providers


@mcp.tool()
def get_provider_categories(provider_name: str) -> List[CategoryInfo]:
    """
    Obtiene las categorías de un proveedor específico.
    
    Args:
        provider_name: Nombre del proveedor (aws, azure, gcp, etc.)
    
    Returns:
        Lista de categorías del proveedor con información de nodos.
    """
    categories = list_providers_use_case.get_provider_categories(provider_name.lower())
    
    result = []
    for category in categories:
        result.append(CategoryInfo(
            name=category.name,
            provider=category.provider,
            nodes_count=len(category.nodes),
            nodes=category.nodes
        ))
    
    return result


@mcp.tool()
def get_category_nodes(provider_name: str, category_name: str) -> List[str]:
    """
    Obtiene los nodos de una categoría específica.
    
    Args:
        provider_name: Nombre del proveedor (aws, azure, gcp, etc.)
        category_name: Nombre de la categoría (compute, network, database, etc.)
    
    Returns:
        Lista de nombres de nodos en la categoría.
    """
    return list_providers_use_case.get_category_nodes(provider_name.lower(), category_name)


@mcp.tool()
def search_nodes(query: str, provider_filter: Optional[str] = None, limit: int = 20) -> List[NodeInfo]:
    """
    Busca nodos por nombre o alias.
    
    Args:
        query: Término de búsqueda
        provider_filter: Filtrar por proveedor específico (opcional)
        limit: Límite máximo de resultados (default: 20)
    
    Returns:
        Lista de nodos que coinciden con la búsqueda.
    """
    results = list_providers_use_case.search_nodes(query, provider_filter)
    results = results[:limit]  # Limitar resultados
    
    nodes = []
    for node in results:
        nodes.append(NodeInfo(
            name=node.name,
            provider=node.provider,
            category=node.category,
            description=node.description
        ))
    
    return nodes


@mcp.tool()
def get_providers_summary() -> Dict[str, Any]:
    """
    Obtiene un resumen estadístico de todos los proveedores.
    
    Returns:
        Diccionario con estadísticas generales de proveedores.
    """
    return list_providers_use_case.get_provider_summary()


@mcp.tool()
def get_provider_examples(provider_name: str, limit: int = 5) -> Dict[str, List[str]]:
    """
    Obtiene ejemplos de nodos por categoría para un proveedor.
    
    Args:
        provider_name: Nombre del proveedor
        limit: Número máximo de ejemplos por categoría
    
    Returns:
        Diccionario con categorías como claves y listas de nodos como valores.
    """
    categories = list_providers_use_case.get_provider_categories(provider_name.lower())
    
    examples = {}
    for category in categories:
        examples[category.name] = category.nodes[:limit]
    
    return examples


# Recursos dinámicos
@mcp.resource("provider://{provider_name}")
def get_provider_resource(provider_name: str) -> str:
    """
    Recurso dinámico para obtener información detallada de un proveedor.
    
    Args:
        provider_name: Nombre del proveedor
    
    Returns:
        Información formateada del proveedor.
    """
    categories = list_providers_use_case.get_provider_categories(provider_name.lower())
    
    if not categories:
        return f"Proveedor '{provider_name}' no encontrado."
    
    total_nodes = sum(len(cat.nodes) for cat in categories)
    
    result = f"# Proveedor: {provider_name.upper()}\n\n"
    result += f"**Total de nodos:** {total_nodes}\n"
    result += f"**Categorías:** {len(categories)}\n\n"
    
    for category in categories:
        result += f"## {category.name.title()} ({len(category.nodes)} nodos)\n"
        examples = category.nodes[:10]  # Primeros 10 como ejemplo
        result += f"Ejemplos: {', '.join(examples)}\n"
        if len(category.nodes) > 10:
            result += f"... y {len(category.nodes) - 10} más\n"
        result += "\n"
    
    return result


@mcp.resource("category://{provider_name}/{category_name}")
def get_category_resource(provider_name: str, category_name: str) -> str:
    """
    Recurso dinámico para obtener información de una categoría específica.
    
    Args:
        provider_name: Nombre del proveedor
        category_name: Nombre de la categoría
    
    Returns:
        Lista de nodos en la categoría.
    """
    nodes = list_providers_use_case.get_category_nodes(provider_name.lower(), category_name)
    
    if not nodes:
        return f"Categoría '{category_name}' no encontrada en el proveedor '{provider_name}'."
    
    result = f"# {provider_name.upper()} - {category_name.title()}\n\n"
    result += f"**Total de nodos:** {len(nodes)}\n\n"
    result += "## Nodos disponibles:\n"
    
    for i, node in enumerate(nodes, 1):
        result += f"{i}. {node}\n"
    
    return result


# Prompts
@mcp.prompt()
def diagram_generation_prompt(
    architecture_description: str, 
    provider: str = "auto",
    complexity: str = "medium"
) -> str:
    """
    Genera un prompt optimizado para crear diagramas de arquitectura.
    
    Args:
        architecture_description: Descripción de la arquitectura deseada
        provider: Proveedor preferido (aws, azure, gcp, etc.) o "auto" para selección automática
        complexity: Nivel de complejidad (simple, medium, complex)
    
    Returns:
        Prompt optimizado para la generación de diagramas.
    """
    prompt = f"""Crea un diagrama de arquitectura para: {architecture_description}

Configuración:
- Proveedor preferido: {provider}
- Nivel de complejidad: {complexity}

Instrucciones específicas:
1. Identifica los componentes principales mencionados en la descripción
2. Selecciona el proveedor más apropiado si se especificó "auto"
3. Incluye las conexiones lógicas entre componentes
4. Considera las mejores prácticas de arquitectura
5. Agrega etiquetas descriptivas a las conexiones

Genera un diagrama técnicamente preciso y visualmente claro."""

    return prompt


@mcp.prompt()
def node_suggestion_prompt(query: str, provider: Optional[str] = None) -> str:
    """
    Genera sugerencias de nodos basadas en una consulta.
    
    Args:
        query: Consulta o descripción del componente buscado
        provider: Proveedor específico para filtrar (opcional)
    
    Returns:
        Prompt con sugerencias de nodos relevantes.
    """
    # Buscar nodos relevantes
    results = list_providers_use_case.search_nodes(query, provider, limit=10)
    
    if not results:
        return f"No se encontraron nodos para '{query}'. Intenta con términos más generales."
    
    prompt = f"Nodos sugeridos para '{query}':\n\n"
    
    for node in results:
        prompt += f"- **{node.name}** ({node.provider.upper()} - {node.category})\n"
    
    prompt += f"\nTotal encontrados: {len(results)} nodos"
    
    if provider:
        prompt += f" en {provider.upper()}"
    
    return prompt


if __name__ == "__main__":
    # Para ejecutar el servidor MCP
    mcp.run()