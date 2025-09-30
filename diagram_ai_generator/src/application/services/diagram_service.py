"""
Servicio simplificado para generación de diagramas
"""
import json
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from PIL import Image
import io

from diagrams import Diagram, Cluster, Edge
from diagrams.generic import Generic
import importlib


class DiagramService:
    """Servicio simple para generar diagramas"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.images_dir = self.project_root / "generated_diagrams"
        self.images_dir.mkdir(exist_ok=True)
        
        # Cargar estructura de proveedores desde JSON
        self.providers_data = self._load_providers_data()
        self.node_classes_cache = {}
    
    def _load_providers_data(self) -> Dict[str, Any]:
        """Carga los datos de proveedores desde el JSON"""
        try:
            json_path = self.project_root / "src" / "infrastructure" / "external" / "diagrams_structure.json"
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando providers data: {e}")
            return {}
    
    def create_diagram_from_spec(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un diagrama a partir de una especificación JSON
        
        Args:
            spec: Especificación del diagrama con formato:
            {
                "title": "Título del diagrama",
                "provider": "aws|azure|gcp|generic",
                "layout": "vertical|horizontal",
                "components": [
                    {
                        "id": "web1",
                        "type": "EC2",
                        "category": "compute", 
                        "label": "Web Server"
                    }
                ],
                "connections": [
                    {
                        "from": "web1",
                        "to": "db1",
                        "label": "connects to",
                        "color": "darkgreen",
                        "style": "dashed"
                    }
                ],
                "clusters": [
                    {
                        "name": "Service Cluster",
                        "components": ["web1", "web2"]
                    }
                ]
            }
        
        Returns:
            Dict con información del diagrama generado
        """
        try:
            title = spec.get('title', 'Diagrama')
            provider = spec.get('provider', 'aws').lower()
            layout = spec.get('layout', 'vertical')
            components = spec.get('components', [])
            connections = spec.get('connections', [])
            clusters = spec.get('clusters', [])
            
            # Crear nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:50]
            filename = f"{safe_title}_{timestamp}" if safe_title else f"diagram_{timestamp}"
            output_path = str(self.images_dir / filename)
            
            # Crear diagrama
            direction = "TB" if layout == "vertical" else "LR"
            with Diagram(
                title, 
                filename=output_path, 
                show=False, 
                direction=direction,
                graph_attr={"dpi": "150", "size": "12,10", "bgcolor": "white"}
            ):
                diagram_nodes = {}
                
                # Crear mapa de componentes por cluster
                cluster_components = {}
                for cluster in clusters:
                    cluster_components[cluster['name']] = cluster.get('components', [])
                
                # Componentes que no están en ningún cluster
                unclustered_components = [
                    comp for comp in components 
                    if not any(comp['id'] in cluster_comps for cluster_comps in cluster_components.values())
                ]
                
                # Crear componentes no agrupados
                for comp in unclustered_components:
                    # Usar component_provider si está especificado, sino usar provider general
                    comp_provider = comp.get('component_provider', provider)
                    node_class = self._get_node_class(
                        comp_provider, 
                        comp.get('category', 'generic'), 
                        comp.get('type', 'Generic')
                    )
                    label = comp.get('label', comp.get('id', 'Component'))
                    diagram_nodes[comp['id']] = node_class(label)
                
                # Crear clusters
                for cluster in clusters:
                    cluster_name = cluster['name']
                    cluster_comps = cluster.get('components', [])
                    
                    with Cluster(cluster_name):
                        for comp_id in cluster_comps:
                            # Encontrar el componente por ID
                            comp = next((c for c in components if c['id'] == comp_id), None)
                            if comp:
                                # Usar component_provider si está especificado, sino usar provider general
                                comp_provider = comp.get('component_provider', provider)
                                node_class = self._get_node_class(
                                    comp_provider, 
                                    comp.get('category', 'generic'), 
                                    comp.get('type', 'Generic')
                                )
                                label = comp.get('label', comp.get('id', 'Component'))
                                diagram_nodes[comp['id']] = node_class(label)
                
                # Crear conexiones con estilos
                for conn in connections:
                    source = diagram_nodes.get(conn['from'])
                    target = diagram_nodes.get(conn['to'])
                    
                    if source and target:
                        # Crear edge con estilos opcionales
                        edge_kwargs = {}
                        if conn.get('label'):
                            edge_kwargs['label'] = conn['label']
                        if conn.get('color'):
                            edge_kwargs['color'] = conn['color']
                        if conn.get('style'):
                            edge_kwargs['style'] = conn['style']
                        
                        if edge_kwargs:
                            source >> Edge(**edge_kwargs) >> target
                        else:
                            source >> target
            
            # Obtener ruta del archivo generado
            image_path = f"{output_path}.png"
            
            if Path(image_path).exists():
                # Optimizar imagen
                image_data = self._optimize_image(image_path)
                image_size_mb = len(image_data) * 3 / 4 / 1024 / 1024
                
                return {
                    'success': True,
                    'title': title,
                    'file_path': image_path,
                    'image_base64': image_data,
                    'image_size_mb': round(image_size_mb, 2),
                    'components_count': len(components),
                    'connections_count': len(connections),
                    'provider': provider.upper()
                }
            else:
                return {
                    'success': False,
                    'error': f'No se pudo generar el archivo: {image_path}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error generando diagrama: {str(e)}'
            }
    
    def _get_node_class(self, provider: str, category: str, node_type: str):
        """Obtiene la clase de nodo apropiada usando importación dinámica con sugerencias"""
        cache_key = f"{provider}_{category}_{node_type}"
        
        if cache_key in self.node_classes_cache:
            return self.node_classes_cache[cache_key]
        
        try:
            # Verificar que el proveedor y categoría existen en nuestros datos
            if (provider in self.providers_data and 
                category in self.providers_data[provider] and
                node_type in self.providers_data[provider][category]):
                
                # Intentar importar el módulo dinámicamente
                module_name = f"diagrams.{provider}.{category}"
                module = importlib.import_module(module_name)
                
                if hasattr(module, node_type):
                    node_class = getattr(module, node_type)
                    self.node_classes_cache[cache_key] = node_class
                    return node_class
            
            # Si no se encuentra exacto, buscar sugerencias y logging
            suggestions = self._find_node_suggestions(provider, category, node_type)
            if suggestions:
                print(f"⚠️  NODO NO ENCONTRADO: '{node_type}' en {provider}/{category}")
                print(f"💡 SUGERENCIAS: {', '.join(suggestions[:3])}")
                
                # Usar la primera sugerencia automáticamente
                best_match = suggestions[0]
                try:
                    module_name = f"diagrams.{provider}.{category}"
                    module = importlib.import_module(module_name)
                    if hasattr(module, best_match):
                        node_class = getattr(module, best_match)
                        self.node_classes_cache[cache_key] = node_class
                        print(f"✅ USANDO SUGERENCIA: '{best_match}' en lugar de '{node_type}'")
                        return node_class
                except:
                    pass
            
            # Fallback a Generic
            self.node_classes_cache[cache_key] = Generic
            return Generic
            
        except (ImportError, AttributeError, KeyError) as e:
            # Fallback a Generic en caso de error
            self.node_classes_cache[cache_key] = Generic
            return Generic
    
    def _find_node_suggestions(self, provider: str, category: str, node_type: str) -> list:
        """Encuentra sugerencias de nodos similares"""
        suggestions = []
        
        if provider not in self.providers_data or category not in self.providers_data[provider]:
            return suggestions
        
        available_nodes = self.providers_data[provider][category]
        node_lower = node_type.lower()
        
        # Buscar coincidencias exactas (case-insensitive)
        for node in available_nodes:
            if node.lower() == node_lower:
                suggestions.append(node)
        
        # Buscar coincidencias que contengan el texto
        for node in available_nodes:
            if node_lower in node.lower() or node.lower() in node_lower:
                if node not in suggestions:
                    suggestions.append(node)
        
        # Buscar coincidencias por similitud (primeras letras)
        for node in available_nodes:
            if (len(node_lower) >= 3 and len(node) >= 3 and 
                node.lower()[:3] == node_lower[:3]):
                if node not in suggestions:
                    suggestions.append(node)
        
        return suggestions[:5]  # Máximo 5 sugerencias
    
    def _optimize_image(self, image_path: str) -> str:
        """Optimiza la imagen y retorna base64"""
        try:
            with Image.open(image_path) as img:
                # Convertir a RGB si es necesario
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Redimensionar si es muy grande
                max_width, max_height = 1000, 800
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Guardar optimizado
                buffer = io.BytesIO()
                img.save(buffer, format='PNG', optimize=True, compress_level=9)
                return base64.b64encode(buffer.getvalue()).decode('utf-8')
                
        except Exception as e:
            # Si falla la optimización, leer el archivo original
            with open(image_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
    
    
    def get_available_providers(self) -> List[str]:
        """Retorna lista de proveedores disponibles"""
        return list(self.providers_data.keys())
    
    def get_provider_categories(self, provider: str) -> List[str]:
        """Retorna las categorías disponibles para un proveedor"""
        return list(self.providers_data.get(provider, {}).keys())
    
    def get_category_nodes(self, provider: str, category: str) -> List[str]:
        """Retorna los nodos disponibles para una categoría de proveedor"""
        return self.providers_data.get(provider, {}).get(category, [])
    
    def search_nodes(self, query: str, provider: str = None) -> List[Dict[str, str]]:
        """Busca nodos por nombre"""
        results = []
        
        for prov_name, categories in self.providers_data.items():
            if provider and prov_name != provider:
                continue
                
            for cat_name, nodes in categories.items():
                for node_name in nodes:
                    if query.lower() in node_name.lower():
                        results.append({
                            'name': node_name,
                            'provider': prov_name,
                            'category': cat_name,
                            'description': f'Nodo {node_name} de {prov_name.upper()}'
                        })
        
        return results
