# Production Deployment Guide - AI Math Tutor

## Overview

Guide for deploying AI Math Tutor in production environments.

---

## Pre-Deployment Checklist

- [ ] All dependencies installed
- [ ] .env configured with API keys
- [ ] Log file location configured
- [ ] Image upload directory permissions set
- [ ] GPU drivers installed (if using GPU)
- [ ] Sufficient disk space (2GB+ for models)
- [ ] Python 3.8+ installed
- [ ] Virtual environment activated

---

## Local Development Setup

### 1. Environment Setup

```bash
# Clone repository
git clone <repo-url> ai-math-tutor
cd ai-math-tutor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

Add:
```
GEMINI_API_KEY=your_api_key_here
```

### 3. Run Application

```bash
# Development
streamlit run app.py

# With custom port
streamlit run app.py --server.port 8000

# Headless mode (server)
streamlit run app.py --server.headless true
```

---

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create non-root user
RUN useradd -m streamlit
USER streamlit

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "app.py", "--server.headless", "true"]
```

### 2. Build Docker Image

```bash
# Build
docker build -t ai-math-tutor:latest .

# Run container
docker run -p 8501:8501 \
  -v $(pwd):/app \
  -e GEMINI_API_KEY=your_key \
  ai-math-tutor:latest

# With GPU support
docker run --gpus all -p 8501:8501 ai-math-tutor:latest
```

### 3. Docker Compose (Multiple Services)

```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run:
```bash
docker-compose up -d
```

---

## Cloud Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. New app → Deploy from GitHub
4. Select repo and app.py
5. Set environment variables in Advanced Settings

```
GEMINI_API_KEY=your_key
```

### AWS EC2

```bash
# Launch EC2 instance (Ubuntu 20.04+)
# Connect to instance

# Install Python and dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv

# Clone and setup
git clone <repo-url>
cd ai-math-tutor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/math-tutor.service
```

Service file:
```ini
[Unit]
Description=AI Math Tutor
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-math-tutor
Environment="PATH=/home/ubuntu/ai-math-tutor/venv/bin"
Environment="GEMINI_API_KEY=your_key"
ExecStart=/home/ubuntu/ai-math-tutor/venv/bin/streamlit run app.py --server.port 8501

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl daemon-reload
sudo systemctl start math-tutor
sudo systemctl enable math-tutor
```

### Google Cloud Run

```bash
# Build Docker image
docker build -t ai-math-tutor .

# Push to GCR
docker tag ai-math-tutor gcr.io/PROJECT_ID/ai-math-tutor
docker push gcr.io/PROJECT_ID/ai-math-tutor

# Deploy to Cloud Run
gcloud run deploy ai-math-tutor \
  --image gcr.io/PROJECT_ID/ai-math-tutor \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=your_key \
  --allow-unauthenticated
```

---

## Performance Optimization

### 1. GPU Acceleration (CUDA)

```python
# In ocr_service.py, change:
self.reader = easyocr.Reader(self.languages, gpu=True)

# Prerequisites:
# - NVIDIA GPU with CUDA support
# - CUDA Toolkit installed
# - cuDNN installed
```

### 2. Image Caching

```python
import streamlit as st

@st.cache_resource
def load_ocr_model():
    from services.ocr_service import OCRService
    return OCRService()

ocr = load_ocr_model()
```

### 3. Model Optimization

```bash
# Install quantized models if available
pip install onnx onnxruntime

# Use in ocr_service.py for faster inference
```

### 4. Request Batching

For multiple equations:
```python
def process_batch(equations):
    results = []
    for eq in equations:
        result = process_single(eq)
        results.append(result)
    return results
```

---

## Monitoring & Logging

### 1. Log Configuration

```python
# In utils/logger.py
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logger.setLevel(LOG_LEVEL)
```

### 2. View Logs

```bash
# Real-time logs
tail -f math_tutor.log

# With grep
grep "ERROR" math_tutor.log

# Count entries
wc -l math_tutor.log

# Archive old logs
gzip math_tutor.log
```

### 3. Monitoring Setup

For AWS CloudWatch:
```python
import logging
import watchtower

logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())
```

For Datadog:
```python
from datadog import initialize, statsd

initialize(options={"api_key": "YOUR_API_KEY"})

@statsd.timed('math_tutor.equation.solve')
def solve_equation(eq):
    # solve logic
    pass
