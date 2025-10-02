"""Node class loader for dynamic imports"""
import importlib
from typing import Any, Optional
from diagrams.generic import Generic


class NodeClassLoader:
    """Loads diagram node classes dynamically"""
    
    def __init__(self):
        """Initialize with cache"""
        self._cache = {}
    
    def load_node_class(self, provider: str, category: str, node_type: str) -> Optional[Any]:
        """
        Load a node class dynamically
        
        Args:
            provider: Cloud provider
            category: Node category
            node_type: Specific node type
        
        Returns:
            Node class if found, None otherwise
        """
        cache_key = f"{provider}_{category}_{node_type}"
        
        # Check cache first
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        try:
            # Import module dynamically
            module_name = f"diagrams.{provider}.{category}"
            module = importlib.import_module(module_name)
            
            # Get class from module
            if hasattr(module, node_type):
                node_class = getattr(module, node_type)
                self._cache[cache_key] = node_class
                return node_class
            
        except (ImportError, AttributeError) as e:
            # Node class not found
            pass
        
        return None
    
    def clear_cache(self):
        """Clear the class cache"""
        self._cache.clear()

