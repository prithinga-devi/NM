# API Documentation - AI Math Tutor

## Overview

This document describes the programmatic API for the AI Math Tutor services.

---

## Services API

### 1. OCRService

Extracts text from images using EasyOCR.

#### Usage
```python
from services.ocr_service import OCRService
import cv2

# Initialize
ocr_service = OCRService(languages=['en'])

# Extract text from image
image = cv2.imread('equation.png')
text, confidence, success = ocr_service.process_image(image)

if success:
    print(f"Extracted: {text}")
    print(f"Confidence: {confidence:.2%}")
```

#### Methods

**`__init__(languages=['en'])`**
- Initialize OCR service
- Args: `languages` (list) - Language codes

**`extract_text(image: np.ndarray) -> Tuple[str, float, bool]`**
- Raw text extraction
- Returns: (text, confidence, success)

**`clean_ocr_output(text: str) -> str`** (static)
- Clean and standardize text
- Handles common OCR mistakes

**`process_image(image: np.ndarray) -> Tuple[str, float, bool]`**
- Complete OCR pipeline
- Returns: (cleaned_text, confidence, success)

---

### 2. EquationParser

Validates and parses equations to SymPy format.

#### Usage
```python
from services.equation_parser import EquationParser

# Initialize
parser = EquationParser(variable='x')

# Parse equation
equation, success, message = parser.parse_equation("2x + 5 = 15")

if success:
    print(f"Parsed: {equation}")
    # Solve it
    from sympy import solve
    solutions = solve(equation, parser.x)
    print(f"Solutions: {solutions}")
```

#### Methods

**`__init__(variable='x')`**
- Initialize with variable to solve for
- Default: 'x'

**`validate_equation(equation: str) -> Tuple[bool, str]`** (static)
- Validate equation syntax
- Returns: (is_valid, error_message)

**`preprocess_equation(equation: str) -> str`**
- Prepare equation for parsing
- Handles implicit multiplication, operator standardization

**`parse_equation(equation_str: str) -> Tuple[Optional[Eq], bool, str]`**
- Convert string to SymPy Equation
- Returns: (equation_object, success, error_message)

**`parse_expression(expr_str: str) -> Tuple[Optional[Expr], bool, str]`**
- Parse expression without equals sign
- Returns: (expression, success, error_message)

---

### 3. SolverService

Solves equations using SymPy's symbolic engine.

#### Usage
```python
from services.solver_service import SolverService

solver = SolverService()

# Solve equation
result = solver.solve_and_simplify(equation)

if result['success']:
    solutions = result['solutions']
    print(f"Solutions: {solutions}")
    print(f"Equation type: {result['message']}")
```

#### Methods

**`solve_equation(equation) -> Tuple[List, bool, str]`** (static)
- Solve SymPy equation
- Returns: (solutions_list, success, message)

**`simplify_expression(expr) -> Tuple[Any, bool, str]`** (static)
- Simplify expression
- Returns: (simplified, success, message)

**`expand_expression(expr) -> Tuple[Any, bool, str]`** (static)
- Expand expression
- Returns: (expanded, success, message)

**`factor_expression(expr) -> Tuple[Any, bool, str]`** (static)
- Factor expression
- Returns: (factored, success, message)

**`solve_and_simplify(equation) -> Dict`**
- Complete solution with details
- Returns dictionary:
  ```python
  {
      'original_equation': str,
      'solutions': [str],
      'expanded_left': str,
      'expanded_right': str,
      'simplified_left': str,
      'simplified_right': str,
      'success': bool,
      'message': str
  }
  ```

**`get_equation_type(equation) -> str`** (static)
- Determine equation type (linear, quadratic, etc.)
- Returns: type string

---

### 4. StepGenerator

Generates step-by-step solutions.

#### Usage
```python
from services.step_generator import StepGenerator

generator = StepGenerator()

# Generate solution steps
result = generator.generate_complete_solution(equation, solutions)

if result['success']:
    for step in result['steps']:
        print(f"Step {step['step_number']}: {step['title']}")
        print(f"  {step['description']}")
        print(f"  Equation: {step['equation']}")
```

