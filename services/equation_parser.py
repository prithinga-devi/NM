"""
Equation Parser for converting text equations to SymPy expression.
Validates and parses algebraic equations from OCR output.
"""

import re
from typing import Optional, Tuple
from sympy import symbols, sympify, sympify, Eq, parse_expr
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from utils.logger import logger, log_error


class EquationParser:
    """Parser for converting text equations to SymPy expressions."""
    
    def __init__(self, variable: str = 'x'):
        """
        Initialize equation parser.
        
        Args:
            variable: The variable to solve for (default: 'x')
        """
        self.variable = variable
        self.x = symbols(variable)
        logger.info(f"EquationParser initialized with variable: {variable}")
    
    @staticmethod
    def validate_equation(equation: str) -> Tuple[bool, str]:
        """
        Validate equation syntax.
        
        Args:
            equation: Equation string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check for balanced parentheses
            if equation.count('(') != equation.count(')'):
                return False, "Unbalanced parentheses"
            
            if equation.count('[') != equation.count(']'):
                return False, "Unbalanced brackets"
            
            # Check for equals sign
            if '=' not in equation:
                return False, "Equation must contain '=' sign"
            
            # Check for valid characters
            valid_chars = r'^[a-zA-Z0-9\+\-\*\/\=\(\)\[\]\{\}\.\^,\s]+$'
            if not re.match(valid_chars, equation):
                return False, "Equation contains invalid characters"
            
            # Check that equals sign is not at beginning or end
            parts = equation.split('=')
            if len(parts) != 2:
                return False, "Equation must have exactly one '=' sign"
            
            if not parts[0].strip() or not parts[1].strip():
                return False, "Both sides of equation must have content"
            
            return True, ""
            
        except Exception as e:
            return False, str(e)
    
    def preprocess_equation(self, equation: str) -> str:
        """
        Preprocess equation for parsing.
        
        Args:
            equation: Raw equation string
            
        Returns:
            Preprocessed equation
        """
        try:
            # Remove extra spaces
            equation = ' '.join(equation.split())
            
            # Standardize operators
            equation = equation.replace('**', '^')  # Handle power operator
            
            # Add multiplication between number and variable (2x -> 2*x)
            equation = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation)
            
            # Add multiplication between ) and number or variable ()x -> ()*x
            equation = re.sub(r'(\))(\d)', r'\1*\2', equation)
            equation = re.sub(r'(\))([a-zA-Z])', r'\1*\2', equation)
            
            # Add multiplication between number/variable and (
            equation = re.sub(r'(\d)(\()', r'\1*\2', equation)
            equation = re.sub(r'([a-zA-Z])(\()', r'\1*\2', equation)
            
            return equation
            
        except Exception as e:
            log_error("Equation Preprocessing", str(e))
            return equation
    
    def parse_equation(self, equation_str: str) -> Tuple[Optional[Eq], bool, str]:
        """
        Parse string equation to SymPy Equation object.
        
        Args:
            equation_str: Equation string (e.g., "2x + 5 = 15")
            
        Returns:
            Tuple of (sympy_equation, success_flag, error_message)
        """
        try:
            # Validate
            is_valid, error_msg = self.validate_equation(equation_str)
            if not is_valid:
                return None, False, error_msg
            
            # Preprocess
            equation_str = self.preprocess_equation(equation_str)
            
            # Split into left and right side
            left_str, right_str = equation_str.split('=')
            left_str = left_str.strip()
            right_str = right_str.strip()
            
            # Replace ^ with **
            left_str = left_str.replace('^', '**')
            right_str = right_str.replace('^', '**')
            
            # Parse both sides
            try:
                transformations = (standard_transformations + (implicit_multiplication_application,))
                left_expr = parse_expr(left_str, local_dict={self.variable: self.x}, transformations=transformations)
                right_expr = parse_expr(right_str, local_dict={self.variable: self.x}, transformations=transformations)
            except Exception as parse_err:
                return None, False, f"Failed to parse equation: {str(parse_err)}"
            
            # Create equation
            equation = Eq(left_expr, right_expr)
            
            logger.info(f"Successfully parsed equation: {equation}")
            return equation, True, ""
            
        except Exception as e:
            error_msg = f"Error parsing equation: {str(e)}"
            log_error("Equation Parsing", error_msg)
            return None, False, error_msg
    
    def parse_expression(self, expr_str: str):
        """
        Parse a simple expression (not an equation).
        
        Args:
            expr_str: Expression string (e.g., "2x + 5")
            
        Returns:
            Tuple of (sympy_expression, success_flag, error_message)
        """
        try:
            expr_str = self.preprocess_equation(expr_str)
            expr_str = expr_str.replace('^', '**')
            
            transformations = (standard_transformations + (implicit_multiplication_application,))
            expr = parse_expr(expr_str, local_dict={self.variable: self.x}, transformations=transformations)
            
            logger.info(f"Successfully parsed expression: {expr}")
            return expr, True, ""
            
        except Exception as e:
            error_msg = f"Error parsing expression: {str(e)}"
            log_error("Expression Parsing", error_msg)
            return None, False, error_msg
