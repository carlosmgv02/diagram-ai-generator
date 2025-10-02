"""
Filesystem adapter for diagram storage.
Implements the DiagramStoragePort interface using the local filesystem.
"""
import os
from pathlib import Path
from typing import Optional

from src.domain.ports.diagram_storage_port import DiagramStoragePort


class FilesystemDiagramStorage(DiagramStoragePort):
    """Stores diagrams in the local filesystem"""
    
    def __init__(self, custom_path: Optional[str] = None):
        """
        Initialize the filesystem storage adapter
        
        Args:
            custom_path: Optional custom path for storing diagrams.
                        If None, uses environment variable or default.
        """
        if custom_path:
            self._output_dir = Path(custom_path)
        else:
            # Check environment variable
            env_path = os.getenv('DIAGRAM_OUTPUT_DIR')
            if env_path:
                self._output_dir = Path(env_path)
            else:
                # Default to generated_diagrams in current directory
                self._output_dir = Path.cwd() / "generated_diagrams"
        
        self.ensure_directory_exists()
    
    def get_output_directory(self) -> Path:
        """Get the configured output directory"""
        return self._output_dir
    
    def ensure_directory_exists(self) -> None:
        """Create the output directory if it doesn't exist"""
        self._output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_diagram_path(self, filename: str) -> Path:
        """Get the full path for a diagram file"""
        return self._output_dir / filename

