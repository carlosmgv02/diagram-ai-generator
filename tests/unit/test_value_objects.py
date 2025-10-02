"""Tests for domain value objects"""
import pytest

from src.domain.value_objects.diagram_specification import (
    DiagramSpecification,
    Component,
    Connection,
    ComponentCluster
)
from src.domain.value_objects.diagram_result import DiagramResult
from tests.fixtures.diagram_specs import SIMPLE_AWS_SPEC, CLUSTERED_SPEC


class TestComponent:
    """Tests for Component value object"""
    
    def test_component_creation(self):
        """Test creating a component"""
        comp = Component(
            id="web1",
            type="EC2",
            category="compute",
            label="Web Server"
        )
        
        assert comp.id == "web1"
        assert comp.type == "EC2"
        assert comp.category == "compute"
        assert comp.get_label() == "Web Server"
    
    def test_component_default_label(self):
        """Test component uses id as default label"""
        comp = Component(id="web1", type="EC2")
        assert comp.get_label() == "web1"
    
    def test_component_immutable(self):
        """Test that component is immutable"""
        comp = Component(id="web1", type="EC2")
        with pytest.raises(AttributeError):
            comp.id = "web2"


class TestConnection:
    """Tests for Connection value object"""
    
    def test_connection_creation(self):
        """Test creating a connection"""
        conn = Connection(
            from_id="web1",
            to_id="db1",
            label="queries",
            color="blue",
            style="dashed"
        )
        
        assert conn.from_id == "web1"
        assert conn.to_id == "db1"
        assert conn.label == "queries"
        assert conn.color == "blue"
        assert conn.style == "dashed"
    
    def test_connection_minimal(self):
        """Test connection with minimal data"""
        conn = Connection(from_id="a", to_id="b")
        assert conn.from_id == "a"
        assert conn.to_id == "b"
        assert conn.label is None


class TestDiagramSpecification:
    """Tests for DiagramSpecification value object"""
    
    def test_from_dict_simple(self):
        """Test creating specification from dictionary"""
        spec = DiagramSpecification.from_dict(SIMPLE_AWS_SPEC)
        
        assert spec.title == "Simple AWS Architecture"
        assert spec.provider == "aws"
        assert spec.layout == "horizontal"
        assert len(spec.components) == 2
        assert len(spec.connections) == 1
        assert len(spec.clusters) == 0
    
    def test_from_dict_clustered(self):
        """Test creating clustered specification"""
        spec = DiagramSpecification.from_dict(CLUSTERED_SPEC)
        
        assert len(spec.components) == 5
        assert len(spec.clusters) == 2
        assert spec.clusters[0].name == "Web Tier"
        assert len(spec.clusters[0].component_ids) == 2
    
    def test_get_direction(self):
        """Test direction calculation"""
        spec_v = DiagramSpecification(title="Test", layout="vertical")
        spec_h = DiagramSpecification(title="Test", layout="horizontal")
        
        assert spec_v.get_direction() == "TB"
        assert spec_h.get_direction() == "LR"
    
    def test_get_unclustered_components(self):
        """Test getting unclustered components"""
        spec = DiagramSpecification.from_dict(CLUSTERED_SPEC)
        unclustered = spec.get_unclustered_components()
        
        # Only 'lb' should be unclustered
        assert len(unclustered) == 1
        assert unclustered[0].id == "lb"
    
    def test_get_component_by_id(self):
        """Test finding component by ID"""
        spec = DiagramSpecification.from_dict(SIMPLE_AWS_SPEC)
        
        comp = spec.get_component_by_id("web1")
        assert comp is not None
        assert comp.type == "EC2"
        
        missing = spec.get_component_by_id("nonexistent")
        assert missing is None


class TestDiagramResult:
    """Tests for DiagramResult value object"""
    
    def test_success_result(self):
        """Test creating success result"""
        result = DiagramResult.success_result(
            title="Test Diagram",
            file_path="/path/to/diagram.png",
            image_base64="base64data",
            image_size_mb=1.5,
            components_count=3,
            connections_count=2,
            provider="aws"
        )
        
        assert result.success is True
        assert result.title == "Test Diagram"
        assert result.provider == "AWS"
        assert result.error is None
    
    def test_failure_result(self):
        """Test creating failure result"""
        result = DiagramResult.failure_result("Something went wrong")
        
        assert result.success is False
        assert result.error == "Something went wrong"
        assert result.title is None
    
    def test_to_dict(self):
        """Test converting result to dictionary"""
        result = DiagramResult.success_result(
            title="Test",
            file_path="/path/to/file.png",
            image_base64="data",
            image_size_mb=1.0,
            components_count=2,
            connections_count=1,
            provider="aws"
        )
        
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict['success'] is True
        assert result_dict['title'] == "Test"