#### Methods

**`__init__()`**
- Initialize generator
- Loads Gemini credentials from .env if available

**`generate_basic_steps(equation, solutions) -> List[Dict]`** (static)
- Generate steps without AI
- Returns list of step dictionaries

**`generate_detailed_explanations(equation_str, solutions) -> List[Dict]`**
- Use Gemini for enhanced explanations
- Returns list of step dictionaries

**`generate_complete_solution(equation, solutions) -> Dict`**
- Full solution with best available steps
- Returns:
  ```python
  {
      'success': bool,
      'steps': [
          {
              'step_number': int,
              'title': str,
              'description': str,
              'equation': str
          },
          ...
      ],
      'has_gemini': bool,
      'message': str
  }
  ```

---

### 5. MistakeDetector

Detects common algebra mistakes.

#### Usage
```python
from services.mistake_detector import MistakeDetector

detector = MistakeDetector()

# Check equation
mistakes = detector.detect_mistakes("2(x+3) = 4")
trap_areas = detector.get_trap_areas("2(x+3) = 4")

if mistakes:
    for mistake in mistakes:
        print(f"Type: {mistake['type']}")
        print(f"Description: {mistake['description']}")
        print(f"Severity: {mistake['severity']}")
```

#### Methods

**`check_parentheses_balance(equation) -> List[Dict]`** (static)
- Check bracket balance
- Returns: list of mistakes

**`check_operator_consistency(equation) -> List[Dict]`** (static)
- Check operator usage
- Returns: list of mistakes

**`check_arithmetic_validity(left_side, right_side) -> List[Dict]`** (static)
- Check arithmetic issues
- Returns: list of mistakes

**`check_common_patterns(equation) -> List[Dict]`** (static)
- Check for known pitfalls
- Returns: list of mistakes

**`detect_mistakes(equation) -> List[Dict]`**
- Comprehensive mistake detection
- Returns complete list of issues

**`get_trap_areas(equation) -> List[str]`** (static)
- Identify problem areas in equation
- Returns: list of descriptions

---

## Utilities API

### 1. Image Preprocessing

```python
from utils.image_preprocess import preprocess_image, get_image_stats
import cv2

# Load image
image = cv2.imread('equation.png')

# Preprocess
preprocessed, success = preprocess_image(image)

if success:
    # Get stats
    stats = get_image_stats(preprocessed)
    print(stats)
```

#### Functions

**`resize_image(image, max_width=1200, max_height=800) -> np.ndarray`**
- Resize while maintaining aspect ratio

**`convert_to_grayscale(image) -> np.ndarray`**
- Convert to single channel

**`adjust_contrast(image, alpha=1.5, beta=30) -> np.ndarray`**
- Enhance contrast

**`reduce_noise(image) -> np.ndarray`**
- Bilateral filtering

**`apply_adaptive_threshold(image) -> np.ndarray`**
- Convert to binary

**`preprocess_image(image) -> Tuple[np.ndarray, bool]`**
- Complete pipeline
- Returns: (processed_image, success)

**`get_image_stats(image) -> Dict`**
- Image quality metrics
- Returns dictionary with stats

---

### 2. LaTeX Conversion

```python
from utils.latex_converter import simple_to_latex, equation_to_latex

# Convert equation
latex = simple_to_latex("2x + 5 = 15")
print(latex)  # Output: 2x + 5 = 15

# Format for display
display = equation_to_latex("2x + 5 = 15")
print(display)  # $$2x + 5 = 15$$
```

#### Functions

**`escape_latex(text) -> str`**
- Escape special LaTeX characters

**`standardize_operators(equation) -> str`**
- Convert × to *, ÷ to /, − to -

**`simple_to_latex(equation) -> str`**
- Basic conversion to LaTeX

**`equation_to_latex(equation, is_solution=False) -> str`**
- Convert with formatting for display

