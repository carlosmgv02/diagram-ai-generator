"""Diagram builder using diagrams library"""
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from diagrams import Diagram, Cluster, Edge

from src.domain.value_objects.diagram_specification import DiagramSpecification, Component
from src.domain.services.node_resolver import NodeResolver


class DiagramBuilder:
    """Builds diagrams using the diagrams library"""
    
    def __init__(self, node_resolver: NodeResolver, output_dir: Path):
        """
        Initialize diagram builder
        
        Args:
            node_resolver: Service to resolve node types
            output_dir: Directory for output files
        """
        self.node_resolver = node_resolver
        self.output_dir = output_dir
    
    def build(self, spec: DiagramSpecification) -> str:
        """
        Build diagram from specification
        
        Args:
            spec: Diagram specification
        
        Returns:
            Path to generated PNG file
        """
        # Generate filename
        filename = self._generate_filename(spec.title)
        output_path = str(self.output_dir / filename)
        
        # Create diagram
        with Diagram(
            spec.title,
            filename=output_path,
            show=False,
            direction=spec.get_direction(),
            graph_attr={"dpi": "150", "size": "12,10", "bgcolor": "white"}
        ):
            # Build node map
            nodes = self._build_nodes(spec)
            
            # Create connections
            self._build_connections(spec, nodes)
        
        # Return path to PNG file
        return f"{output_path}.png"
    
    def _generate_filename(self, title: str) -> str:
        """Generate safe filename from title"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]
        return f"{safe_title}_{timestamp}" if safe_title else f"diagram_{timestamp}"
    
    def _build_nodes(self, spec: DiagramSpecification) -> Dict[str, Any]:
        """Build all diagram nodes"""
        nodes = {}
        
        # Create cluster components map
        cluster_component_ids = set()
        for cluster in spec.clusters:
            cluster_component_ids.update(cluster.component_ids)
        
        # Create unclustered nodes
        for component in spec.get_unclustered_components():
            nodes[component.id] = self._create_node(component, spec.provider)
        
        # Create clustered nodes
        for cluster in spec.clusters:
            with Cluster(cluster.name):
                for comp_id in cluster.component_ids:
                    component = spec.get_component_by_id(comp_id)
                    if component:
                        nodes[component.id] = self._create_node(component, spec.provider)
        
        return nodes
    
    def _create_node(self, component: Component, default_provider: str) -> Any:
        """Create a single diagram node"""
        provider = component.component_provider or default_provider
        node_class = self.node_resolver.resolve_node(
            provider,
            component.category,
            component.type
        )
        return node_class(component.get_label())
    
    def _build_connections(self, spec: DiagramSpecification, nodes: Dict[str, Any]):
        """Build all connections between nodes"""
        for connection in spec.connections:
            source = nodes.get(connection.from_id)
            target = nodes.get(connection.to_id)
            
            if source and target:
                edge_kwargs = self._build_edge_kwargs(connection)
                if edge_kwargs:
                    source >> Edge(**edge_kwargs) >> target
                else:
                    source >> target
    
    def _build_edge_kwargs(self, connection) -> dict:
        """Build edge kwargs from connection"""
        kwargs = {}
        if connection.label:
            kwargs['label'] = connection.label
        if connection.color:
            kwargs['color'] = connection.color
        if connection.style:
            kwargs['style'] = connection.style
        return kwargs

