"""Provider repository implementation"""
import json
from pathlib import Path
from typing import List, Dict, Any

from src.domain.ports.provider_repository_port import ProviderRepositoryPort


class ProviderRepository(ProviderRepositoryPort):
    """Repository for provider data from JSON file"""
    
    def __init__(self, json_path: Path = None):
        """
        Initialize repository
        
        Args:
            json_path: Path to diagrams_structure.json. If None, uses default location.
        """
        if json_path is None:
            project_root = Path(__file__).parent.parent.parent.parent
            json_path = project_root / "src" / "infrastructure" / "external" / "diagrams_structure.json"
        
        self._data = self._load_data(json_path)
    
    def _load_data(self, json_path: Path) -> Dict[str, Any]:
        """Load provider data from JSON"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading provider data: {e}")
            return {}
    
    def get_all_providers(self) -> List[str]:
        """Get all available providers"""
        return list(self._data.keys())
    
    def get_provider_categories(self, provider: str) -> List[str]:
        """Get categories for a provider"""
        return list(self._data.get(provider, {}).keys())
    
    def get_category_nodes(self, provider: str, category: str) -> List[str]:
        """Get nodes for a provider category"""
        return self._data.get(provider, {}).get(category, [])
    
    def node_exists(self, provider: str, category: str, node_type: str) -> bool:
        """Check if a node exists"""
        return (provider in self._data and 
                category in self._data[provider] and
                node_type in self._data[provider][category])
    
    def search_nodes(self, query: str, provider: str = None) -> List[Dict[str, str]]:
        """Search for nodes by query"""
        results = []
        query_lower = query.lower()
        
        for prov_name, categories in self._data.items():
            if provider and prov_name != provider:
                continue
            
            for cat_name, nodes in categories.items():
                for node_name in nodes:
                    if query_lower in node_name.lower():
                        results.append({
                            'name': node_name,
                            'provider': prov_name,
                            'category': cat_name,
                            'description': f'Node {node_name} from {prov_name.upper()}'
                        })
        
        return results

