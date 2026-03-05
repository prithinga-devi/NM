# ✅ Installation Verification Guide

Complete checklist to verify AI Math Tutor is properly installed and ready to use.

---

## 1️⃣ Repository Structure Verification

**Check that all files exist:**

```bash
# Navigate to project directory
cd ai-math-tutor

# Verify core files
ls -la app.py requirements.txt .env.example .gitignore README.md

# Verify services
ls -la services/
# Should show: __init__.py, ocr_service.py, equation_parser.py, 
#              solver_service.py, step_generator.py, mistake_detector.py

# Verify utilities
ls -la utils/
# Should show: __init__.py, logger.py, image_preprocess.py, latex_converter.py

# Verify documentation
ls -la *.md
# Should show: README.md, QUICKSTART.md, API_DOCS.md, DEPLOYMENT.md, 
#              CONFIGURATION.md, PROJECT_SUMMARY.md, INDEX.md
```

**Expected output**: 19 files, 4 directories

---

## 2️⃣ Python Environment Verification

**Check Python version (must be 3.8+):**

```bash
python --version
# Expected: Python 3.10+ (or 3.8+)

python3 --version
# Expected: Python 3.10+ (or 3.8+)
```

**Create virtual environment:**

```bash
# Create
python -m venv venv

# Verify venv created
ls -la venv/
# Should show: bin, lib, pyvenv.cfg, etc.

# Activate (Linux/Mac)
source venv/bin/activate
# Should show: (venv) in terminal

# Activate (Windows)
venv\Scripts\activate
# Should show: (venv) in terminal
```

---

## 3️⃣ Dependencies Installation Verification

**Install dependencies:**

```bash
# Ensure venv is activated
which python
# Should show path containing /venv/

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected packages:**

```
streamlit           >= 1.28.0
pillow              >= 10.0.0
numpy               >= 1.24.0
opencv-python       >= 4.8.0
easyocr             >= 1.6.0
sympy               >= 1.12
python-dotenv       >= 1.0.0
google-generativeai >= 0.3.0
```

**Verify each:**

```bash
python -c "import streamlit; print(f'Streamlit: {streamlit.__version__}')"
python -c "import cv2; print(f'OpenCV: {cv2.__version__}')"
python -c "import easyocr; print('EasyOCR: OK')"
python -c "import sympy; print(f'SymPy: {sympy.__version__}')"
python -c "from PIL import Image; print('Pillow: OK')"
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
python -c "import dotenv; print('python-dotenv: OK')"
python -c "import google.generativeai; print('Google Generative AI: OK')"
```

All should print without errors.

---

## 4️⃣ Environment Configuration Verification

**Create .env file from template:**

```bash
# Copy template
cp .env.example .env

# Verify file created
ls -la .env
# Should show: .env file exists

# Optional: Add Gemini API key
# Edit .env and add: GEMINI_API_KEY=your_key_here
```

**Verify environment loading:**

```bash
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv('GEMINI_API_KEY', 'Not set')
print(f'Gemini API Key: {key[:5]}...' if key != 'Not set' else 'Gemini not configured (optional)')
"
```

---

## 5️⃣ Module Import Verification

**Test all modules can be imported:**

```bash
python << 'EOF'
print("Testing imports...")

try:
    from services.ocr_service import OCRService
    print("✓ OCR Service: OK")
except Exception as e:
    print(f"✗ OCR Service: {e}")

try:
    from services.equation_parser import EquationParser
    print("✓ Equation Parser: OK")
except Exception as e:
    print(f"✗ Equation Parser: {e}")

try:
    from services.solver_service import SolverService
    print("✓ Solver Service: OK")
except Exception as e:
    print(f"✗ Solver Service: {e}")

try:
    from services.step_generator import StepGenerator
    print("✓ Step Generator: OK")
except Exception as e:
    print(f"✗ Step Generator: {e}")

try:
    from services.mistake_detector import MistakeDetector
    print("✓ Mistake Detector: OK")
except Exception as e:
    print(f"✗ Mistake Detector: {e}")

try:
    from utils.logger import logger
    print("✓ Logger: OK")
except Exception as e:
    print(f"✗ Logger: {e}")

try:
    from utils.image_preprocess import preprocess_image
    print("✓ Image Preprocess: OK")
except Exception as e:
    print(f"✗ Image Preprocess: {e}")

try:
    from utils.latex_converter import simple_to_latex
    print("✓ LaTeX Converter: OK")
except Exception as e:
    print(f"✗ LaTeX Converter: {e}")

print("\nAll modules imported successfully!")
EOF
```

**Expected output**: All modules should show "✓ OK"

---

## 6️⃣ Streamlit Verification

**Check Streamlit is working:**

```bash
streamlit --version
# Expected: Streamlit, version 1.28.0+ (or your installed version)

streamlit hello
# Should open demo app in browser
# Press Ctrl+C to close
```

---

## 7️⃣ Application Launch Verification

**Start the application:**

```bash
streamlit run app.py
```

**Expected output in terminal:**

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501

Press CTRL+C to stop the server
```

**Expected in browser:**

- Page title: "AI Math Tutor"
- Upload button visible
- Sidebar with settings
- Info message about uploading images

---

## 8️⃣ Functional Testing

**Test OCR Service:**

```python
from services.ocr_service import OCRService
import cv2

# Create OCR service
ocr = OCRService()
print(f"OCR Service initialized: {ocr.reader is not None}")

# Test with a simple image (requires opencv/numpy)
# If you have an image:
# image = cv2.imread('test_image.png')
# text, conf, success = ocr.process_image(image)
# print(f"OCR Result: {text}, Confidence: {conf}, Success: {success}")
```

