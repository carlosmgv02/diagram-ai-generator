"""
Excepciones del dominio
"""


class DiagramGeneratorError(Exception):
    """Excepción base para errores del generador de diagramas"""
    pass


class AIProviderError(DiagramGeneratorError):
    """Error relacionado con el proveedor de IA"""
    pass


class DiagramValidationError(DiagramGeneratorError):
    """Error de validación de especificación de diagrama"""
    pass


class DiagramRenderingError(DiagramGeneratorError):
    """Error durante el renderizado del diagrama"""
    pass


class ProviderNotFoundError(DiagramGeneratorError):
    """Error cuando no se encuentra un proveedor"""
    pass


class InvalidConfigurationError(DiagramGeneratorError):
    """Error de configuración inválida"""
    pass