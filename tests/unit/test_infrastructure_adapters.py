"""Tests for infrastructure adapters"""
import pytest
from pathlib import Path
import tempfile
import json

from src.infrastructure.adapters.provider_repository import ProviderRepository
from src.infrastructure.adapters.node_class_loader import NodeClassLoader
from src.infrastructure.adapters.image_optimizer import ImageOptimizer
from src.infrastructure.adapters.filesystem_storage import FilesystemDiagramStorage


class TestProviderRepository:
    """Tests for ProviderRepository"""
    
    @pytest.fixture
    def temp_json(self):
        """Create temporary JSON file with provider data"""
        data = {
            "aws": {
                "compute": ["EC2", "Lambda", "ECS"],
                "database": ["RDS", "DynamoDB", "Aurora"]
            },
            "azure": {
                "compute": ["VM", "Functions"],
                "database": ["SQLDatabases", "CosmosDB"]
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(data, f)
            return Path(f.name)
    
    def test_get_all_providers(self, temp_json):
        """Test getting all providers"""
        repo = ProviderRepository(temp_json)
        providers = repo.get_all_providers()
        
        assert "aws" in providers
        assert "azure" in providers
        assert len(providers) == 2
    
    def test_get_provider_categories(self, temp_json):
        """Test getting provider categories"""
        repo = ProviderRepository(temp_json)
        categories = repo.get_provider_categories("aws")
        
        assert "compute" in categories
        assert "database" in categories
    
    def test_get_category_nodes(self, temp_json):
        """Test getting category nodes"""
        repo = ProviderRepository(temp_json)
        nodes = repo.get_category_nodes("aws", "compute")
        
        assert "EC2" in nodes
        assert "Lambda" in nodes
        assert len(nodes) == 3
    
    def test_node_exists(self, temp_json):
        """Test checking if node exists"""
        repo = ProviderRepository(temp_json)
        
        assert repo.node_exists("aws", "compute", "EC2") is True
        assert repo.node_exists("aws", "compute", "NonExistent") is False
        assert repo.node_exists("invalid", "invalid", "invalid") is False
    
    def test_search_nodes(self, temp_json):
        """Test searching for nodes"""
        repo = ProviderRepository(temp_json)
        results = repo.search_nodes("ec2")
        
        assert len(results) > 0
        assert results[0]['name'] == "EC2"
        assert results[0]['provider'] == "aws"
    
    def test_search_nodes_with_provider_filter(self, temp_json):
        """Test searching with provider filter"""
        repo = ProviderRepository(temp_json)
        results = repo.search_nodes("database", provider="azure")
        
        assert all(r['provider'] == "azure" for r in results)


class TestNodeClassLoader:
    """Tests for NodeClassLoader"""
    
    def test_load_valid_node_class(self):
        """Test loading a valid node class"""
        loader = NodeClassLoader()
        node_class = loader.load_node_class("aws", "compute", "EC2")
        
        assert node_class is not None
        # Check it's the correct class
        assert node_class.__name__ == "EC2"
        assert hasattr(node_class, '__init__')
    
    def test_load_invalid_node_class(self):
        """Test loading an invalid node class"""
        loader = NodeClassLoader()
        node_class = loader.load_node_class("invalid", "invalid", "Invalid")
        
        assert node_class is None
    
    def test_caching(self):
        """Test that loader caches results"""
        loader = NodeClassLoader()
        
        # Load same class twice
        class1 = loader.load_node_class("aws", "compute", "EC2")
        class2 = loader.load_node_class("aws", "compute", "EC2")
        
        # Should be same object (cached)
        assert class1 is class2
    
    def test_clear_cache(self):
        """Test clearing the cache"""
        loader = NodeClassLoader()
        
        loader.load_node_class("aws", "compute", "EC2")
        assert len(loader._cache) > 0
        
        loader.clear_cache()
        assert len(loader._cache) == 0


class TestImageOptimizer:
    """Tests for ImageOptimizer"""
    
    def test_get_image_size_mb(self):
        """Test calculating image size"""
        optimizer = ImageOptimizer()
        
        # Base64 string of ~100KB (should be > 0.01 MB)
        test_data = "A" * 100000
        size_mb = optimizer.get_image_size_mb(test_data)
        
        assert isinstance(size_mb, float)
        assert size_mb > 0.01  # Should be at least 0.01 MB
    
    def test_custom_dimensions(self):
        """Test custom max dimensions"""
        optimizer = ImageOptimizer(max_width=500, max_height=400)
        
        assert optimizer.max_width == 500
        assert optimizer.max_height == 400


class TestFilesystemDiagramStorage:
    """Tests for FilesystemDiagramStorage"""
    
    def test_custom_path(self):
        """Test using custom output path"""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = FilesystemDiagramStorage(custom_path=tmpdir)
            
            assert str(storage.get_output_directory()) == tmpdir
            assert storage.get_output_directory().exists()
    
    def test_default_path(self):
        """Test default output path"""
        storage = FilesystemDiagramStorage()
        output_dir = storage.get_output_directory()
        
        assert output_dir.exists()
        assert output_dir.name == "generated_diagrams"
    
    def test_get_diagram_path(self):
        """Test getting diagram path"""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = FilesystemDiagramStorage(custom_path=tmpdir)
            diagram_path = storage.get_diagram_path("test.png")
            
            assert diagram_path.name == "test.png"
            assert str(diagram_path.parent) == tmpdir