**Test Equation Parser:**

```python
from services.equation_parser import EquationParser

parser = EquationParser()

# Test validation
is_valid, msg = parser.validate_equation("2x + 5 = 15")
print(f"Equation valid: {is_valid}")

# Test parsing
equation, success, msg = parser.parse_equation("2x + 5 = 15")
print(f"Parsing success: {success}")
if success:
    print(f"Parsed equation: {equation}")
```

**Test Solver:**

```python
from services.solver_service import SolverService
from services.equation_parser import EquationParser

parser = EquationParser()
solver = SolverService()

# Parse an equation
eq, success, _ = parser.parse_equation("2x + 5 = 15")

# Solve it
if success:
    result = solver.solve_and_simplify(eq)
    print(f"Solution: {result['solutions']}")
    print(f"Success: {result['success']}")
```

**Test Mistake Detection:**

```python
from services.mistake_detector import MistakeDetector

detector = MistakeDetector()

# Test error detection
equation = "2(x+3) = 4"  
mistakes = detector.detect_mistakes(equation)
trap_areas = detector.get_trap_areas(equation)

print(f"Found {len(mistakes)} mistakes")
print(f"Trap areas: {trap_areas}")
```

---

## 9️⃣ Logging Verification

**Check logs are being created:**

```bash
# Run a quick test
python -c "
from utils.logger import logger
logger.info('Test log message')
print('Check if math_tutor.log was created')
"

# Verify log file
ls -la math_tutor.log
cat math_tutor.log
```

**Expected**: Log file created with timestamp and messages

---

## 🔟 Performance Verification

**Quick performance check:**

```bash
time python << 'EOF'
from services.equation_parser import EquationParser
from services.solver_service import SolverService

parser = EquationParser()
solver = SolverService()

# Parse and solve
eq, success, _ = parser.parse_equation("x^2 - 5x + 6 = 0")
if success:
    result = solver.solve_and_simplify(eq)
    print(f"Solutions: {result['solutions']}")

print("Performance test complete")
EOF
```

**Expected**: Completes in under 1 second

---

## ✅ Final Verification Checklist

Use this checklist to confirm everything is working:

```bash
# Copy this into terminal
cat << 'EOF'
VERIFICATION CHECKLIST
====================
[ ] Python 3.8+ installed
[ ] Virtual environment created and activated
[ ] All dependencies installed (pip install -r requirements.txt)
[ ] .env file created
[ ] All 19 files present
[ ] All Python modules import without error
[ ] Streamlit installed (streamlit --version)
[ ] App launches (streamlit run app.py)
[ ] Browser opens to http://localhost:8501
[ ] Upload button visible in UI
[ ] Sidebar configuration visible
[ ] math_tutor.log file created
[ ] All services functional
[ ] Performance acceptable

If all checked, installation is complete!
EOF
```

---

## 🐛 Troubleshooting

### Issue: "Command not found: python"
**Solution**:
```bash
python3 --version
# Use python3 instead of python for all commands
```

### Issue: "ModuleNotFoundError"
**Solution**:
```bash
# Ensure venv is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Streamlit not found"
**Solution**:
```bash
pip install streamlit==1.28.0
streamlit --version
```

### Issue: "EasyOCR slow first run"
**Solution**:
This is normal - first run downloads ~100MB models
Subsequent runs will be faster

### Issue: "Port 8501 already in use"
**Solution**:
```bash
streamlit run app.py --server.port 8000
# Or kill the process using port 8501
```

### Issue: "ImportError in app.py"
**Solution**:
```bash
# Make sure you're in project root directory
cd /path/to/ai-math-tutor
python app.py  # Should show what's missing
```

### Issue: "OpenCV not working"
**Solution**:
```bash
pip uninstall opencv-python
pip install opencv-python==4.8.0
```

---

## 📝 Verification Report Template

Save this for documentation:

```
AI MATH TUTOR - INSTALLATION VERIFICATION REPORT
================================================

Date: [Today's date]
Python Version: [From python --version]
OS: [From uname -s]

FILES VERIFIED:
[ ] app.py
[ ] requirements.txt
[ ] services/ (5 files)
[ ] utils/ (4 files)
[ ] Documentation (7 files)

DEPENDENCIES VERIFIED:
[ ] streamlit
[ ] opencv-python
[ ] easyocr
[ ] sympy
[ ] pillow
[ ] numpy
[ ] python-dotenv
[ ] google-generativeai

MODULES IMPORTED:
[ ] OCRService
[ ] EquationParser
[ ] SolverService
[ ] StepGenerator
[ ] MistakeDetector
[ ] logger
[ ] image_preprocess
[ ] latex_converter

FUNCTIONAL TESTS:
[ ] Application launches
[ ] UI displays correctly
[ ] Equation parsing works
[ ] Solver provides answers
[ ] Logs are created

STATUS: ✅ READY FOR USE
```

---

## 🚀 Next Steps After Verification

1. **Test with real images**: Upload equation photos
2. **Explore sidebar settings**: Try different configurations
3. **Read documentation**: Check README.md for details
4. **Extend functionality**: See API_DOCS.md for adding features
5. **Deploy**: Follow DEPLOYMENT.md for production setup

---

## ✨ Success!

If you've completed this verification checklist and all items are checked, your **AI Math Tutor installation is complete and ready to use!**

**Start the app anytime with:**
```bash
streamlit run app.py
```

---

**Verification Guide Version**: 1.0
**Last Updated**: March 5, 2026
**Status**: Complete ✅
