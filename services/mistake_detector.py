"""
Mistake Detector for identifying common algebra errors.
Detects and highlights common mistakes in equation solving.
"""

import re
from typing import List, Dict, Optional
from sympy import symbols, sympify, simplify
from utils.logger import logger, log_error


class MistakeDetector:
    """Detect common algebra mistakes in equations."""
    
    # Common mistake patterns and their descriptions
    MISTAKE_PATTERNS = {
        "sign_error": {
            "patterns": [
                r"(\d+)\s*\+\s*(\d+)\s*=\s*(-?\d+(?:\s*-\s*\d+)?)",  # Wrong sign in combining
            ],
            "description": "Sign error: Check the signs when combining positive/negative numbers",
            "severity": "high",
            "trap_area": "When moving terms between sides of equation"
        },
        "distribution_error": {
            "patterns": [
                r"(\d+)\s*\(\s*([^)]+)\)",  # Distribution issue
            ],
            "description": "Incorrect distributive property: Remember to multiply each term inside brackets",
            "severity": "high",
            "trap_area": "When expanding brackets using distributive property"
        },
        "division_error": {
            "patterns": [
                r"(\d+)/(\d+)",  # Fraction issues
            ],
            "description": "Check division: Ensure both sides are divided by the same number",
            "severity": "medium",
            "trap_area": "When dividing both sides by a number"
        },
        "variable_loss": {
            "patterns": [
                r"(\d+x)\s*[*/]\s*(\d+)\s*[!=]",  # Variable might be lost
            ],
            "description": "Variable loss: Don't lose variables when performing operations",
            "severity": "high",
            "trap_area": "When dividing terms containing variables"
        },
        "missing_brackets": {
            "patterns": [
                r"(\d+)\s*([+-])\s*(\d+x)\s*([+-])\s*(\d+)",
            ],
            "description": "Missing brackets: Use brackets when needed to group terms",
            "severity": "medium",
            "trap_area": "When expanding or rearranging multiple terms"
        }
    }
    
    @staticmethod
    def check_parentheses_balance(equation: str) -> List[Dict[str, any]]:
        """
        Check for unbalanced parentheses.
        
        Args:
            equation: Equation string
            
        Returns:
            List of detected mistakes
        """
        mistakes = []
        
        try:
            open_count = equation.count('(')
            close_count = equation.count(')')
            
            if open_count != close_count:
                mistakes.append({
                    "type": "parentheses_error",
                    "description": f"Unbalanced parentheses: {open_count} open, {close_count} close",
                    "severity": "critical",
                    "trap_area": "Parentheses matching"
                })
            
            # Check bracket balance
            open_bracket = equation.count('[')
            close_bracket = equation.count(']')
            
            if open_bracket != close_bracket:
                mistakes.append({
                    "type": "bracket_error",
                    "description": f"Unbalanced brackets: {open_bracket} open, {close_bracket} close",
                    "severity": "critical",
                    "trap_area": "Bracket matching"
                })
        
        except Exception as e:
            log_error("Parentheses Check", str(e))
        
        return mistakes
    
    @staticmethod
    def check_operator_consistency(equation: str) -> List[Dict[str, any]]:
        """
        Check for consistent operator usage.
        
        Args:
            equation: Equation string
            
        Returns:
            List of detected mistakes
        """
        mistakes = []
        
        try:
            # Check for multiple equals signs
            equals_count = equation.count('=')
            if equals_count != 1:
                mistakes.append({
                    "type": "multiple_equals",
                    "description": f"Equation should have exactly one '=' sign, found {equals_count}",
                    "severity": "critical",
                    "trap_area": "Equation structure"
                })
            
            # Check for consecutive operators
            if re.search(r'[+\-*/]{2,}', equation):
                mistakes.append({
                    "type": "consecutive_operators",
                    "description": "Consecutive operators detected. Check operator spacing",
                    "severity": "medium",
                    "trap_area": "Operator placement"
                })
        
        except Exception as e:
            log_error("Operator Consistency", str(e))
        
        return mistakes
    
    @staticmethod
    def check_arithmetic_validity(left_side: str, right_side: str) -> List[Dict[str, any]]:
        """
        Check for obvious arithmetic errors.
        
        Args:
            left_side: Left side of equation
            right_side: Right side of equation
            
        Returns:
            List of detected mistakes
        """
        mistakes = []
        
        try:
            # Check for division by zero patterns
            if re.search(r'/\s*0', left_side) or re.search(r'/\s*0', right_side):
                mistakes.append({
                    "type": "division_by_zero",
                    "description": "Division by zero detected! This is undefined.",
                    "severity": "critical",
                    "trap_area": "Division operations"
                })
            
            # Check for 0*variable patterns
            if re.search(r'0\s*\*', left_side) or re.search(r'0\s*\*', right_side):
                mistakes.append({
                    "type": "zero_multiplication",
                    "description": "Found 0 multiplied by variable. This equals 0.",
                    "severity": "medium",
                    "trap_area": "Multiplication and simplification"
                })
        
        except Exception as e:
            log_error("Arithmetic Validity", str(e))
        
        return mistakes
    
    @staticmethod
    def check_common_patterns(equation: str) -> List[Dict[str, any]]:
        """
        Check for common algebra mistakes.
        
        Args:
            equation: Full equation string
            
        Returns:
            List of detected mistakes
        """
        mistakes = []
        
        try:
            # Check for (a+b)^2 common error: a^2 + b^2 (forgetting 2ab)
            if re.search(r'\(\s*[a-zA-Z0-9]\s*[+\-]\s*[a-zA-Z0-9]\s*\)\s*\*\*\s*2', equation):
                mistakes.append({
                    "type": "perfect_square_error",
                    "description": "Perfect square detected: (a±b)² = a² ± 2ab + b² (Don't forget the 2ab term!)",
                    "severity": "high",
                    "trap_area": "Expanding perfect squares"
                })
            
            # Check for fraction operations
            if '/' in equation:
                # Check if there might be numerator/denominator issues
                fractions = re.findall(r'(\d+)/(\d+)', equation)
                if fractions:
                    # Could be simplified
                    for num, denom in fractions:
                        if int(denom) == 0:
                            mistakes.append({
                                "type": "invalid_fraction",
                                "description": f"Invalid fraction: {num}/{denom}",
                                "severity": "critical",
                                "trap_area": "Fractions"
                            })
        
        except Exception as e:
            log_error("Common Patterns", str(e))
        
        return mistakes
    
    def detect_mistakes(self, equation: str) -> List[Dict[str, any]]:
        """
        Comprehensive mistake detection.
        
        Args:
            equation: Equation string
            
        Returns:
            List of all detected mistakes
        """
        all_mistakes = []
        
        try:
            # Check parentheses
            all_mistakes.extend(self.check_parentheses_balance(equation))
            
            # Check operators
            all_mistakes.extend(self.check_operator_consistency(equation))
            
            # Check common patterns
            all_mistakes.extend(self.check_common_patterns(equation))
            
            # Check arithmetic
            if '=' in equation:
                left, right = equation.split('=')
                all_mistakes.extend(self.check_arithmetic_validity(left, right))
            
            # Log findings
            if all_mistakes:
                logger.info(f"Detected {len(all_mistakes)} potential mistakes")
            else:
                logger.info("No obvious mistakes detected")
            
            return all_mistakes
            
        except Exception as e:
            log_error("Mistake Detection", str(e))
            return all_mistakes
    
    @staticmethod
    def get_trap_areas(equation: str) -> List[str]:
        """
        Get list of common trap areas based on equation content.
        
        Args:
            equation: Equation string
            
        Returns:
            List of trap area descriptions
        """
        trap_areas = []
        
        try:
            # Parentheses detected
            if '(' in equation or '[' in equation:
                trap_areas.append("Distribution of signs and numbers across brackets")
            
            # Negative numbers
            if re.search(r'[+\-]\s*-', equation) or re.search(r'=\s*-', equation):
                trap_areas.append("Handling negative numbers correctly")
            
            # Fractions
            if '/' in equation:
                trap_areas.append("Correct handling of fractions and reciprocals")
            
            # Powers
            if '^' in equation or '**' in equation:
                trap_areas.append("Correct application of exponent rules")
            
            # Multiple variables
            if equation.count('x') > 1:
                trap_areas.append("Combining like terms correctly")
            
            return trap_areas
            
        except Exception as e:
            log_error("Trap Areas", str(e))
            return trap_areas
