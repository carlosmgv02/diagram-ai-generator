"""
Repository interface para diagramas
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.diagram import DiagramResult, DiagramSpec
from ..entities.provider import ProvidersRegistry


class DiagramRepository(ABC):
    """Interface para el repositorio de diagramas"""
    
    @abstractmethod
    async def generate_diagram(self, spec: DiagramSpec, output_path: str, format: str = "png") -> DiagramResult:
        """
        Genera un diagrama físico basado en la especificación
        
        Args:
            spec: Especificación del diagrama
            output_path: Ruta donde guardar el diagrama
            format: Formato de salida (png, svg, pdf)
            
        Returns:
            DiagramResult: Resultado de la generación
        """
        pass
    
    @abstractmethod
    def get_providers_registry(self) -> ProvidersRegistry:
        """
        Obtiene el registro de proveedores disponibles
        
        Returns:
            ProvidersRegistry: Registro con todos los proveedores y nodos
        """
        pass
    
    @abstractmethod
    def validate_spec(self, spec: DiagramSpec) -> tuple[bool, List[str]]:
        """
        Valida una especificación de diagrama
        
        Args:
            spec: Especificación a validar
            
        Returns:
            tuple: (es_válida, lista_de_errores)
        """
        pass