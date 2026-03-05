# Configuration Guide - AI Math Tutor

## Environment Variables (.env)

Copy `.env.example` to `.env` and configure:

### Required Variables

```bash
# Google Gemini API Key (Optional but recommended)
# Get free key from: https://ai.google.dev
GEMINI_API_KEY=your_api_key_here
```

### Optional Variables

```bash
# Logging Level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# OCR Model Language (e.g., 'en', 'es', 'fr')
OCR_LANGUAGE=en

# Image Upload Directory
UPLOAD_DIR=./uploads

# Log File Path
LOG_FILE=./math_tutor.log

# Enable GPU (true/false)
USE_GPU=false

# Streamlit Port
STREAMLIT_PORT=8501

# Server Host
STREAMLIT_HOST=localhost
```

---

## Streamlit Configuration

Create `~/.streamlit/config.toml` for persistent settings:

```toml
[theme]
primaryColor = "#0066cc"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true
toolbarMode = "minimal"
showSidebarNavigation = true

[logger]
level = "info"
messageFormat = "%(asctime)s - %(message)s"

[server]
port = 8501
headless = false
runOnSave = true
maxUploadSize = 200

[browser]
gatherUsageStats = false
serverAddress = "localhost"
```

Save location:
- **Linux/Mac**: `~/.streamlit/config.toml`
- **Windows**: `%userprofile%/.streamlit/config.toml`

---

## Application Settings

Settings available in the Streamlit UI sidebar:

### 1. OCR Confidence Threshold
- **Range**: 0.0 - 1.0
- **Default**: 0.5
- **Description**: Minimum confidence required for OCR results
- **Use case**: Set higher (0.8) for critical applications, lower (0.3) for quick results

### 2. Show Image Statistics
- **Options**: Enable/Disable
- **Default**: Disabled
- **Shows**: Image dimensions, intensity metrics
- **Use case**: Debugging image quality issues

### 3. Show LaTeX Code
- **Options**: Enable/Disable
- **Default**: Disabled
- **Shows**: LaTeX source for equations
- **Use case**: Learning LaTeX formatting

---

## System Configuration

### Python Version
- **Minimum**: Python 3.8
- **Recommended**: Python 3.10+
- **Check**: `python --version`

### Virtual Environment
```bash
# Create
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Dependencies
All in `requirements.txt`:
- streamlit >= 1.28.0
- pillow >= 10.0.0
- numpy >= 1.24.0
- opencv-python >= 4.8.0
- easyocr >= 1.6.0
- sympy >= 1.12
- python-dotenv >= 1.0.0
- google-generativeai >= 0.3.0

Install:
```bash
pip install -r requirements.txt
```

---

## GPU Configuration

### Enable CUDA for EasyOCR

**Step 1: Install NVIDIA Drivers**
```bash
ubuntu-drivers devices
sudo apt install nvidia-driver-530

# Verify
nvidia-smi
```

**Step 2: Install CUDA Toolkit**
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-repo-ubuntu2004_11.8.0-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2004_11.8.0-1_amd64.deb
sudo apt update
sudo apt install cuda-11-8
```

**Step 3: Install cuDNN**
- Download from NVIDIA website
- Extract and copy to CUDA directory

**Step 4: Configure Python**

In `services/ocr_service.py`:
```python
self.reader = easyocr.Reader(self.languages, gpu=True)
```

Set environment variable:
```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64
```

---

## Docker Configuration

### Build Arguments

```dockerfile
ARG PYTHON_VERSION=3.10
ARG EASYOCR_CACHE=/root/.EasyOCR
ARG GPU_SUPPORT=false
```

### Runtime Environment

```bash
# Without GPU
docker build -t ai-math-tutor .

# With GPU
docker build -t ai-math-tutor-gpu --build-arg GPU_SUPPORT=true .
```

### Volume Mounts

```bash
docker run -v $(pwd)/logs:/app/logs \
           -v $(pwd)/uploads:/app/uploads \
           ai-math-tutor
```

---

## API Configuration

### Google Gemini Settings

```python
# In services/step_generator.py
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel(
    'gemini-pro',
    safety_settings=[...]  # Optional
)
```

### Request Timeouts

```python
# Default: 30 seconds
import socket
socket.setdefaulttimeout(30)
```

### Retry Logic

```python
from tenacity import retry, wait_exponential

@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def call_api_with_retry():
    pass
```

---

## Logging Configuration

### Log Levels

| Level | Description | When to use |
|-------|-------------|------------|
| DEBUG | Detailed info | Development |
| INFO | General info | Production |
| WARNING | Warning messages | Watch for issues |
| ERROR | Error messages | Critical problems |

### Configure in Code

```python
import logging

# Set level
logging.getLogger().setLevel(logging.DEBUG)

# Or via environment
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logging.getLogger().setLevel(LOG_LEVEL)
```

### Log Rotation

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'math_tutor.log',
    maxBytes=10_000_000,  # 10MB
    backupCount=5
)
```

---

## Performance Configuration

### Image Processing

```python
# In utils/image_preprocess.py

