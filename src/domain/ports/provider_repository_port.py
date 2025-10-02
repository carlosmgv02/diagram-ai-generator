"""Provider repository port"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ProviderRepositoryPort(ABC):
    """Port for accessing provider data"""
    
    @abstractmethod
    def get_all_providers(self) -> List[str]:
        """Get all available providers"""
        pass
    
    @abstractmethod
    def get_provider_categories(self, provider: str) -> List[str]:
        """Get categories for a provider"""
        pass
    
    @abstractmethod
    def get_category_nodes(self, provider: str, category: str) -> List[str]:
        """Get nodes for a provider category"""
        pass
    
    @abstractmethod
    def node_exists(self, provider: str, category: str, node_type: str) -> bool:
        """Check if a node exists"""
        pass
    
    @abstractmethod
    def search_nodes(self, query: str, provider: str = None) -> List[Dict[str, str]]:
        """Search for nodes by query"""
        pass

