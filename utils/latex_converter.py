"""
LaTeX conversion utilities for displaying equations in Streamlit.
Converts algebraic equations to LaTeX format for mathematical rendering.
"""

import re
from typing import Optional, Tuple
from utils.logger import logger, log_error


def escape_latex(text: str) -> str:
    """
    Escape special LaTeX characters.
    
    Args:
        text: Input text
        
    Returns:
        LaTeX-safe text
    """
    special_chars = {
        '_': r'\_',
        '^': r'\^{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
    }
    
    for char, replacement in special_chars.items():
        text = text.replace(char, replacement)
    
    return text


def standardize_operators(equation: str) -> str:
    """
    Standardize mathematical operators for LaTeX conversion.
    
    Args:
        equation: Input equation string
        
    Returns:
        Standardized equation
    """
    # Replace division symbol
    equation = equation.replace('÷', '/')
    equation = equation.replace('∕', '/')
    
    # Replace multiplication symbol
    equation = equation.replace('×', '*')
    equation = equation.replace('∗', '*')
    equation = equation.replace('·', '*')
    
    # Normalize minus sign
    equation = equation.replace('−', '-')
    equation = equation.replace('–', '-')
    
    # Normalize equals
    equation = equation.replace('=', ' = ')
    
    return equation


def simple_to_latex(equation: str) -> str:
    """
    Convert simple algebraic equation to LaTeX format.
    
    Args:
        equation: Input equation (e.g., "2x + 5 = 15")
        
    Returns:
        LaTeX formatted equation (e.g., "2x + 5 = 15")
    """
    try:
        # Standardize operators first
        equation = standardize_operators(equation)
        
        # Clean up whitespace
        equation = ' '.join(equation.split())
        
        # Replace common patterns
        
        # Handle fractions with / symbol
        equation = re.sub(r'(\d+)\s*/\s*(\d+)', r'\\frac{\1}{\2}', equation)
        
        # Handle exponents (x^2 or x**2 -> x^{2})
        equation = re.sub(r'([a-zA-Z0-9\)])\s*\*\*\s*(\d+)', r'\1^{\2}', equation)
        equation = re.sub(r'([a-zA-Z0-9\)])\s*\^\s*(\d+)', r'\1^{\2}', equation)
        
        # Handle square root
        equation = re.sub(r'sqrt\(([^)]+)\)', r'\\sqrt{\1}', equation, flags=re.IGNORECASE)
        
        # Replace multiplication between (implicit multiplication handling)
        # This is optional - many prefer to show explicit multiplication
        
        logger.info(f"Converted to LaTeX: {equation}")
        return equation
        
    except Exception as e:
        log_error("LaTeX Conversion", str(e))
        return equation


def equation_to_latex(equation: str, is_solution: bool = False) -> str:
    """
    Convert equation to display-ready LaTeX.
    
    Args:
        equation: Input equation string
        is_solution: Whether this is a solution/answer
        
    Returns:
        LaTeX formatted string
    """
    try:
        latex = simple_to_latex(equation)
        
        if is_solution:
            return f"$$x = {latex}$$"
        else:
            return f"$${latex}$$"
            
    except Exception as e:
        log_error("Equation to LaTeX", str(e))
        return f"$${equation}$$"


def format_step(step_description: str, equation: str) -> Tuple[str, str]:
    """
    Format a single step with description and equation.
    
    Args:
        step_description: Description of the step
        equation: Equation after this step
        
    Returns:
        Tuple of (description, latex_equation)
    """
    try:
        latex_eq = simple_to_latex(equation)
        return step_description, f"$${latex_eq}$$"
    except Exception as e:
        log_error("Format Step", str(e))
        return step_description, f"$${equation}$$"
