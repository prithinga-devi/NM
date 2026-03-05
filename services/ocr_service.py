"""
OCR Service for extracting mathematical equations from images.
Uses EasyOCR for reliable text extraction from equation images.
"""

import easyocr
import numpy as np
import re
from typing import Tuple, Optional
from utils.logger import logger, log_error, log_ocr_result


class OCRService:
    """Service for optical character recognition using EasyOCR."""
    
    def __init__(self, languages: list = None):
        """
        Initialize OCR service.
        
        Args:
            languages: List of language codes (default: ['en'])
        """
        self.languages = languages or ['en']
        try:
            self.reader = easyocr.Reader(self.languages, gpu=False)
            logger.info(f"OCR Service initialized with languages: {self.languages}")
        except Exception as e:
            log_error("OCR Initialization", str(e))
            self.reader = None
    
    def extract_text(self, image: np.ndarray) -> Tuple[str, float, bool]:
        """
        Extract text from image using EasyOCR.
        
        Args:
            image: Input image array
            
        Returns:
            Tuple of (extracted_text, confidence, success_flag)
        """
        try:
            if self.reader is None:
                log_error("OCR Extraction", "OCR reader not initialized")
                return "", 0.0, False
            
            if image is None or image.size == 0:
                log_error("OCR Extraction", "Invalid image provided")
                return "", 0.0, False
            
            results = self.reader.readtext(image)
            
            if not results:
                logger.warning("No text detected in image")
                return "", 0.0, False
            
            # Extract text and calculate average confidence
            texts = [text[1] for text in results]
            confidences = [float(text[2]) for text in results]
            
            # Sort by confidence and join
            text_with_conf = [(text, conf) for text, conf in zip(texts, confidences)]
            text_with_conf.sort(key=lambda x: x[1], reverse=True)
            
            extracted_text = ' '.join([t[0] for t in text_with_conf])
            avg_confidence = np.mean(confidences)
            
            log_ocr_result(extracted_text, avg_confidence)
            return extracted_text, avg_confidence, True
            
        except Exception as e:
            log_error("OCR Extraction", str(e))
            return "", 0.0, False
    
    @staticmethod
    def clean_ocr_output(text: str) -> str:
        """
        Clean and standardize OCR output.
        
        Args:
            text: Raw OCR output
            
        Returns:
            Cleaned text
        """
        try:
            # Remove extra whitespace
            text = ' '.join(text.split())
            
            # Replace common OCR mistakes in equations
            replacements = {
                'O': '0',  # Letter O might be confused with zero in some contexts
                'I': '1',  # Letter I might be confused with one
                '|': '1',  # Pipe might be one
                'l': '1',  # Lowercase L might be one
                ' ': '',   # Remove spaces for equation parsing
            }
            
            # More careful replacements - only for clear cases
            text = text.replace('÷', '/')
            text = text.replace('×', '*')
            text = text.replace('−', '-')
            text = text.replace('–', '-')
            text = text.replace('·', '*')
            
            # Handle common math symbols
            text = text.replace('²', '**2')
            text = text.replace('³', '**3')
            text = text.replace('√', 'sqrt')
            
            # Remove unwanted characters but keep parentheses, brackets
            text = re.sub(r'[^\w\s\+\-\*\/\=\(\)\[\]\{\}\.^]', '', text)
            
            logger.info(f"Cleaned OCR output: {text}")
            return text
            
        except Exception as e:
            log_error("OCR Cleaning", str(e))
            return text
    
    def process_image(self, image: np.ndarray) -> Tuple[str, float, bool]:
        """
        Complete OCR pipeline: extract and clean text.
        
        Args:
            image: Input image array
            
        Returns:
            Tuple of (cleaned_text, confidence, success_flag)
        """
        text, confidence, success = self.extract_text(image)
        
        if success and text:
            text = self.clean_ocr_output(text)
            return text, confidence, True
        
        return text, confidence, success
