"""Diagram specification value object"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass(frozen=True)
class Component:
    """Represents a diagram component"""
    id: str
    type: str
    category: str = "generic"
    label: Optional[str] = None
    component_provider: Optional[str] = None
    
    def get_label(self) -> str:
        """Get component label, fallback to id"""
        return self.label or self.id


@dataclass(frozen=True)
class Connection:
    """Represents a connection between components"""
    from_id: str
    to_id: str
    label: Optional[str] = None
    color: Optional[str] = None
    style: Optional[str] = None


@dataclass(frozen=True)
class ComponentCluster:
    """Represents a logical grouping of components"""
    name: str
    component_ids: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class DiagramSpecification:
    """Complete specification for diagram generation"""
    title: str
    provider: str = "aws"
    layout: str = "vertical"
    components: List[Component] = field(default_factory=list)
    connections: List[Connection] = field(default_factory=list)
    clusters: List[ComponentCluster] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, spec: Dict[str, Any]) -> 'DiagramSpecification':
        """Create specification from dictionary"""
        components = [
            Component(
                id=c['id'],
                type=c.get('type', 'Generic'),
                category=c.get('category', 'generic'),
                label=c.get('label'),
                component_provider=c.get('component_provider')
            )
            for c in spec.get('components', [])
        ]
        
        connections = [
            Connection(
                from_id=c['from'],
                to_id=c['to'],
                label=c.get('label'),
                color=c.get('color'),
                style=c.get('style')
            )
            for c in spec.get('connections', [])
        ]
        
        clusters = [
            ComponentCluster(
                name=cl['name'],
                component_ids=cl.get('components', [])
            )
            for cl in spec.get('clusters', [])
        ]
        
        return cls(
            title=spec.get('title', 'Diagram'),
            provider=spec.get('provider', 'aws').lower(),
            layout=spec.get('layout', 'vertical'),
            components=components,
            connections=connections,
            clusters=clusters
        )
    
    def get_direction(self) -> str:
        """Get graph direction based on layout"""
        return "TB" if self.layout == "vertical" else "LR"
    
    def get_unclustered_components(self) -> List[Component]:
        """Get components not in any cluster"""
        clustered_ids = set()
        for cluster in self.clusters:
            clustered_ids.update(cluster.component_ids)
        
        return [c for c in self.components if c.id not in clustered_ids]
    
    def get_component_by_id(self, component_id: str) -> Optional[Component]:
        """Find component by ID"""
        return next((c for c in self.components if c.id == component_id), None)

