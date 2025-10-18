"""
Tests para casos de uso
"""
import pytest
from unittest.mock import AsyncMock, Mock

from diagram_ai_generator.src.domain.entities.diagram import (
    DiagramRequest, DiagramSpec, DiagramNode, DiagramConnection,
    DiagramType, OutputFormat, DiagramResult
)
from diagram_ai_generator.src.domain.use_cases.generate_diagram_use_case import GenerateDiagramUseCase
from diagram_ai_generator.src.domain.use_cases.list_providers_use_case import ListProvidersUseCase
from diagram_ai_generator.src.domain.entities.provider import DiagramProvider, ProvidersRegistry


class TestGenerateDiagramUseCase:
    """Tests para el caso de uso de generar diagramas"""
    
    @pytest.fixture
    def mock_ai_provider(self):
        """Mock del proveedor de IA"""
        mock = AsyncMock()
        return mock
    
    @pytest.fixture
    def mock_diagram_repository(self):
        """Mock del repositorio de diagramas"""
        mock = Mock()
        return mock
    
    @pytest.fixture
    def use_case(self, mock_ai_provider, mock_diagram_repository):
        """Instancia del caso de uso con mocks"""
        return GenerateDiagramUseCase(mock_ai_provider, mock_diagram_repository)
    
    @pytest.mark.asyncio
    async def test_successful_diagram_generation(self, use_case, mock_ai_provider, mock_diagram_repository):
        """Test generación exitosa de diagrama"""
        # Arrange
        request = DiagramRequest(
            prompt="test architecture",
            diagram_type=DiagramType.AWS,
            output_format=OutputFormat.PNG
        )
        
        spec = DiagramSpec(
            title="Test",
            description="Test",
            nodes=[DiagramNode("WebServer", "EC2", "aws", "compute")],
            connections=[],
            diagram_type=DiagramType.AWS
        )
        
        expected_result = DiagramResult(
            success=True,
            file_path="test.png"
        )
        
        # Configure mocks
        mock_ai_provider.generate_diagram_spec.return_value = spec
        mock_diagram_repository.validate_spec.return_value = (True, [])
        mock_diagram_repository.generate_diagram.return_value = expected_result
        
        # Act
        result = await use_case.execute(request)
        
        # Assert
        assert result.success is True
        assert result.file_path == "test.png"
        assert result.spec == spec
        assert result.generation_time is not None
        
        # Verify calls
        mock_ai_provider.generate_diagram_spec.assert_called_once_with(request)
        mock_diagram_repository.validate_spec.assert_called_once_with(spec)
        mock_diagram_repository.generate_diagram.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_validation_error(self, use_case, mock_ai_provider, mock_diagram_repository):
        """Test error de validación"""
        # Arrange
        request = DiagramRequest(prompt="test")
        spec = DiagramSpec(
            title="Test",
            description="Test", 
            nodes=[],
            connections=[],
            diagram_type=DiagramType.AWS
        )
        
        # Configure mocks
        mock_ai_provider.generate_diagram_spec.return_value = spec
        mock_diagram_repository.validate_spec.return_value = (False, ["No nodes found"])
        
        # Act
        result = await use_case.execute(request)
        
        # Assert
        assert result.success is False
        assert "Especificación inválida" in result.error_message
        assert "No nodes found" in result.error_message
    
    @pytest.mark.asyncio
    async def test_ai_provider_exception(self, use_case, mock_ai_provider, mock_diagram_repository):
        """Test excepción del proveedor de IA"""
        # Arrange
        request = DiagramRequest(prompt="test")
        mock_ai_provider.generate_diagram_spec.side_effect = Exception("AI Error")
        
        # Act
        result = await use_case.execute(request)
        
        # Assert
        assert result.success is False
        assert "Error durante la generación" in result.error_message
        assert "AI Error" in result.error_message


class TestListProvidersUseCase:
    """Tests para el caso de uso de listar proveedores"""
    
    @pytest.fixture
    def mock_diagram_repository(self):
        """Mock del repositorio con datos de prueba"""
        mock = Mock()
        
        # Crear datos de prueba
        provider = DiagramProvider(
            name="aws",
            display_name="AWS",
            description="Amazon Web Services",
            categories=["compute", "network"],
            total_nodes=100
        )
        
        registry = ProvidersRegistry(
            providers={"aws": provider},
            categories={},
            nodes={}
        )
        
        mock.get_providers_registry.return_value = registry
        return mock
    
    @pytest.fixture
    def use_case(self, mock_diagram_repository):
        """Instancia del caso de uso"""
        return ListProvidersUseCase(mock_diagram_repository)
    
    def test_get_all_providers(self, use_case):
        """Test obtener todos los proveedores"""
        providers = use_case.get_all_providers()
        
        assert len(providers) == 1
        assert providers[0].name == "aws"
        assert providers[0].display_name == "AWS"
        assert providers[0].total_nodes == 100
    
    def test_get_provider_summary(self, use_case):
        """Test obtener resumen de proveedores"""
        summary = use_case.get_provider_summary()
        
        assert summary["total_providers"] == 1
        assert summary["total_nodes"] == 100
        assert "aws" in summary["providers"]
        assert summary["providers"]["aws"]["display_name"] == "AWS"