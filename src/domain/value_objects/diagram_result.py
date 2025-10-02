"""Diagram generation result value object"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DiagramResult:
    """Result of diagram generation"""
    success: bool
    title: Optional[str] = None
    file_path: Optional[str] = None
    image_base64: Optional[str] = None
    image_size_mb: Optional[float] = None
    components_count: Optional[int] = None
    connections_count: Optional[int] = None
    provider: Optional[str] = None
    error: Optional[str] = None
    
    @classmethod
    def success_result(
        cls,
        title: str,
        file_path: str,
        image_base64: str,
        image_size_mb: float,
        components_count: int,
        connections_count: int,
        provider: str
    ) -> 'DiagramResult':
        """Create a successful result"""
        return cls(
            success=True,
            title=title,
            file_path=file_path,
            image_base64=image_base64,
            image_size_mb=image_size_mb,
            components_count=components_count,
            connections_count=connections_count,
            provider=provider.upper()
        )
    
    @classmethod
    def failure_result(cls, error: str) -> 'DiagramResult':
        """Create a failure result"""
        return cls(success=False, error=error)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'success': self.success,
            'title': self.title,
            'file_path': self.file_path,
            'image_base64': self.image_base64,
            'image_size_mb': self.image_size_mb,
            'components_count': self.components_count,
            'connections_count': self.connections_count,
            'provider': self.provider,
            'error': self.error
        }