```

---

## Security Best Practices

### 1. API Key Management

```bash
# Use AWS Secrets Manager
import boto3

def get_gemini_key():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId='gemini-api-key')
    return response['SecretString']
```

### 2. Input Validation

```python
# In app.py - already implemented
# Validates equation syntax and structure
# Prevents malicious input

def validate_input(equation: str) -> bool:
    # Check length
    if len(equation) > 1000:
        return False
    # Check characters
    if not re.match(r'^[a-zA-Z0-9\+\-\*\/\=\(\)\[\]\.^,\s]+$', equation):
        return False
    return True
```

### 3. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.route('/solve')
@limiter.limit("10/minute")
def solve():
    pass
```

### 4. CORS Headers

For API deployment:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Backup & Disaster Recovery

### 1. Backup Strategy

```bash
# Backup logs daily
0 2 * * * tar -czf mat_math_tutor_logs_$(date +%Y%m%d).tar.gz /app/logs/

# Upload to S3
aws s3 cp math_tutor_logs_*.tar.gz s3://backup-bucket/
```

### 2. Automated Logs Cleanup

```bash
# Delete logs older than 30 days
find /app/logs -name "*.log" -mtime +30 -delete
```

---

## Capacity Planning

### 1. System Requirements

| Component | Minimum | Recommended |
|-----------|---------|------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4GB | 8GB+ |
| Storage | 2GB | 10GB+ |
| Network | 1Mbps | 10Mbps+ |

### 2. Concurrent Users

- **1-10 users**: Single instance, 4GB RAM
- **10-50 users**: 2 instances, load balancer
- **50+ users**: Auto-scaling group

### 3. Load Balancing

```bash
# Using nginx
upstream app {
    server localhost:8501;
    server localhost:8502;
}

server {
    listen 80;
    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
    }
}
```

---

## Maintenance

### 1. Update Dependencies

```bash
# Check for updates
pip list --outdated

# Update package
pip install --upgrade package_name

# Update all
pip install --upgrade -r requirements.txt
```

### 2. Health Checks

```python
@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': check_models(),
        'api_available': check_api()
    }
```

### 3. Rolling Updates

```bash
# Stop container 1, update, restart
docker stop app-1
docker pull ai-math-tutor:latest
docker run ... ai-math-tutor:latest

# Container 2 still serves traffic
# No downtime
```

---

## Testing Before Deployment

### 1. Unit Tests

```bash
pytest tests/ -v
```

### 2. Load Testing

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8501

# Using Locust
locust -f locustfile.py -u 100 -r 10 -t 60s
```

### 3. Integration Testing

```python
def test_full_workflow():
    # Test OCR → Parse → Solve → Steps
    image = load_test_image()
    result = full_pipeline(image)
    assert result['success'] == True
```

---

## Cost Optimization

### 1. Use Free Tier Services

- Google Gemini: Free tier for development
- Streamlit Cloud: Free deployment
- GitHub: Free repository hosting

### 2. Optimize Resources

- Use lightweight base images
- Cache frequently used models
- Limit concurrent requests
- Clean up temp files

### 3. Cost Estimation

| Service | Cost |
|---------|------|
| Gemini API | Free/Pay-as-you-go |
| EC2 (t3.medium) | $0.04/hour |
| Streamlit Cloud | Free for public apps |
| Cloud Run | Free tier + $0.00002400/GB-second |

---

## Troubleshooting Deployment

### Port Already in Use

```bash
# Linux/Mac
lsof -i :8501
kill -9 <PID>

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Out of Memory

```bash
# Increase swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Slow OCR

```bash
# Use GPU
# Or reduce image resolution
# Or use lighter model

from services.ocr_service import OCRService
ocr = OCRService()
ocr.reader = easyocr.Reader(['en'], gpu=True)
```

---

## Monitoring Dashboard

For real-time monitoring, integrate with:
- Grafana (visualization)
- Prometheus (metrics)
- NewRelic (APM)
- Datadog (monitoring)

```bash
# Install Prometheus client
pip install prometheus-client
```

---

## Scheduled Maintenance

### Recommended Schedule

**Daily**: Monitor logs, check health
**Weekly**: Update security patches
**Monthly**: Performance review, cleanup
**Quarterly**: Capacity planning, cost review

---

## Getting Help

- Check logs: `tail -f math_tutor.log`
- Review deployment guide
- Check cloud provider documentation
- Contact support with logs and configuration

---

**Ready to deploy! 🚀**
