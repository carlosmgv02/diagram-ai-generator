"""Integration tests for DiagramService"""
import pytest
import tempfile
from pathlib import Path

from src.application.services.diagram_service import DiagramService
from src.infrastructure.adapters.filesystem_storage import FilesystemDiagramStorage
from tests.fixtures.diagram_specs import (
    SIMPLE_AWS_SPEC,
    MULTICLOUD_SPEC,
    CLUSTERED_SPEC
)


class TestDiagramServiceIntegration:
    """Integration tests for complete diagram generation"""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage for tests"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield FilesystemDiagramStorage(custom_path=tmpdir)
    
    @pytest.fixture
    def service(self, temp_storage):
        """Create diagram service with temp storage"""
        return DiagramService(storage=temp_storage)
    
    def test_create_simple_diagram(self, service):
        """Test creating a simple AWS diagram"""
        result = service.create_diagram_from_spec(SIMPLE_AWS_SPEC)
        
        assert result['success'] is True
        assert result['title'] == "Simple AWS Architecture"
        assert result['provider'] == "AWS"
        assert result['components_count'] == 2
        assert result['connections_count'] == 1
        assert Path(result['file_path']).exists()
        assert result['image_base64'] is not None
        assert result['image_size_mb'] > 0
    
    def test_create_multicloud_diagram(self, service):
        """Test creating a multi-cloud diagram"""
        result = service.create_diagram_from_spec(MULTICLOUD_SPEC)
        
        assert result['success'] is True
        assert result['title'] == "Multi-Cloud Architecture"
        assert result['components_count'] == 3
        assert Path(result['file_path']).exists()
    
    def test_create_clustered_diagram(self, service):
        """Test creating a diagram with clusters"""
        result = service.create_diagram_from_spec(CLUSTERED_SPEC)
        
        assert result['success'] is True
        assert result['components_count'] == 5
        assert result['connections_count'] == 5
        assert Path(result['file_path']).exists()
    
    def test_diagram_file_naming(self, service):
        """Test that diagram files are named correctly"""
        result = service.create_diagram_from_spec(SIMPLE_AWS_SPEC)
        
        file_path = Path(result['file_path'])
        assert file_path.suffix == '.png'
        assert "Simple_AWS_Architecture" in file_path.name
        assert file_path.name[-19:-4].replace('_', '').isdigit()  # timestamp
    
    def test_error_handling_invalid_spec(self, service):
        """Test error handling with invalid spec"""
        invalid_spec = {"invalid": "spec"}
        result = service.create_diagram_from_spec(invalid_spec)
        
        # Should handle gracefully
        assert 'success' in result
    
    def test_get_available_providers(self, service):
        """Test getting available providers"""
        providers = service.get_available_providers()
        
        assert isinstance(providers, list)
        assert "aws" in providers
        assert "azure" in providers
        assert "gcp" in providers
    
    def test_get_provider_categories(self, service):
        """Test getting provider categories"""
        categories = service.get_provider_categories("aws")
        
        assert isinstance(categories, list)
        assert "compute" in categories
        assert "database" in categories
        assert "storage" in categories
    
    def test_get_category_nodes(self, service):
        """Test getting category nodes"""
        nodes = service.get_category_nodes("aws", "compute")
        
        assert isinstance(nodes, list)
        assert "EC2" in nodes
        assert "Lambda" in nodes
    
    def test_search_nodes(self, service):
        """Test searching for nodes"""
        results = service.search_nodes("ec2")
        
        assert isinstance(results, list)
        assert len(results) > 0
        assert any(r['name'] == "EC2" for r in results)
    
    def test_search_nodes_with_provider(self, service):
        """Test searching nodes with provider filter"""
        results = service.search_nodes("database", provider="aws")
        
        assert all(r['provider'] == "aws" for r in results)
    
    def test_horizontal_layout(self, service):
        """Test horizontal layout diagram"""
        spec = SIMPLE_AWS_SPEC.copy()
        spec['layout'] = 'horizontal'
        
        result = service.create_diagram_from_spec(spec)
        assert result['success'] is True
    
    def test_vertical_layout(self, service):
        """Test vertical layout diagram"""
        spec = SIMPLE_AWS_SPEC.copy()
        spec['layout'] = 'vertical'
        
        result = service.create_diagram_from_spec(spec)
        assert result['success'] is True
    
    def test_connection_styling(self, service):
        """Test connections with various styles"""
        spec = {
            "title": "Styled Connections",
            "provider": "aws",
            "components": [
                {"id": "a", "type": "EC2", "category": "compute"},
                {"id": "b", "type": "RDS", "category": "database"}
            ],
            "connections": [
                {
                    "from": "a",
                    "to": "b",
                    "label": "queries",
                    "color": "blue",
                    "style": "dashed"
                }
            ],
            "clusters": []
        }
        
        result = service.create_diagram_from_spec(spec)
        assert result['success'] is True
    
    def test_empty_diagram(self, service):
        """Test creating diagram with no components"""
        spec = {
            "title": "Empty Diagram",
            "provider": "aws",
            "components": [],
            "connections": [],
            "clusters": []
        }
        
        result = service.create_diagram_from_spec(spec)
        assert result['success'] is True
        assert result['components_count'] == 0
    
    def test_diagram_with_generic_nodes(self, service):
        """Test diagram with fallback to generic nodes"""
        spec = {
            "title": "Generic Nodes Test",
            "provider": "aws",
            "components": [
                {
                    "id": "unknown",
                    "type": "NonExistentNode",
                    "category": "invalid_category"
                }
            ],
            "connections": [],
            "clusters": []
        }
        
        result = service.create_diagram_from_spec(spec)
        # Should succeed with generic fallback
        assert result['success'] is True

