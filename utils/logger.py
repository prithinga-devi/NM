"""
Logging utility for AI Math Tutor application.
Provides simple logging for tracking OCR results and solver outputs.
"""

import logging
from datetime import datetime
from pathlib import Path


def setup_logger(name: str, log_file: str = "math_tutor.log") -> logging.Logger:
    """
    Set up and configure a logger for the application.
    
    Args:
        name: Logger name (typically __name__)
        log_file: Path to log file
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler
    log_path = Path(log_file)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


# Create a shared logger instance
logger = setup_logger(__name__)


def log_ocr_result(equation: str, confidence: float) -> None:
    """Log OCR results."""
    logger.info(f"OCR Result - Equation: {equation}, Confidence: {confidence:.2f}")


def log_solver_result(equation: str, solution: str) -> None:
    """Log solver results."""
    logger.info(f"Solver Result - Equation: {equation}, Solution: {solution}")


def log_error(error_type: str, error_message: str) -> None:
    """Log errors."""
    logger.error(f"{error_type}: {error_message}")
