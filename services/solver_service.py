"""
Solver Service for solving algebraic equations using SymPy.
Handles linear equations, quadratic equations, and symbolic computation.
"""

from typing import List, Optional, Tuple, Dict, Any
from sympy import Eq, solve, simplify, expand, factor
from sympy.abc import x
from utils.logger import logger, log_error, log_solver_result


class SolverService:
    """Service for solving algebraic equations using SymPy."""
    
    def __init__(self, variable='x'):
        """
        Initialize solver service.
        
        Args:
            variable: The variable to solve for
        """
        self.variable = variable
        logger.info(f"SolverService initialized for variable: {variable}")
    
    @staticmethod
    def solve_equation(equation) -> Tuple[List[Any], bool, str]:
        """
        Solve a SymPy equation.
        
        Args:
            equation: SymPy equation object
            
        Returns:
            Tuple of (solutions_list, success_flag, message)
        """
        try:
            if equation is None:
                return [], False, "Invalid equation"
            
            solutions = solve(equation, x)
            
            if not solutions:
                return [], False, "No solutions found"
            
            logger.info(f"Equation solved successfully: {solutions}")
            return solutions, True, ""
            
        except ZeroDivisionError:
            error_msg = "Division by zero encountered"
            log_error("Solver", error_msg)
            return [], False, error_msg
            
        except Exception as e:
            error_msg = f"Error solving equation: {str(e)}"
            log_error("Solver", error_msg)
            return [], False, error_msg
    
    @staticmethod
    def simplify_expression(expr) -> Tuple[Any, bool, str]:
        """
        Simplify a SymPy expression.
        
        Args:
            expr: SymPy expression
            
        Returns:
            Tuple of (simplified_expression, success_flag, message)
        """
        try:
            simplified = simplify(expr)
            logger.info(f"Expression simplified: {simplified}")
            return simplified, True, ""
            
        except Exception as e:
            error_msg = f"Error simplifying expression: {str(e)}"
            log_error("Simplification", error_msg)
            return expr, False, error_msg
    
    @staticmethod
    def expand_expression(expr) -> Tuple[Any, bool, str]:
        """
        Expand a SymPy expression.
        
        Args:
            expr: SymPy expression
            
        Returns:
            Tuple of (expanded_expression, success_flag, message)
        """
        try:
            expanded = expand(expr)
            logger.info(f"Expression expanded: {expanded}")
            return expanded, True, ""
            
        except Exception as e:
            error_msg = f"Error expanding expression: {str(e)}"
            log_error("Expansion", error_msg)
            return expr, False, error_msg
    
    @staticmethod
    def factor_expression(expr) -> Tuple[Any, bool, str]:
        """
        Factor a SymPy expression.
        
        Args:
            expr: SymPy expression
            
        Returns:
            Tuple of (factored_expression, success_flag, message)
        """
        try:
            factored = factor(expr)
            logger.info(f"Expression factored: {factored}")
            return factored, True, ""
            
        except Exception as e:
            error_msg = f"Error factoring expression: {str(e)}"
            log_error("Factoring", error_msg)
            return expr, False, error_msg
    
    def solve_and_simplify(self, equation) -> Dict[str, Any]:
        """
        Solve equation and return comprehensive solution info.
        
        Args:
            equation: SymPy equation object
            
        Returns:
            Dictionary with solution details
        """
        result = {
            "original_equation": str(equation),
            "solutions": [],
            "expanded_left": None,
            "expanded_right": None,
            "simplified_left": None,
            "simplified_right": None,
            "success": False,
            "message": ""
        }
        
        try:
            # Expand both sides
            left_expanded, _, _ = self.expand_expression(equation.lhs)
            right_expanded, _, _ = self.expand_expression(equation.rhs)
            
            result["expanded_left"] = str(left_expanded)
            result["expanded_right"] = str(right_expanded)
            
            # Simplify both sides
            left_simplified, _, _ = self.simplify_expression(equation.lhs)
            right_simplified, _, _ = self.simplify_expression(equation.rhs)
            
            result["simplified_left"] = str(left_simplified)
            result["simplified_right"] = str(right_simplified)
            
            # Solve
            solutions, success, message = self.solve_equation(equation)
            
            if success:
                result["solutions"] = [str(sol) for sol in solutions]
                result["success"] = True
                result["message"] = f"Found {len(solutions)} solution(s)"
                log_solver_result(str(equation), str(solutions))
            else:
                result["message"] = message
            
            return result
            
        except Exception as e:
            error_msg = f"Error in solve_and_simplify: {str(e)}"
            log_error("Solver", error_msg)
            result["message"] = error_msg
            return result
    
    @staticmethod
    def get_equation_type(equation) -> str:
        """
        Determine the type of equation (linear, quadratic, etc.).
        
        Args:
            equation: SymPy equation
            
        Returns:
            Equation type string
        """
        try:
            from sympy import degree
            
            # Get the left side and find its degree
            left_side = equation.lhs - equation.rhs
            eq_degree = degree(left_side, x)
            
            if eq_degree == 1:
                return "linear"
            elif eq_degree == 2:
                return "quadratic"
            elif eq_degree > 2:
                return f"polynomial (degree {eq_degree})"
            else:
                return "unknown"
                
        except Exception:
            return "unknown"
