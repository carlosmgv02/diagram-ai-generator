"""
Repository interface para proveedores de IA
"""
from abc import ABC, abstractmethod
from typing import Optional

from ..entities.diagram import DiagramRequest, DiagramSpec


class AIProviderRepository(ABC):
    """Interface para proveedores de IA que generan especificaciones de diagramas"""
    
    @abstractmethod
    async def generate_diagram_spec(self, request: DiagramRequest) -> DiagramSpec:
        """
        Genera una especificación de diagrama basada en el prompt del usuario
        
        Args:
            request: Solicitud con el prompt y configuración
            
        Returns:
            DiagramSpec: Especificación del diagrama generada
            
        Raises:
            AIProviderError: Si hay un error en la generación
        """
        pass
    
    @abstractmethod
    async def validate_connection(self) -> bool:
        """
        Valida que la conexión con el proveedor de IA esté funcionando
        
        Returns:
            bool: True si la conexión es válida
        """
        pass
    
    @abstractmethod
    def get_provider_info(self) -> dict:
        """
        Obtiene información sobre el proveedor de IA
        
        Returns:
            dict: Información del proveedor (nombre, modelo, etc.)
        """
        pass