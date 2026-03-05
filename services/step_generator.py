"""
Step Generator for creating step-by-step solutions.
Generates detailed algebra steps and optionally uses Google Gemini for explanations.
"""

import os
from typing import List, Dict, Optional, Tuple
from sympy import Eq, solve, expand, simplify, symbols
from utils.logger import logger, log_error

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google Generative AI not installed. Gemini features will be unavailable.")


class StepGenerator:
    """Generate step-by-step solutions for algebraic equations."""
    
    def __init__(self):
        """Initialize step generator."""
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        
        if self.gemini_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=self.gemini_key)
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini API initialized successfully")
            except Exception as e:
                log_error("Gemini Initialization", str(e))
                self.model = None
        else:
            self.model = None
            if not self.gemini_key:
                logger.info("GEMINI_API_KEY not set. Using built-in step generation only.")
    
    @staticmethod
    def generate_basic_steps(equation, solutions: List) -> List[Dict[str, str]]:
        """
        Generate basic step-by-step solution without Gemini.
        
        Args:
            equation: SymPy equation
            solutions: List of solutions
            
        Returns:
            List of step dictionaries
        """
        steps = []
        x = symbols('x')
        
        try:
            # Step 1: Original equation
            steps.append({
                "step_number": 1,
                "title": "Original Equation",
                "description": "Start with the original equation",
                "equation": str(equation)
            })
            
            # Step 2: Expand if needed
            left_expanded = expand(equation.lhs)
            right_expanded = expand(equation.rhs)
            
            if left_expanded != equation.lhs or right_expanded != equation.rhs:
                steps.append({
                    "step_number": len(steps) + 1,
                    "title": "Expand Expression",
                    "description": "Expand brackets if present",
                    "equation": f"{left_expanded} = {right_expanded}"
                })
            
            # Step 3: Move all terms to one side
            moved_equation = left_expanded - right_expanded
            steps.append({
                "step_number": len(steps) + 1,
                "title": "Move All Terms to One Side",
                "description": "Subtract right side from both sides",
                "equation": f"{moved_equation} = 0"
            })
            
            # Step 4: Simplify
            simplified = simplify(moved_equation)
            if simplified != moved_equation:
                steps.append({
                    "step_number": len(steps) + 1,
                    "title": "Simplify",
                    "description": "Combine like terms",
                    "equation": f"{simplified} = 0"
                })
            
            # Step 5: Solution
            if solutions:
                sol_str = ", ".join([str(s) for s in solutions])
                steps.append({
                    "step_number": len(steps) + 1,
                    "title": "Solution",
                    "description": "Solve for the variable",
                    "equation": f"x = {sol_str}"
                })
            
            logger.info(f"Generated {len(steps)} basic steps")
            return steps
            
        except Exception as e:
            log_error("Step Generation", str(e))
            return steps
    
    def generate_detailed_explanations(self, equation_str: str, solutions: List) -> List[Dict[str, str]]:
        """
        Generate detailed explanations using Gemini if available.
        
        Args:
            equation_str: String representation of equation
            solutions: List of solutions
            
        Returns:
            List of step dictionaries with explanations
        """
        if not self.model:
            logger.warning("Gemini model not available. Using basic steps only.")
            return []
        
        try:
            prompt = f"""
You are a math tutor. Provide a clear step-by-step solution to this algebra equation:

Equation: {equation_str}

Return EXACTLY in this JSON format (no markdown, just JSON):
{{"steps": [
  {{"step_number": 1, "title": "...", "description": "...", "equation": "..."}},
  {{"step_number": 2, "title": "...", "description": "...", "equation": "..."}}
]}}

Each step should be clear and educational. Include:
- Step number and title
- Clear description of what you're doing
- The resulting equation

Solutions found: {', '.join([str(s) for s in solutions])}
"""
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                try:
                    import json
                    response_text = response.text.strip()
                    
                    # Remove markdown code blocks if present
                    if response_text.startswith('```'):
                        response_text = response_text.split('```')[1]
                        if response_text.startswith('json'):
                            response_text = response_text[4:]
                    
                    data = json.loads(response_text)
                    logger.info(f"Generated {len(data.get('steps', []))} detailed steps via Gemini")
                    return data.get('steps', [])
                    
                except json.JSONDecodeError as e:
                    log_error("JSON Parsing", f"Failed to parse Gemini response: {str(e)}")
                    return []
            
            return []
            
        except Exception as e:
            log_error("Gemini Step Generation", str(e))
            return []
    
    def generate_complete_solution(self, equation, solutions: List) -> Dict[str, any]:
        """
        Generate complete solution with steps and explanations.
        
        Args:
            equation: SymPy equation
            solutions: List of solutions
            
        Returns:
            Dictionary with solution details
        """
        result = {
            "success": False,
            "steps": [],
            "has_gemini": self.model is not None,
            "message": ""
        }
        
        try:
            # Always generate basic steps
            basic_steps = self.generate_basic_steps(equation, solutions)
            result["steps"] = basic_steps
            
            # Try to get detailed explanations from Gemini
            if self.model:
                detailed_steps = self.generate_detailed_explanations(str(equation), solutions)
                if detailed_steps:
                    result["steps"] = detailed_steps
            
            result["success"] = True
            return result
            
        except Exception as e:
            error_msg = f"Error generating complete solution: {str(e)}"
            log_error("Complete Solution Generation", error_msg)
            result["message"] = error_msg
            return result
