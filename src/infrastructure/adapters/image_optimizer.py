"""Image optimization adapter"""
import base64
from pathlib import Path
from PIL import Image
import io


class ImageOptimizer:
    """Optimizes and encodes diagram images"""
    
    def __init__(self, max_width: int = 1000, max_height: int = 800):
        """
        Initialize optimizer
        
        Args:
            max_width: Maximum image width
            max_height: Maximum image height
        """
        self.max_width = max_width
        self.max_height = max_height
    
    def optimize_and_encode(self, image_path: str) -> str:
        """
        Optimize image and return base64 encoding
        
        Args:
            image_path: Path to image file
        
        Returns:
            Base64 encoded image string
        """
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too large
                if img.width > self.max_width or img.height > self.max_height:
                    img.thumbnail((self.max_width, self.max_height), Image.Resampling.LANCZOS)
                
                # Save optimized
                buffer = io.BytesIO()
                img.save(buffer, format='PNG', optimize=True, compress_level=9)
                return base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        except Exception as e:
            # Fallback: read original file
            with open(image_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
    
    def get_image_size_mb(self, base64_data: str) -> float:
        """
        Calculate image size in MB from base64 data
        
        Args:
            base64_data: Base64 encoded image
        
        Returns:
            Size in MB
        """
        # Base64 adds ~33% overhead, so multiply by 3/4 to get original size
        size_bytes = len(base64_data) * 3 / 4
        return round(size_bytes / 1024 / 1024, 2)

