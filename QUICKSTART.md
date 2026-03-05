# Getting Started Guide - AI Math Tutor

## Quick Start (5 minutes)

### 1. Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

### 3. Use the App
1. Upload an equation image (JPG/PNG)
2. Review OCR result, correct if needed
3. Click "Parse Equation" to validate
4. Click "Solve Equation" to solve

---

## File Structure Explained

### Root Level
- **app.py** - Main Streamlit application with UI
- **requirements.txt** - Python package dependencies
- **.env.example** - Template for environment variables
- **.gitignore** - Git ignore rules
- **README.md** - Full documentation

### services/ (Core Processing)
- **ocr_service.py** - Extracts text from images
- **equation_parser.py** - Validates and converts to SymPy format
- **solver_service.py** - Solves equations symbolically
- **step_generator.py** - Creates step-by-step solutions
- **mistake_detector.py** - Finds common algebra errors

### utils/ (Helper Functions)
- **logger.py** - Logging configuration
- **image_preprocess.py** - Image enhancement
- **latex_converter.py** - LaTeX formatting

---

## Feature Highlights

### 1. OCR Recognition
Extracts mathematical equations from:
- Handwritten images
- Printed documents
- Photos of whiteboards
- Screenshots

Handles common OCR mistakes and cleans output.

### 2. Equation Parsing
Validates equation format:
- ✅ Balanced parentheses
- ✅ Valid operators (+, -, *, /)
- ✅ Exactly one equals sign
- ✅ Proper variable usage

Converts to SymPy format for solving.

### 3. Symbolic Solving
Solves different equation types:
- Linear: 2x + 5 = 15
- Quadratic: x² - 5x + 6 = 0
- Polynomial: x³ - 2x² + x = 0
- Complex expressions with brackets

### 4. Step-by-Step Solutions
Shows detailed steps:
1. Expansion (if needed)
2. Simplification
3. Term rearrangement
4. Final solution

Optional AI-powered explanations via Gemini.

### 5. Mistake Detection
Identifies common errors:
- ⚠️ Sign errors
- ⚠️ Bracket mistakes
- ⚠️ Distribution errors
- ⚠️ Division by zero
- ⚠️ Perfect square errors

---

## Example Workflows

### Example 1: Simple Linear Equation
**Input:** Image of "2x + 5 = 15"
**Steps:**
1. OCR extracts: "2x + 5 = 15"
2. Parser validates syntax
3. Solver finds: x = 5
4. Explanation: Subtract 5, then divide by 2

### Example 2: Quadratic Equation
**Input:** Image of "x² - 5x + 6 = 0"
**Steps:**
1. OCR extracts: "x^2 - 5x + 6 = 0"
2. Parser validates and converts
3. Solver factors: (x - 2)(x - 3) = 0
4. Solutions: x = 2, 3
5. Warnings: Check zero product property

### Example 3: Equation with Brackets
**Input:** Image of "2(x + 3) - 4 = 10"
**Steps:**
1. OCR extracts: "2(x + 3) - 4 = 10"
2. Parser validates
3. Solver expands: 2x + 6 - 4 = 10
4. Simplifies: 2x + 2 = 10
5. Solves: x = 4
6. Alert: Don't forget to multiply both terms in brackets!

---

## Configuration

### Environment Variables (.env)
```bash
# Optional: For AI-powered explanations
GEMINI_API_KEY=your_api_key_here
```

### Streamlit Settings (sidebar)
- **OCR Confidence Threshold**: 0.0 - 1.0 (default: 0.5)
- **Show Image Statistics**: View image quality metrics
- **Show LaTeX Code**: See mathematical formatting

---

## Troubleshooting

### Issue: OCR Not Recognizing Equation
**Solutions:**
- ✅ Improve image quality/lighting
- ✅ Use crisp, clear fonts
- ✅ Ensure equation is centered
- ✅ Manually correct in text box

### Issue: "Failed to parse equation"
**Check:**
- ✅ Balanced parentheses: ( ) [ ]
- ✅ Exactly one = sign
- ✅ Valid operators: +, -, *, /, ^
- ✅ No special symbols except variables and numbers

### Issue: Solver Errors
**Possible causes:**
- ✅ Division by zero: Equation has no solution
- ✅ Complex numbers: Solution not in real numbers
- ✅ No equals sign: Need equation, not just expression

### Issue: Gemini Not Working
**Check:**
- ✅ API key is correct
- ✅ Internet connection available
- ✅ API key has usage remaining
- ✅ Environment variable set: .env file exists

---

## Code Quality

All code includes:
- ✅ **Type Hints**: Full type annotations
- ✅ **Docstrings**: Function documentation
- ✅ **Error Handling**: Graceful failures
- ✅ **Logging**: Detailed event tracking
- ✅ **Modularity**: Separate concerns

---

## Dependencies Overview

| Package | Purpose |
|---------|---------|
| streamlit | Web UI framework |
| PIL/Pillow | Image handling |
| opencv-python | Image processing |
| easyocr | Text recognition |
| sympy | Symbolic math solving |
| numpy | Numerical operations |
| python-dotenv | Environment variables |
| google-generativeai | AI explanations |

---

## Testing Examples

Try these equations to test:

**Simple Linear**
```
x + 5 = 12
```

**With Brackets**
```
2(x - 3) = 8
```

**Quadratic**
```
x^2 - 4 = 0
```

**Multi-step**
```
3x + 2 = 2x + 7
```

**With Fractions**
```
x/2 + 3 = 7
```

---

## Performance Tips

1. **First Run**: EasyOCR downloads ~100MB models (one-time)
2. **Image Size**: Smaller images process faster
3. **Resolution**: 300+ DPI recommended for clarity
4. **All at Once**: Let each step complete before next

---

## Next Steps

1. ✅ Run the app: `streamlit run app.py`
2. ✅ Try an equation image
3. ✅ Explore the sidebar options
4. ✅ Check `math_tutor.log` for details
5. ✅ Add Gemini API key for better explanations
6. ✅ Customize UI in app.py as needed

---

## Support & Resources

- **SymPy**: https://docs.sympy.org/
- **Streamlit**: https://docs.streamlit.io/
- **EasyOCR**: https://github.com/JaidedAI/EasyOCR
- **Gemini**: https://ai.google.dev/

---

**Happy Learning! 📐✨**
