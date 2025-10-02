"""Tests for NodeResolver domain service"""
import pytest
from unittest.mock import Mock

from src.domain.services.node_resolver import NodeResolver
from diagrams.generic import Generic


class TestNodeResolver:
    """Tests for NodeResolver service"""
    
    @pytest.fixture
    def mock_loader(self):
        """Create mock node loader"""
        return Mock()
    
    @pytest.fixture
    def mock_repository(self):
        """Create mock provider repository"""
        repo = Mock()
        repo.node_exists.return_value = False
        repo.get_category_nodes.return_value = []
        return repo
    
    def test_resolve_exact_match(self, mock_loader, mock_repository):
        """Test resolving with exact match"""
        from diagrams.aws.compute import EC2
        
        mock_repository.node_exists.return_value = True
        mock_loader.load_node_class.return_value = EC2
        
        resolver = NodeResolver(mock_loader, mock_repository)
        result = resolver.resolve_node("aws", "compute", "EC2")
        
        assert result == EC2
        mock_loader.load_node_class.assert_called_once_with("aws", "compute", "EC2")
    
    def test_resolve_with_suggestion(self, mock_loader, mock_repository):
        """Test resolving with suggestion fallback"""
        from diagrams.aws.compute import Lambda
        
        mock_repository.node_exists.return_value = False
        mock_repository.get_category_nodes.return_value = ["Lambda", "EC2"]
        mock_loader.load_node_class.return_value = Lambda
        
        resolver = NodeResolver(mock_loader, mock_repository)
        result = resolver.resolve_node("aws", "compute", "lamb")  # Typo
        
        assert result == Lambda
    
    def test_resolve_fallback_to_generic(self, mock_loader, mock_repository):
        """Test fallback to Generic when nothing found"""
        mock_repository.node_exists.return_value = False
        mock_repository.get_category_nodes.return_value = []
        mock_loader.load_node_class.return_value = None
        
        resolver = NodeResolver(mock_loader, mock_repository)
        result = resolver.resolve_node("invalid", "invalid", "invalid")
        
        assert result == Generic
    
    def test_find_suggestions_exact_match(self, mock_loader, mock_repository):
        """Test finding suggestions with exact match"""
        mock_repository.get_category_nodes.return_value = ["EC2", "ECS", "Lambda"]
        
        resolver = NodeResolver(mock_loader, mock_repository)
        suggestions = resolver._find_suggestions("aws", "compute", "ec2")
        
        assert "EC2" in suggestions
        assert suggestions[0] == "EC2"  # Exact match should be first
    
    def test_find_suggestions_partial_match(self, mock_loader, mock_repository):
        """Test finding suggestions with partial match"""
        mock_repository.get_category_nodes.return_value = ["RDSInstance", "RDSCluster", "Aurora"]
        
        resolver = NodeResolver(mock_loader, mock_repository)
        suggestions = resolver._find_suggestions("aws", "database", "rds")
        
        assert len(suggestions) > 0
        assert any("RDS" in s for s in suggestions)
    
    def test_find_suggestions_prefix_match(self, mock_loader, mock_repository):
        """Test finding suggestions with prefix match"""
        mock_repository.get_category_nodes.return_value = ["Lambda", "LambdaFunction"]
        
        resolver = NodeResolver(mock_loader, mock_repository)
        suggestions = resolver._find_suggestions("aws", "compute", "lam")
        
        assert len(suggestions) > 0
        assert any(s.startswith("Lam") for s in suggestions)

