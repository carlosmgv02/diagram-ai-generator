"""
Tests para la capa de dominio
"""
import pytest
from datetime import datetime

from diagram_ai_generator.src.domain.entities.diagram import (
    DiagramRequest, DiagramSpec, DiagramNode, DiagramConnection,
    DiagramType, OutputFormat, DiagramResult
)
from diagram_ai_generator.src.domain.entities.provider import (
    DiagramProvider, DiagramCategory, ProvidersRegistry
)


class TestDiagramEntities:
    """Tests para las entidades de diagrama"""
    
    def test_diagram_request_creation(self):
        """Test creación de DiagramRequest"""
        request = DiagramRequest(
            prompt="test architecture",
            diagram_type=DiagramType.AWS,
            output_format=OutputFormat.PNG
        )
        
        assert request.prompt == "test architecture"
        assert request.diagram_type == DiagramType.AWS
        assert request.output_format == OutputFormat.PNG
        assert isinstance(request.created_at, datetime)
    
    def test_diagram_node_creation(self):
        """Test creación de DiagramNode"""
        node = DiagramNode(
            name="WebServer",
            node_type="EC2",
            provider="aws",
            category="compute",
            properties={"instance_type": "t3.micro"}
        )
        
        assert node.name == "WebServer"
        assert node.node_type == "EC2"
        assert node.provider == "aws"
        assert node.category == "compute"
        assert node.properties["instance_type"] == "t3.micro"
    
    def test_diagram_connection_creation(self):
        """Test creación de DiagramConnection"""
        connection = DiagramConnection(
            source="LoadBalancer",
            target="WebServer",
            label="HTTP"
        )
        
        assert connection.source == "LoadBalancer"
        assert connection.target == "WebServer"
        assert connection.label == "HTTP"
    
    def test_diagram_spec_creation(self):
        """Test creación de DiagramSpec"""
        nodes = [
            DiagramNode("WebServer", "EC2", "aws", "compute"),
            DiagramNode("Database", "RDS", "aws", "database")
        ]
        connections = [
            DiagramConnection("WebServer", "Database", "SQL")
        ]
        
        spec = DiagramSpec(
            title="Test Architecture",
            description="A test architecture",
            nodes=nodes,
            connections=connections,
            diagram_type=DiagramType.AWS
        )
        
        assert spec.title == "Test Architecture"
        assert len(spec.nodes) == 2
        assert len(spec.connections) == 1
        assert spec.diagram_type == DiagramType.AWS


class TestProviderEntities:
    """Tests para las entidades de proveedor"""
    
    def test_diagram_provider_creation(self):
        """Test creación de DiagramProvider"""
        provider = DiagramProvider(
            name="aws",
            display_name="Amazon Web Services",
            description="AWS Cloud Provider",
            categories=["compute", "network", "database"],
            total_nodes=500
        )
        
        assert provider.name == "aws"
        assert provider.display_name == "Amazon Web Services"
        assert provider.total_nodes == 500
        assert len(provider.categories) == 3
    
    def test_providers_registry(self):
        """Test ProvidersRegistry functionality"""
        provider = DiagramProvider(
            name="aws",
            display_name="AWS",
            description="AWS",
            categories=["compute"],
            total_nodes=100
        )
        
        category = DiagramCategory(
            name="compute",
            provider="aws",
            nodes=["EC2", "Lambda"]
        )
        
        registry = ProvidersRegistry(
            providers={"aws": provider},
            categories={"aws": [category]},
            nodes={}
        )
        
        # Test get_provider
        found_provider = registry.get_provider("aws")
        assert found_provider is not None
        assert found_provider.name == "aws"
        
        # Test get_provider case insensitive
        found_provider = registry.get_provider("AWS")
        assert found_provider is not None
        
        # Test get_categories_for_provider
        categories = registry.get_categories_for_provider("aws")
        assert len(categories) == 1
        assert categories[0].name == "compute"
        
        # Test get_nodes_for_category
        nodes = registry.get_nodes_for_category("aws", "compute")
        assert nodes == ["EC2", "Lambda"]