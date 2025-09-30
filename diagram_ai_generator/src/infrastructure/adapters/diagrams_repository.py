"""
Implementación del repositorio de diagramas usando la librería diagrams
"""
import json
import os
import tempfile
import importlib
from typing import List, Dict, Any, Optional
from pathlib import Path

from diagrams import Diagram, Node, Edge
from diagrams.aws import compute as aws_compute, network as aws_network, database as aws_database
from diagrams.azure import compute as azure_compute, network as azure_network, database as azure_database
from diagrams.gcp import compute as gcp_compute, network as gcp_network, database as gcp_database

from ...domain.entities.diagram import DiagramResult, DiagramSpec
from ...domain.entities.provider import ProvidersRegistry, DiagramProvider, DiagramCategory, DiagramNodeInfo
from ...domain.repositories.diagram_repository import DiagramRepository
from ...domain.exceptions import DiagramRenderingError, DiagramValidationError


class DiagramsRepository(DiagramRepository):
    """Implementación del repositorio usando la librería diagrams de Python"""
    
    def __init__(self):
        self.providers_registry = self._load_providers_registry()
        self.node_classes_cache = {}
    
    def _load_providers_registry(self) -> ProvidersRegistry:
        """Carga el registro de proveedores desde el archivo JSON"""
        try:
            providers_file = os.path.join(
                os.path.dirname(__file__), 
                "..", 
                "external", 
                "diagrams_structure.json"
            )
            with open(providers_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            providers = {}
            categories = {}
            nodes = {}
            
            for provider_name, provider_data in data.items():
                # Crear proveedor
                total_nodes = sum(len(nodes_list) for nodes_list in provider_data.values())
                provider = DiagramProvider(
                    name=provider_name.lower(),
                    display_name=provider_name.upper(),
                    description=f"Proveedor {provider_name.upper()}",
                    categories=list(provider_data.keys()),
                    total_nodes=total_nodes
                )
                providers[provider_name.lower()] = provider
                
                # Crear categorías
                provider_categories = []
                for category_name, nodes_list in provider_data.items():
                    category = DiagramCategory(
                        name=category_name,
                        provider=provider_name.lower(),
                        nodes=nodes_list,
                        description=f"Categoría {category_name} de {provider_name.upper()}"
                    )
                    provider_categories.append(category)
                    
                    # Crear nodos
                    for node_name in nodes_list:
                        node_info = DiagramNodeInfo(
                            name=node_name,
                            provider=provider_name.lower(),
                            category=category_name,
                            description=f"Nodo {node_name} de {provider_name.upper()}"
                        )
                        nodes[f"{provider_name.lower()}_{category_name}_{node_name}"] = node_info
                
                categories[provider_name.lower()] = provider_categories
            
            return ProvidersRegistry(
                providers=providers,
                categories=categories,
                nodes=nodes
            )
            
        except Exception as e:
            # Fallback a registro vacío si hay error
            return ProvidersRegistry(providers={}, categories={}, nodes={})
    
    def _get_node_class(self, provider: str, category: str, node_type: str) -> Optional[type]:
        """Obtiene la clase de nodo correspondiente de la librería diagrams"""
        cache_key = f"{provider}_{category}_{node_type}"
        
        if cache_key in self.node_classes_cache:
            return self.node_classes_cache[cache_key]
        
        try:
            # Mapeo de proveedores a módulos
            provider_modules = {
                'aws': 'diagrams.aws',
                'azure': 'diagrams.azure', 
                'gcp': 'diagrams.gcp',
                'k8s': 'diagrams.k8s',
                'onprem': 'diagrams.onprem',
                'generic': 'diagrams.generic',
                'programming': 'diagrams.programming'
            }
            
            if provider not in provider_modules:
                return None
            
            # Importar módulo de categoría
            module_name = f"{provider_modules[provider]}.{category}"
            module = importlib.import_module(module_name)
            
            # Buscar la clase del nodo
            if hasattr(module, node_type):
                node_class = getattr(module, node_type)
                self.node_classes_cache[cache_key] = node_class
                return node_class
            
        except (ImportError, AttributeError):
            pass
        
        # Fallback a nodo genérico
        try:
            from diagrams.generic import Generic
            self.node_classes_cache[cache_key] = Generic
            return Generic
        except ImportError:
            return None
    
    async def generate_diagram(self, spec: DiagramSpec, output_path: str, format: str = "png") -> DiagramResult:
        """Genera un diagrama físico usando la librería diagrams"""
        try:
            # Configurar directorio de salida
            output_dir = os.path.dirname(output_path) or "."
            os.makedirs(output_dir, exist_ok=True)
            
            # Configurar nombre del archivo (sin extensión para diagrams)
            filename = os.path.splitext(os.path.basename(output_path))[0]
            
            # Crear diagrama
            with Diagram(
                name=spec.title,
                filename=os.path.join(output_dir, filename),
                show=False,
                outformat=format,
                direction="TB" if spec.layout != "horizontal" else "LR"
            ):
                # Crear nodos
                diagram_nodes = {}
                for node_spec in spec.nodes:
                    node_class = self._get_node_class(
                        node_spec.provider, 
                        node_spec.category, 
                        node_spec.node_type
                    )
                    
                    if node_class:
                        label = node_spec.properties.get('label', node_spec.name)
                        diagram_nodes[node_spec.name] = node_class(label)
                    else:
                        # Usar nodo genérico como fallback
                        from diagrams.generic import Generic
                        label = node_spec.properties.get('label', node_spec.name)
                        diagram_nodes[node_spec.name] = Generic(label)
                
                # Crear conexiones
                for connection in spec.connections:
                    source_node = diagram_nodes.get(connection.source)
                    target_node = diagram_nodes.get(connection.target)
                    
                    if source_node and target_node:
                        if connection.label:
                            source_node >> Edge(label=connection.label) >> target_node
                        else:
                            source_node >> target_node
            
            # Verificar que el archivo se generó
            expected_file = f"{os.path.join(output_dir, filename)}.{format}"
            if os.path.exists(expected_file):
                return DiagramResult(
                    success=True,
                    file_path=expected_file,
                    spec=spec
                )
            else:
                return DiagramResult(
                    success=False,
                    error_message=f"El archivo {expected_file} no se generó correctamente"
                )
                
        except Exception as e:
            return DiagramResult(
                success=False,
                error_message=f"Error generando diagrama: {str(e)}"
            )
    
    def get_providers_registry(self) -> ProvidersRegistry:
        """Obtiene el registro de proveedores"""
        return self.providers_registry
    
    def validate_spec(self, spec: DiagramSpec) -> tuple[bool, List[str]]:
        """Valida una especificación de diagrama"""
        errors = []
        
        # Validar que hay al menos un nodo
        if not spec.nodes:
            errors.append("El diagrama debe tener al menos un nodo")
        
        # Validar nombres únicos de nodos
        node_names = [node.name for node in spec.nodes]
        if len(node_names) != len(set(node_names)):
            errors.append("Los nombres de nodos deben ser únicos")
        
        # Validar conexiones
        for connection in spec.connections:
            if connection.source not in node_names:
                errors.append(f"Nodo fuente '{connection.source}' no existe")
            if connection.target not in node_names:
                errors.append(f"Nodo destino '{connection.target}' no existe")
        
        # Validar que el proveedor existe
        if spec.diagram_type.value not in self.providers_registry.providers:
            # Advertencia, no error crítico
            pass
        
        return len(errors) == 0, errors