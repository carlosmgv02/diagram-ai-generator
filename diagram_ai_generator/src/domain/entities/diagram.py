"""
Entidades del dominio para diagramas
"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime


class DiagramType(Enum):
    """Tipos de diagramas disponibles"""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    KUBERNETES = "k8s"
    ON_PREMISE = "onprem"
    GENERIC = "generic"
    PROGRAMMING = "programming"
    C4 = "c4"
    CUSTOM = "custom"


class OutputFormat(Enum):
    """Formatos de salida para diagramas"""
    PNG = "png"
    SVG = "svg"
    PDF = "pdf"
    DOT = "dot"


@dataclass
class DiagramNode:
    """Representa un nodo en el diagrama"""
    name: str
    node_type: str
    provider: str
    category: str
    properties: Dict[str, str] = None
    
    def __post_init__(self):
        if self.properties is None:
            self.properties = {}


@dataclass
class DiagramConnection:
    """Representa una conexión entre nodos"""
    source: str
    target: str
    label: Optional[str] = None
    style: Optional[str] = None


@dataclass
class DiagramRequest:
    """Solicitud para generar un diagrama"""
    prompt: str
    diagram_type: Optional[DiagramType] = None
    output_format: OutputFormat = OutputFormat.PNG
    output_path: Optional[str] = None
    title: Optional[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class DiagramSpec:
    """Especificación completa de un diagrama"""
    title: str
    description: str
    nodes: List[DiagramNode]
    connections: List[DiagramConnection]
    diagram_type: DiagramType
    layout: Optional[str] = None
    metadata: Dict[str, str] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class DiagramResult:
    """Resultado de la generación de un diagrama"""
    success: bool
    file_path: Optional[str] = None
    error_message: Optional[str] = None
    spec: Optional[DiagramSpec] = None
    generation_time: Optional[float] = None