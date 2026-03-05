# AI Math Tutor

A complete production-ready system that helps students learn algebra by uploading equation images, extracting them using OCR, solving them symbolically, and providing step-by-step explanations with common mistake detection.

## 🎯 Features

### Core Functionality
- **📸 Image Upload**: Support for JPG, JPEG, PNG images
- **🔍 OCR Recognition**: Extract equations from handwritten or printed images using EasyOCR
- **📊 Equation Parsing**: Validate and parse equations to SymPy format
- **✨ Symbolic Solving**: Solve linear, quadratic, and polynomial equations
- **📖 Step-by-Step Solutions**: Generate detailed solution steps
- **⚠️ Mistake Detection**: Identify common algebra errors and trap areas
- **🤖 AI Explanations**: Use Google Gemini for enhanced step-by-step guidance (optional)

### Image Processing
- Image resizing and normalization
- Grayscale conversion
- Noise reduction
- Contrast adjustment
- Adaptive thresholding

### Equation Support
- Linear equations: `2x + 5 = 15`
- Quadratic equations: `x² - 5x + 6 = 0`
- Polynomial equations: `x³ - 2x² + x = 0`
- Complex expressions with brackets and operators

### Common Mistakes Detected
- Sign errors in arithmetic
- Incorrect distributive property application
- Division by zero
- Unbalanced parentheses
- Missing brackets in multi-term expressions
- Perfect square errors (forgetting 2ab term)
- Variable loss in operations

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **UI Framework** | Streamlit |
| **Image Processing** | OpenCV |
| **OCR** | EasyOCR |
| **Symbolic Math** | SymPy |
| **AI Assistant** | Google Gemini API |
| **Environment** | python-dotenv |
| **Language** | Python 3.8+ |

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 2GB disk space (for EasyOCR models)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd ai-math-tutor
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment (Optional)
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Gemini API key
# Get free API key from: https://ai.google.dev
```

## 🚀 Running the Application

### Start the Streamlit App
```bash
streamlit run app.py
```

The application will launch at `http://localhost:8501`

### Run with Custom Port
```bash
streamlit run app.py --server.port 8000
```

## 📂 Project Structure

```
ai-math-tutor/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
│
├── services/
│   ├── ocr_service.py         # OCR text extraction
│   ├── equation_parser.py      # Equation validation and parsing
│   ├── solver_service.py       # Symbolic equation solving
│   ├── step_generator.py       # Step-by-step solution generation
│   └── mistake_detector.py     # Common error detection
│
├── utils/
│   ├── image_preprocess.py    # Image enhancement pipeline
│   ├── latex_converter.py     # LaTeX formatting
│   └── logger.py              # Logging utility
│
└── assets/                     # Images, icons (if needed)
```

## 🎓 Usage Guide

### Basic Workflow

1. **Start the App**
   ```bash
   streamlit run app.py
   ```

2. **Upload Image**
   - Click the upload button in the sidebar
   - Select an image containing an algebra equation
   - The app automatically preprocesses the image

3. **Extract Equation**
   - The OCR service extracts text from the image
   - Review and correct the extracted equation if needed
   - Adjust the OCR confidence threshold if needed (sidebar)

4. **Parse Equation**
   - Click "Parse Equation" button
   - System validates the equation syntax
   - Shows any structural issues

5. **Solve Equation**
   - Click "Solve Equation" button
   - System solves using SymPy
   - Displays complete solution with steps

6. **Review Results**
   - View the final answer
   - Read step-by-step explanation
   - Check warnings about common mistakes
   - Learn about trap areas in the equation

### Example Equations

**Linear Equation:**
```
2x + 5 = 15
```

**Quadratic Equation:**
```
x^2 - 5x + 6 = 0
```

**Polynomial Equation:**
```
2x^3 - 3x^2 + x - 2 = 0
```

**Equation with Brackets:**
```
2(x + 3) - 4 = 10
```

## 🔑 API Keys

### Google Gemini API (Optional)

For enhanced step-by-step explanations:

