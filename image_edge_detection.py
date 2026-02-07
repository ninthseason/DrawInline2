"""
Image Edge Detection Library
Provides functions to apply Canny edge detection to PIL Images
Written by Claude AI.
"""

import cv2
import numpy as np
from PIL import Image
from typing import Optional, Tuple


def canny_edge_detect(
    pil_image: Image.Image,
    low_threshold: int = 50,
    high_threshold: int = 150,
    blur_kernel: Tuple[int, int] = (5, 5),
    blur_sigma: float = 1.4,
    return_pil: bool = True
) -> Image.Image | cv2.typing.MatLike:
    """
    Apply Canny edge detection to a PIL Image.
    
    Parameters:
    -----------
    pil_image : PIL.Image.Image
        Input image from PIL/ImageGrab
    low_threshold : int, optional (default=50)
        Lower threshold for edge detection. Pixels with gradient below this are not edges.
    high_threshold : int, optional (default=150)
        Upper threshold for edge detection. Pixels with gradient above this are strong edges.
    blur_kernel : tuple of int, optional (default=(5, 5))
        Kernel size for Gaussian blur. Must be odd numbers.
    blur_sigma : float, optional (default=1.4)
        Standard deviation for Gaussian blur.
    return_pil : bool, optional (default=True)
        If True, returns PIL Image. If False, returns numpy array.
    
    Returns:
    --------
    PIL.Image.Image or numpy.ndarray
        Edge-detected image (binary: white edges on black background)
    
    Examples:
    ---------
    >>> from PIL import ImageGrab
    >>> import image_edge_detection as ied
    >>> 
    >>> # Get image from clipboard
    >>> img = ImageGrab.grabclipboard()
    >>> 
    >>> # Apply edge detection with default settings
    >>> edges = ied.canny_edge_detect(img)
    >>> edges.show()
    >>> 
    >>> # More sensitive detection
    >>> edges_sensitive = ied.canny_edge_detect(img, low_threshold=30, high_threshold=100)
    >>> 
    >>> # Stricter detection
    >>> edges_strict = ied.canny_edge_detect(img, low_threshold=100, high_threshold=200)
    """
    # Convert PIL Image to numpy array
    img_array = np.array(pil_image)
    
    # Handle different image formats
    if len(img_array.shape) == 2:
        # Already grayscale
        gray = img_array
    elif len(img_array.shape) == 3:
        if img_array.shape[2] == 4:
            # RGBA -> Convert to RGB first, then grayscale
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        # RGB to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        raise ValueError(f"Unexpected image shape: {img_array.shape}")
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, blur_kernel, blur_sigma)
    
    # Apply Canny edge detection
    edges = cv2.Canny(blurred, low_threshold, high_threshold)
    
    # Return as PIL Image or numpy array
    if return_pil:
        return Image.fromarray(edges)
    else:
        return edges


def canny_edge_detect_multi(
    pil_image: Image.Image,
    presets: str = 'default'
) -> dict:
    """
    Apply Canny edge detection with multiple threshold presets.
    
    Parameters:
    -----------
    pil_image : PIL.Image.Image
        Input image from PIL/ImageGrab
    presets : str, optional (default='default')
        Preset configuration: 'default', 'all', or 'comparison'
        - 'default': Returns single result with balanced thresholds
        - 'all': Returns sensitive, medium, and strict versions
        - 'comparison': Same as 'all' but also includes original grayscale
    
    Returns:
    --------
    dict
        Dictionary with preset names as keys and PIL Images as values
    
    Examples:
    ---------
    >>> from PIL import ImageGrab
    >>> import image_edge_detection as ied
    >>> 
    >>> img = ImageGrab.grabclipboard()
    >>> results = ied.canny_edge_detect_multi(img, presets='all')
    >>> results['sensitive'].show()
    >>> results['medium'].show()
    >>> results['strict'].show()
    """
    results = {}
    
    if presets == 'default':
        results['edges'] = canny_edge_detect(pil_image, 50, 150)
    
    elif presets in ['all', 'comparison']:
        results['sensitive'] = canny_edge_detect(pil_image, 30, 100)
        results['medium'] = canny_edge_detect(pil_image, 50, 150)
        results['strict'] = canny_edge_detect(pil_image, 100, 200)
        
        if presets == 'comparison':
            # Convert to grayscale
            img_array = np.array(pil_image)
            if len(img_array.shape) == 3:
                if img_array.shape[2] == 4:
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            results['grayscale'] = Image.fromarray(gray)
    
    else:
        raise ValueError(f"Unknown preset: {presets}. Use 'default', 'all', or 'comparison'")
    
    return results


# Convenience function aliases
def edges(pil_image: Image.Image, **kwargs) -> Image.Image | cv2.typing.MatLike:
    """Shorthand for canny_edge_detect with default parameters."""
    return canny_edge_detect(pil_image, **kwargs)


if __name__ == "__main__":
    # Example usage
    print("Image Edge Detection Library")
    print("=" * 50)
    print("\nExample usage:")
    print("""
from PIL import ImageGrab
import image_edge_detection as ied

# Get image from clipboard
img = ImageGrab.grabclipboard()

# Simple usage
edges = ied.canny_edge_detect(img)
edges.save('edges.png')

# Custom thresholds
edges_custom = ied.canny_edge_detect(img, low_threshold=30, high_threshold=100)

# Multiple versions at once
results = ied.canny_edge_detect_multi(img, presets='all')
results['sensitive'].save('edges_sensitive.png')
results['medium'].save('edges_medium.png')
results['strict'].save('edges_strict.png')

# Shorthand
edges = ied.edges(img)
    """)