**`format_step(step_description, equation) -> Tuple[str, str]`**
- Format a solution step

---

### 3. Logging

```python
from utils.logger import logger, log_ocr_result, log_solver_result, log_error

# Automatic logging
logger.info("Processing equation")

# Specialized logging
log_ocr_result("2x + 5 = 15", 0.95)
log_solver_result("2x + 5 = 15", "x = 5")
log_error("OMG", "Something went wrong!")
```

#### Functions

**`setup_logger(name, log_file='math_tutor.log') -> Logger`**
- Create logger instance

**`log_ocr_result(equation, confidence)`**
- Log OCR results

**`log_solver_result(equation, solution)`**
- Log solver results

**`log_error(error_type, error_message)`**
- Log errors

---

## Complete Example

### End-to-End Workflow

```python
import cv2
from services.ocr_service import OCRService
from services.equation_parser import EquationParser
from services.solver_service import SolverService
from services.step_generator import StepGenerator
from services.mistake_detector import MistakeDetector
from utils.image_preprocess import preprocess_image

# 1. Load image
image = cv2.imread('equation.png')

# 2. Preprocess
preprocessed, success = preprocess_image(image)

# 3. Extract text
ocr = OCRService()
text, confidence, success = ocr.process_image(preprocessed)
print(f"OCR: {text} ({confidence:.2%})")

# 4. Parse
parser = EquationParser()
equation, success, msg = parser.parse_equation(text)
print(f"Parsed: {equation}")

# 5. Detect mistakes
detector = MistakeDetector()
mistakes = detector.detect_mistakes(text)
for m in mistakes:
    print(f"Warning: {m['description']}")

# 6. Solve
solver = SolverService()
result = solver.solve_and_simplify(equation)
print(f"Solutions: {result['solutions']}")

# 7. Generate steps
generator = StepGenerator()
steps = generator.generate_complete_solution(equation, result['solutions'])
for step in steps['steps']:
    print(f"{step['step_number']}. {step['title']}")
    print(f"   {step['equation']}")
```

---

## Error Handling

All services return tuples with success flags:

```python
result, success, message = some_service_function(...)

if not success:
    print(f"Error: {message}")
    # Handle error
else:
    # Use result
    print(result)
```

---

## Performance Considerations

1. **OCR**: First run downloads ~100MB models
2. **Caching**: OCR reader loaded once and reused
3. **SymPy**: Faster for simple equations, slower for complex
4. **Gemini**: Requires internet, adds latency

---

## Extending the System

### Add New Service

1. Create file in `services/`
2. Follow class-based structure
3. Add type hints
4. Add docstrings
5. Use logger for tracking

### Modify Parser

Edit `services/equation_parser.py`:
- Add pattern validation
- Extend preprocessing
- Support new operators

### Add Mistake Types

Edit `services/mistake_detector.py`:
- Add detection method
- Return mistake dictionary
- Log findings

---

## Type Hints Reference

```python
from typing import List, Dict, Tuple, Optional, Any
import numpy as np
from sympy import Eq, symbols

# Common signatures:
def process(equation: str) -> Tuple[str, float, bool]: ...
def detect(text: str) -> List[Dict[str, Any]]: ...
def solve(eq: Eq) -> List[Any]: ...
def preprocess(image: np.ndarray) -> Tuple[np.ndarray, bool]: ...
```

---

## Troubleshooting API Usage

### Import Errors
```python
# Make sure you're in correct directory
import sys
sys.path.insert(0, '/path/to/ai-math-tutor')

from services.ocr_service import OCRService
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Gemini Errors
```python
# Check if GEMINI_API_KEY is set
import os
print(os.getenv('GEMINI_API_KEY'))
```

---

## API Stability

- **Stable**: ocr_service, equation_parser, solver_service
- **In Development**: step_generator (Gemini integration)
- **Experimental**: mistake_detector (adding more patterns)

---

**For questions, refer to docstrings in source code or main README.md**
