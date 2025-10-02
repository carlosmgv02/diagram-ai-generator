"""
Port (interface) for diagram storage.
This allows us to swap storage implementations (filesystem, S3, database, etc.)
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class DiagramStoragePort(ABC):
    """Interface for storing generated diagrams"""
    
    @abstractmethod
    def get_output_directory(self) -> Path:
        """
        Get the directory where diagrams should be saved
        
        Returns:
            Path: The output directory path
        """
        pass
    
    @abstractmethod
    def ensure_directory_exists(self) -> None:
        """Ensure the output directory exists, creating it if necessary"""
        pass
    
    @abstractmethod
    def get_diagram_path(self, filename: str) -> Path:
        """
        Get the full path for a diagram file
        
        Args:
            filename: The name of the diagram file
            
        Returns:
            Path: The full path to the diagram file
        """
        pass