1. Go to [Google AI Studio](https://ai.google.dev)
2. Click "Get API Key"
3. Create a new API key
4. Add to `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

The app works without Gemini, using built-in step generation.

## ⚙️ Configuration

### Settings in Sidebar

**OCR Confidence Threshold**
- Default: 0.5 (50%)
- Adjust to require higher accuracy from OCR
- Higher values = fewer results but more accurate

**Show Image Statistics**
- Displays image height, width, and intensity details
- Useful for debugging image quality issues

**Show LaTeX Code**
- Displays the LaTeX code for equations
- Helpful for understanding mathematical formatting

## 🐛 Error Handling

The app handles:
- **Invalid Images**: Detects empty or corrupted images
- **OCR Failures**: Gracefully handles OCR limits
- **Parse Errors**: Validates equation syntax
- **Solver Errors**: Catches division by zero and complex cases
- **API Errors**: Handles Gemini connectivity issues

All errors are logged to `math_tutor.log`

## 📊 Output Examples

### Linear Equation Solution
```
Original Equation: 2x + 5 = 15
Step 1: Subtract 5 from both sides
        2x = 10
Step 2: Divide both sides by 2
        x = 5
Final Answer: x = 5
```

### Quadratic Equation Solution
```
Original Equation: x² - 5x + 6 = 0
Step 1: Factor the expression
        (x - 2)(x - 3) = 0
Step 2: Apply zero product property
        x - 2 = 0  or  x - 3 = 0
Final Answer: x = 2, 3
```

## 🎨 Features Detail

### Image Preprocessing Pipeline
1. **Resize** - Optimize image size
2. **Grayscale** - Convert to single channel
3. **Denoise** - Remove noise using bilateral filter
4. **Contrast Adjustment** - Enhance text visibility
5. **Adaptive Threshold** - Convert to binary for better OCR

### Equation Validation
- Parentheses balance check
- Equals sign verification
- Character validation
- Structure analysis

### Mistake Detection Types
1. **Sign Errors** - Wrong positive/negative signs
2. **Distribution Errors** - Missing terms in expansion
3. **Division Errors** - Incorrect fraction handling
4. **Variable Loss** - Losing variables in operations
5. **Bracket Errors** - Missing or misplaced brackets
6. **Perfect Square Errors** - Forgetting 2ab term

## 🔧 Development

### Adding New Features

**To add a new service:**
1. Create file in `services/` directory
2. Follow the class-based structure
3. Add type hints and docstrings
4. Update logger calls
5. Test thoroughly

**To modify UI:**
1. Edit `app.py`
2. Use Streamlit components
3. Maintain responsive layout
4. Test on different screen sizes

### Running Tests

```bash
# Test with different equation types
python -m pytest tests/ -v
```

### Code Quality

- **Type Hints**: All functions have type annotations
- **Docstrings**: Comprehensive module and function documentation
- **Logging**: Detailed event tracking
- **Error Handling**: Graceful failure modes

## 📝 Logging

Logs are saved to `math_tutor.log` with:
- Timestamp
- Log level (INFO, WARNING, ERROR, DEBUG)
- Module name
- Message

View logs:
```bash
tail -f math_tutor.log
```

## 🚨 Troubleshooting

### OCR Low Confidence
- Improve image quality
- Ensure good lighting when photographing
- Use clear, printed equations
- Manually correct if needed

### Equation Won't Parse
- Check for balanced parentheses
- Ensure equation has exactly one `=`
- Verify operator syntax (+, -, *, /)
- Use ^ for powers: `x^2` not `x2`

### Gemini Not Working
- Verify API key is correct
- Check internet connection
- Ensure API key has appropriate permissions
- Check API usage limits at Google Cloud

### Slow Performance
- First run downloads OCR models (~100MB)
- Reduce image size
- Close other applications
- Use GPU if available (modify code)

## 📄 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review error messages in `math_tutor.log`
- Ensure all dependencies are installed correctly

## 🎉 Features Roadmap

- [ ] Handwriting recognition improvements
- [ ] Multi-variable equation support
- [ ] Graphing equation solutions
- [ ] Mobile application
- [ ] Real-time web-based version
- [ ] Support for more language inputs
- [ ] Integration with learning platforms

## 📚 Resources

- [SymPy Documentation](https://docs.sympy.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [EasyOCR Documentation](https://github.com/JaidedAI/EasyOCR)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Google Gemini API](https://ai.google.dev/)

---

**Made with ❤️ for students learning algebra**