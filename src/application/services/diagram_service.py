"""
Refactored diagram service following hexagonal architecture
"""
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.domain.value_objects.diagram_specification import DiagramSpecification
from src.domain.value_objects.diagram_result import DiagramResult
from src.domain.services.node_resolver import NodeResolver
from src.domain.ports.diagram_storage_port import DiagramStoragePort
from src.domain.ports.provider_repository_port import ProviderRepositoryPort
from src.infrastructure.adapters.filesystem_storage import FilesystemDiagramStorage
from src.infrastructure.adapters.provider_repository import ProviderRepository
from src.infrastructure.adapters.node_class_loader import NodeClassLoader
from src.infrastructure.adapters.image_optimizer import ImageOptimizer
from src.infrastructure.adapters.diagram_builder import DiagramBuilder


class DiagramService:
    """
    Application service for diagram generation
    
    Orchestrates the diagram creation process using domain services and infrastructure adapters.
    This service is thin and delegates business logic to domain services.
    """
    
    def __init__(
        self,
        storage: Optional[DiagramStoragePort] = None,
        provider_repository: Optional[ProviderRepositoryPort] = None
    ):
        """
        Initialize diagram service with dependency injection
        
        Args:
            storage: Storage adapter for saving diagrams
            provider_repository: Repository for provider data
        """
        # Infrastructure adapters
        self.storage = storage or FilesystemDiagramStorage()
        self.provider_repository = provider_repository or ProviderRepository()
        self.node_loader = NodeClassLoader()
        self.image_optimizer = ImageOptimizer()
        
        # Domain services
        self.node_resolver = NodeResolver(self.node_loader, self.provider_repository)
        
        # Diagram builder
        self.diagram_builder = DiagramBuilder(
            self.node_resolver,
            self.storage.get_output_directory()
        )
    
    def create_diagram_from_spec(self, spec_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create diagram from specification dictionary
        
        Args:
            spec_dict: Dictionary containing diagram specification
        
        Returns:
            Dictionary with generation result
        """
        try:
            # Parse specification into value object
            spec = DiagramSpecification.from_dict(spec_dict)
            
            # Build diagram
            image_path = self.diagram_builder.build(spec)
            
            # Verify file exists
            if not Path(image_path).exists():
                return DiagramResult.failure_result(
                    f'Failed to generate file: {image_path}'
                ).to_dict()
            
            # Optimize and encode image
            image_data = self.image_optimizer.optimize_and_encode(image_path)
            image_size_mb = self.image_optimizer.get_image_size_mb(image_data)
            
            # Return success result
            return DiagramResult.success_result(
                title=spec.title,
                file_path=image_path,
                image_base64=image_data,
                image_size_mb=image_size_mb,
                components_count=len(spec.components),
                connections_count=len(spec.connections),
                provider=spec.provider
            ).to_dict()
            
        except Exception as e:
            return DiagramResult.failure_result(
                f'Error generating diagram: {str(e)}'
            ).to_dict()
    
    # Query methods (delegated to repository)
    
    def get_available_providers(self) -> List[str]:
        """Get list of available cloud providers"""
        return self.provider_repository.get_all_providers()
    
    def get_provider_categories(self, provider: str) -> List[str]:
        """Get categories for a specific provider"""
        return self.provider_repository.get_provider_categories(provider)
    
    def get_category_nodes(self, provider: str, category: str) -> List[str]:
        """Get available nodes for a provider category"""
        return self.provider_repository.get_category_nodes(provider, category)
    
    def search_nodes(self, query: str, provider: str = None) -> List[Dict[str, str]]:
        """Search for nodes by name"""
        return self.provider_repository.search_nodes(query, provider)