# Resize limits
MAX_WIDTH = 1200
MAX_HEIGHT = 800

# Noise reduction strength
BILATERAL_DIAMETER = 9
BILATERAL_SIGMA_COLOR = 75
BILATERAL_SIGMA_SPACE = 75
```

### OCR Settings

```python
# In services/ocr_service.py

# Languages (affects model download)
LANGUAGES = ['en']  # Single = smaller, faster

# GPU usage
USE_GPU = False  # Change to True with CUDA
```

### SymPy Timeout

```python
from sympy import symbols, solve
from signal import alarm, SIGALRM

# Set timeout in seconds
def timeout_handler(signum, frame):
    raise TimeoutError("Solving took too long")

signal.signal(SIGALRM, timeout_handler)
signal.alarm(5)  # 5 second timeout

try:
    solutions = solve(equation, x)
finally:
    signal.alarm(0)
```

---

## Security Configuration

### Input Validation

```python
# Equation length limit
MAX_EQUATION_LENGTH = 1000

# Allowed characters
ALLOWED_CHARS = r'^[a-zA-Z0-9\+\-\*\/\=\(\)\[\]\.^,\s]+$'

# Rate limiting (requests per minute)
RATE_LIMIT = 60
```

### API Key Protection

```python
# In .env (don't commit!)
GEMINI_API_KEY=sk-...

# In code
key = os.getenv('GEMINI_API_KEY')
if not key:
    logger.warning("GEMINI_API_KEY not set")
```

### CORS Configuration

```python
# For web API version
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com"
]
```

---

## Integration Configuration

### Database Setup (Optional for future)

```python
import sqlalchemy

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'sqlite:///./math_tutor.db'
)

engine = sqlalchemy.create_engine(DATABASE_URL)
```

### Email Notifications (Optional)

```python
import smtplib

EMAIL_SERVER = os.getenv('EMAIL_SERVER')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
```

### Slack Notifications (Optional)

```python
import slack
from slack_sdk import WebClient

client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))

def notify_error(error_msg):
    client.chat_postMessage(
        channel='#errors',
        text=f'Error: {error_msg}'
    )
```

---

## Monitoring Configuration

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram

ocr_attempts = Counter('ocr_attempts_total', 'OCR attempts')
solve_duration = Histogram('solve_duration_seconds', 'Solve time')
```

### Datadog APM

```python
from ddtrace import tracer, patch_all

patch_all()

@tracer.wrap()
def solve_equation(eq):
    pass
```

---

## Feature Flags

Enable/disable features:

```python
# In app.py or config.py
FEATURES = {
    'gemini_enabled': os.getenv('GEMINI_API_KEY') is not None,
    'gpu_enabled': os.getenv('USE_GPU', 'false').lower() == 'true',
    'detailed_logs': os.getenv('LOG_LEVEL') == 'DEBUG',
    'image_stats': os.getenv('SHOW_IMAGE_STATS', 'false').lower() == 'true',
}

if FEATURES['gemini_enabled']:
    # Use Gemini features
    pass
```

---

## Performance Tuning

### Cache Settings

```python
# LRU Cache for expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(param):
    pass
```

### Batch Processing

```python
BATCH_SIZE = 10  # Process equations in batches
MAX_WAIT_TIME = 5  # Max seconds to wait before processing
```

### Memory Limits

```bash
# Linux: Limit memory usage
python -c "import resource; resource.setrlimit(resource.RLIMIT_AS, (4*1024**3, 4*1024**3))" && streamlit run app.py
```

---

## Typical Configurations

### Development Setup
```bash
LOG_LEVEL=DEBUG
GEMINI_API_KEY=<your_dev_key>
USE_GPU=false
STREAMLIT_LOGGER_LEVEL=debug
```

### Production Setup
```bash
LOG_LEVEL=INFO
GEMINI_API_KEY=<your_prod_key>
USE_GPU=true
STREAMLIT_LOGGER_LEVEL=warning
```

### Testing Setup
```bash
LOG_LEVEL=DEBUG
GEMINI_API_KEY=<test_key_or_empty>
USE_GPU=false
STREAMLIT_LOGGER_LEVEL=debug
```

---

## Verification

Verify configuration:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Check all required settings
required = ['GEMINI_API_KEY']
for var in required:
    value = os.getenv(var)
    if not value:
        print(f"WARNING: {var} not set")
    else:
        print(f"✓ {var} configured")
```

---

## Troubleshooting Configuration

### Issues and Solutions

**Q: OCR very slow**
- A: Try `USE_GPU=true` or reduce image size in preprocessing

**Q: Gemini not working**
- A: Verify `GEMINI_API_KEY` is correct and has usage available

**Q: Out of memory**
- A: Reduce `MAX_WIDTH/MAX_HEIGHT` or use GPU

**Q: Port already in use**
- A: Change `STREAMLIT_PORT` in config or kill process using port

**Q: Logs filling disk**
- A: Enable log rotation or configure `LogLevel=WARNING`

---

**Configuration complete! Start the app with:**
```bash
streamlit run app.py
```
