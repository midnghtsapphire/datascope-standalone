# DataScope Enhanced - Installation Guide

This comprehensive guide will walk you through installing and setting up DataScope Enhanced on various platforms and environments.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Installation](#quick-installation)
3. [Detailed Installation](#detailed-installation)
4. [Platform-Specific Instructions](#platform-specific-instructions)
5. [Docker Installation](#docker-installation)
6. [Cloud Deployment](#cloud-deployment)
7. [Configuration](#configuration)
8. [Verification](#verification)
9. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Operating System**: Linux (Ubuntu 18.04+), macOS (10.14+), Windows 10+
- **Python**: 3.11 or higher
- **Memory**: 4 GB RAM
- **Storage**: 10 GB free space
- **Network**: Internet connection for data collection

### Recommended Requirements
- **Operating System**: Linux (Ubuntu 20.04+), macOS (12.0+), Windows 11
- **Python**: 3.11+
- **Memory**: 8 GB RAM
- **Storage**: 50 GB free space (for data caching)
- **CPU**: Multi-core processor for parallel processing

### Browser Automation Requirements
- **Chrome Browser**: Latest stable version
- **ChromeDriver**: Compatible with installed Chrome version
- **Display**: For non-headless mode (development/debugging)

## Quick Installation

For users who want to get started quickly:

```bash
# Clone the repository
git clone https://github.com/your-org/datascope-enhanced.git
cd datascope-enhanced

# Run the quick setup script
chmod +x scripts/quick_setup.sh
./scripts/quick_setup.sh

# Test the installation
python enhanced_main.py cybersecurity --test
```

## Detailed Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/datascope-enhanced.git
cd datascope-enhanced
```

### Step 2: Create Virtual Environment

#### Using venv (Recommended)
```bash
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Using conda
```bash
conda create -n datascope-enhanced python=3.11
conda activate datascope-enhanced
```

### Step 3: Install Python Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install optional dependencies for full functionality
pip install -r requirements-optional.txt
```

### Step 4: Install Browser Automation Dependencies

#### Automatic Installation (Recommended)
```bash
python scripts/setup_browser.py
```

#### Manual Installation

**Install Chrome Browser:**

*Ubuntu/Debian:*
```bash
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google.list
sudo apt update
sudo apt install google-chrome-stable
```

*macOS:*
```bash
brew install --cask google-chrome
```

*Windows:*
Download and install from [Google Chrome](https://www.google.com/chrome/)

**Install ChromeDriver:**

*Automatic (using webdriver-manager):*
```python
from webdriver_manager.chrome import ChromeDriverManager
ChromeDriverManager().install()
```

*Manual:*
1. Check Chrome version: `google-chrome --version`
2. Download matching ChromeDriver from [ChromeDriver Downloads](https://chromedriver.chromium.org/)
3. Extract and place in PATH or project directory

### Step 5: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (see Configuration section)
nano .env
```

### Step 6: Initialize Database and Cache

```bash
# Create necessary directories
mkdir -p cache reports data logs

# Initialize database (if using database features)
python scripts/init_database.py

# Test configuration
python scripts/test_config.py
```

## Platform-Specific Instructions

### Ubuntu/Debian Linux

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip git curl wget

# Install additional dependencies for browser automation
sudo apt install -y libnss3-dev libgconf-2-4 libxss1 libappindicator1 libindicator7

# Install Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google.list
sudo apt update
sudo apt install -y google-chrome-stable

# Continue with standard installation
git clone https://github.com/your-org/datascope-enhanced.git
cd datascope-enhanced
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### CentOS/RHEL/Fedora

```bash
# Install system dependencies
sudo dnf install -y python3.11 python3-pip git curl wget

# Install Chrome
sudo dnf install -y https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm

# Continue with standard installation
```

### macOS

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Install Chrome
brew install --cask google-chrome

# Continue with standard installation
git clone https://github.com/your-org/datascope-enhanced.git
cd datascope-enhanced
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows

#### Using PowerShell (Recommended)

```powershell
# Install Python 3.11 from Microsoft Store or python.org

# Install Git
winget install Git.Git

# Clone repository
git clone https://github.com/your-org/datascope-enhanced.git
cd datascope-enhanced

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Chrome (if not already installed)
winget install Google.Chrome
```

#### Using WSL (Windows Subsystem for Linux)

```bash
# Enable WSL and install Ubuntu
wsl --install

# Follow Ubuntu installation instructions within WSL
```

## Docker Installation

### Using Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/your-org/datascope-enhanced.git
cd datascope-enhanced

# Copy environment file
cp .env.example .env

# Edit .env file with your configuration
nano .env

# Build and start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f datascope
```

### Using Docker Only

```bash
# Build the image
docker build -t datascope-enhanced .

# Run the container
docker run -d \
  --name datascope \
  -p 5000:5000 \
  -v $(pwd)/cache:/app/cache \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  datascope-enhanced

# Check logs
docker logs -f datascope
```

### Docker Compose Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  datascope:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./cache:/app/cache
      - ./reports:/app/reports
      - ./data:/app/data
      - ./logs:/app/logs
    env_file:
      - .env
    restart: unless-stopped
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: datascope
      POSTGRES_USER: datascope
      POSTGRES_PASSWORD: your_password_here
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - datascope
    restart: unless-stopped

volumes:
  redis_data:
  postgres_data:
```

## Cloud Deployment

### AWS EC2

```bash
# Launch EC2 instance (Ubuntu 20.04 LTS)
# Connect via SSH

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and deploy
git clone https://github.com/your-org/datascope-enhanced.git
cd datascope-enhanced
cp .env.example .env
# Edit .env file
docker-compose up -d
```

### Google Cloud Platform

```bash
# Create VM instance
gcloud compute instances create datascope-enhanced \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --machine-type=e2-standard-4 \
  --boot-disk-size=50GB

# SSH into instance
gcloud compute ssh datascope-enhanced

# Follow standard installation or Docker installation
```

### Azure

```bash
# Create VM
az vm create \
  --resource-group myResourceGroup \
  --name datascope-enhanced \
  --image UbuntuLTS \
  --size Standard_D4s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys

# SSH into VM
az vm run-command invoke \
  --resource-group myResourceGroup \
  --name datascope-enhanced \
  --command-id RunShellScript \
  --scripts "curl -fsSL https://get.docker.com | sh"
```

### Kubernetes Deployment

```yaml
# datascope-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: datascope-enhanced
spec:
  replicas: 3
  selector:
    matchLabels:
      app: datascope-enhanced
  template:
    metadata:
      labels:
        app: datascope-enhanced
    spec:
      containers:
      - name: datascope
        image: datascope-enhanced:latest
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: datascope-secrets
              key: database-url
        volumeMounts:
        - name: cache-volume
          mountPath: /app/cache
        - name: reports-volume
          mountPath: /app/reports
      volumes:
      - name: cache-volume
        persistentVolumeClaim:
          claimName: datascope-cache-pvc
      - name: reports-volume
        persistentVolumeClaim:
          claimName: datascope-reports-pvc
```

## Configuration

### Basic Configuration

Edit the `.env` file with your settings:

```bash
# Core settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Directories
CACHE_DIRECTORY=./cache
OUTPUT_DIRECTORY=./reports

# Browser automation
HEADLESS_BROWSER=true
CHROME_DRIVER_PATH=/usr/local/bin/chromedriver

# API settings
API_HOST=0.0.0.0
API_PORT=5000
```

### Advanced Configuration

#### Database Configuration

**SQLite (Default):**
```bash
DATABASE_URL=sqlite:///datascope.db
```

**PostgreSQL:**
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/datascope
```

#### Redis Configuration

```bash
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your_redis_password
```

#### Social Media Credentials

```bash
# Add your social media credentials
LEMON8_USERNAME=your_username
LEMON8_PASSWORD=your_password
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

### Security Configuration

```bash
# Generate secure keys
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env
API_SECRET_KEY=your_generated_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
ENCRYPTION_KEY=your_encryption_key
```

## Verification

### Test Installation

```bash
# Test basic functionality
python enhanced_main.py --test

# Test specific domain
python enhanced_main.py cybersecurity --test

# Test browser automation
python scripts/test_browser.py

# Test API endpoints
python scripts/test_api.py
```

### Run Health Checks

```bash
# Check system status
python scripts/health_check.py

# Check dependencies
python scripts/check_dependencies.py

# Check configuration
python scripts/validate_config.py
```

### Verify Services

```bash
# Check if API is running
curl http://localhost:5000/api/v1/status

# Check browser automation
python -c "from browser_automation import BrowserDataCollector; print('Browser automation OK')"

# Check data collection
python -c "from prompt_engine import PromptEngine; engine = PromptEngine(); print('Prompt engine OK')"
```

## Troubleshooting

### Common Issues

#### Chrome/ChromeDriver Issues

**Problem**: ChromeDriver version mismatch
```bash
# Solution: Update ChromeDriver
pip install --upgrade webdriver-manager
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
```

**Problem**: Chrome not found
```bash
# Solution: Install Chrome or set path
export CHROME_BIN=/usr/bin/google-chrome
# Or add to .env file
echo "CHROME_BIN=/usr/bin/google-chrome" >> .env
```

#### Permission Issues

**Problem**: Permission denied errors
```bash
# Solution: Fix permissions
sudo chown -R $USER:$USER ./cache ./reports ./data
chmod -R 755 ./cache ./reports ./data
```

#### Memory Issues

**Problem**: Out of memory errors
```bash
# Solution: Increase swap space or reduce collection size
# Add to .env:
MAX_ITEMS_PER_COLLECTION=100
MAX_MEMORY_USAGE_MB=1024
```

#### Network Issues

**Problem**: Connection timeouts
```bash
# Solution: Increase timeouts
# Add to .env:
REQUEST_TIMEOUT=60
COLLECTION_TIMEOUT_SECONDS=600
```

### Debug Mode

Enable debug mode for troubleshooting:

```bash
# Set in .env
DEBUG=true
LOG_LEVEL=DEBUG

# Or run with debug flag
python enhanced_main.py --debug cybersecurity
```

### Log Analysis

```bash
# View application logs
tail -f logs/datascope_enhanced.log

# View error logs
grep ERROR logs/datascope_enhanced.log

# View browser automation logs
tail -f logs/browser_automation.log
```

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Look in the `logs/` directory for error messages
2. **Search issues**: Check [GitHub Issues](https://github.com/your-org/datascope-enhanced/issues)
3. **Create an issue**: Provide logs, system info, and steps to reproduce
4. **Join discussions**: Use [GitHub Discussions](https://github.com/your-org/datascope-enhanced/discussions)
5. **Contact support**: Email support@datascope-enhanced.com

### System Information Script

Create a system info script for support:

```bash
# scripts/system_info.py
import platform
import sys
import subprocess

def get_system_info():
    info = {
        'platform': platform.platform(),
        'python_version': sys.version,
        'chrome_version': get_chrome_version(),
        'chromedriver_version': get_chromedriver_version()
    }
    return info

# Run: python scripts/system_info.py
```

## Next Steps

After successful installation:

1. **Read the User Guide**: Learn how to use DataScope Enhanced effectively
2. **Configure Domains**: Set up domain-specific configurations
3. **Set Up Automation**: Configure scheduled data collection
4. **Explore API**: Try the REST API endpoints
5. **Customize Reports**: Create custom report templates
6. **Monitor Performance**: Set up monitoring and alerting

---

**Congratulations!** You have successfully installed DataScope Enhanced. Start collecting intelligence data across multiple domains with ease!

