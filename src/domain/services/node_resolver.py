"""Node resolution domain service"""
from typing import Optional, List, Any
from diagrams.generic import Generic


class NodeResolver:
    """Resolves node types to diagram node classes"""
    
    def __init__(self, node_loader: 'NodeClassLoader', providers_repository: 'ProviderRepository'):
        """
        Initialize node resolver
        
        Args:
            node_loader: Adapter for loading node classes dynamically
            providers_repository: Repository for provider data
        """
        self.node_loader = node_loader
        self.providers_repository = providers_repository
    
    def resolve_node(self, provider: str, category: str, node_type: str) -> Any:
        """
        Resolve a node type to its corresponding class
        
        Args:
            provider: Cloud provider (aws, azure, gcp, etc.)
            category: Node category (compute, database, etc.)
            node_type: Specific node type (EC2, RDS, etc.)
        
        Returns:
            Node class, or Generic as fallback
        """
        # Try exact match first
        if self.providers_repository.node_exists(provider, category, node_type):
            node_class = self.node_loader.load_node_class(provider, category, node_type)
            if node_class:
                return node_class
        
        # Try to find suggestions and use best match
        suggestions = self._find_suggestions(provider, category, node_type)
        if suggestions:
            print(f"⚠️  Node not found: '{node_type}' in {provider}/{category}")
            print(f"💡 Suggestions: {', '.join(suggestions[:3])}")
            
            # Try first suggestion
            best_match = suggestions[0]
            node_class = self.node_loader.load_node_class(provider, category, best_match)
            if node_class:
                print(f"✅ Using suggestion: '{best_match}' instead of '{node_type}'")
                return node_class
        
        # Fallback to Generic
        return Generic
    
    def _find_suggestions(self, provider: str, category: str, node_type: str) -> List[str]:
        """Find similar node suggestions"""
        available_nodes = self.providers_repository.get_category_nodes(provider, category)
        if not available_nodes:
            return []
        
        suggestions = []
        node_lower = node_type.lower()
        
        # Exact match (case-insensitive)
        for node in available_nodes:
            if node.lower() == node_lower:
                suggestions.append(node)
        
        # Contains match
        for node in available_nodes:
            if node_lower in node.lower() or node.lower() in node_lower:
                if node not in suggestions:
                    suggestions.append(node)
        
        # Prefix match (first 3 characters)
        for node in available_nodes:
            if (len(node_lower) >= 3 and len(node) >= 3 and 
                node.lower()[:3] == node_lower[:3]):
                if node not in suggestions:
                    suggestions.append(node)
        
        return suggestions[:5]

