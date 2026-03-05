"""
Image preprocessing utilities for equation image enhancement.
Uses OpenCV for image enhancement before OCR.
"""

import cv2
import numpy as np
from typing import Optional, Tuple
from utils.logger import logger, log_error


def resize_image(image: np.ndarray, max_width: int = 1200, max_height: int = 800) -> np.ndarray:
    """
    Resize image while maintaining aspect ratio.
    
    Args:
        image: Input image array
        max_width: Maximum width
        max_height: Maximum height
        
    Returns:
        Resized image
    """
    height, width = image.shape[:2]
    
    if width <= max_width and height <= max_height:
        return image
    
    scale = min(max_width / width, max_height / height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert image to grayscale.
    
    Args:
        image: Input image array
        
    Returns:
        Grayscale image
    """
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def adjust_contrast(image: np.ndarray, alpha: float = 1.5, beta: float = 30) -> np.ndarray:
    """
    Adjust image contrast using formula: new_image = alpha * image + beta.
    
    Args:
        image: Input grayscale image
        alpha: Contrast control (1.0 = original)
        beta: Brightness control (0 = no change)
        
    Returns:
        Contrast-adjusted image
    """
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return np.clip(adjusted, 0, 255).astype(np.uint8)


def reduce_noise(image: np.ndarray) -> np.ndarray:
    """
    Reduce image noise using bilateral filtering.
    
    Args:
        image: Input image
        
    Returns:
        Denoised image
    """
    return cv2.bilateralFilter(image, 9, 75, 75)


def apply_adaptive_threshold(image: np.ndarray) -> np.ndarray:
    """
    Apply adaptive thresholding to create binary image.
    Better for varying lighting conditions.
    
    Args:
        image: Input grayscale image
        
    Returns:
        Binary image
    """
    return cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )


def preprocess_image(image: np.ndarray) -> Tuple[np.ndarray, bool]:
    """
    Complete preprocessing pipeline for equation image.
    
    Args:
        image: Input image array (BGR or grayscale)
        
    Returns:
        Tuple of (preprocessed_image, success_flag)
    """
    try:
        if image is None or image.size == 0:
            log_error("Preprocessing", "Empty or invalid image")
            return None, False
        
        # Resize
        image = resize_image(image)
        
        # Convert to grayscale
        image = convert_to_grayscale(image)
        
        # Reduce noise
        image = reduce_noise(image)
        
        # Adjust contrast
        image = adjust_contrast(image, alpha=1.5, beta=30)
        
        # Apply adaptive threshold
        image = apply_adaptive_threshold(image)
        
        logger.info("Image preprocessing completed successfully")
        return image, True
        
    except Exception as e:
        log_error("Image Preprocessing", str(e))
        return None, False


def get_image_stats(image: np.ndarray) -> dict:
    """
    Get statistics about the image for quality assessment.
    
    Args:
        image: Input image array
        
    Returns:
        Dictionary with image statistics
    """
    try:
        return {
            "height": image.shape[0],
            "width": image.shape[1],
            "mean_intensity": float(np.mean(image)),
            "std_intensity": float(np.std(image)),
            "min_intensity": int(np.min(image)),
            "max_intensity": int(np.max(image))
        }
    except Exception as e:
        log_error("Image Stats", str(e))
        return {}
