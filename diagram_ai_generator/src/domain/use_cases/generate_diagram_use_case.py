"""
Caso de uso principal para generar diagramas
"""
import time
from typing import Optional

from ..entities.diagram import DiagramRequest, DiagramResult, OutputFormat
from ..repositories.ai_provider_repository import AIProviderRepository
from ..repositories.diagram_repository import DiagramRepository


class GenerateDiagramUseCase:
    """Caso de uso para generar diagramas usando IA"""
    
    def __init__(
        self, 
        ai_provider: AIProviderRepository,
        diagram_repository: DiagramRepository
    ):
        self.ai_provider = ai_provider
        self.diagram_repository = diagram_repository
    
    async def execute(self, request: DiagramRequest) -> DiagramResult:
        """
        Ejecuta la generación completa de un diagrama
        
        Args:
            request: Solicitud de generación del diagrama
            
        Returns:
            DiagramResult: Resultado de la operación
        """
        start_time = time.time()
        
        try:
            # 1. Generar especificación usando IA
            spec = await self.ai_provider.generate_diagram_spec(request)
            
            # 2. Validar especificación
            is_valid, errors = self.diagram_repository.validate_spec(spec)
            if not is_valid:
                return DiagramResult(
                    success=False,
                    error_message=f"Especificación inválida: {', '.join(errors)}",
                    generation_time=time.time() - start_time
                )
            
            # 3. Generar diagrama físico
            output_path = request.output_path or f"diagram_{int(time.time())}.{request.output_format.value}"
            result = await self.diagram_repository.generate_diagram(
                spec, 
                output_path, 
                request.output_format.value
            )
            
            # 4. Actualizar tiempo de generación
            result.generation_time = time.time() - start_time
            result.spec = spec
            
            return result
            
        except Exception as e:
            return DiagramResult(
                success=False,
                error_message=f"Error durante la generación: {str(e)}",
                generation_time=time.time() - start_time
            )