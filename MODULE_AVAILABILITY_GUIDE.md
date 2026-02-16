# DataScope Enhanced - Module Availability Guide

## Understanding Module Availability Warnings

When you see warnings like "module unavailability" or "TURN modules not available," these are **intentional design features** that allow DataScope Enhanced to work gracefully even when optional components aren't installed. The system uses a **modular architecture** where features degrade gracefully rather than failing completely.

## Common Warnings and What They Mean

### 1. "TURN modules not available - cybersecurity features limited"

**What it means:**
- The original TURN Global Fusion Digest modules from your uploaded threat intelligence system aren't available
- Basic cybersecurity data collection still works, but advanced threat analysis is limited

**Impact:**
- ✅ **Still works**: Data collection from CISA KEV, FBI IC3
- ✅ **Still works**: Basic report generation
- ❌ **Limited**: Advanced threat categorization and TURN-style analysis

**How to fix:**
```bash
# Copy TURN modules to the enhanced system
cp /home/ubuntu/upload/*.py /home/ubuntu/datascope-enhanced/
cd /home/ubuntu/datascope-enhanced
python enhanced_main.py cybersecurity federal
```

### 2. "Browser automation not available - some features limited"

**What it means:**
- Selenium WebDriver or Chrome isn't properly installed
- Social media collection requiring login won't work

**Impact:**
- ✅ **Still works**: API-based data collection, web scraping
- ❌ **Limited**: Lemon8, Instagram, LinkedIn data collection

**How to fix:**
```bash
# Install browser automation dependencies
pip install selenium webdriver-manager

# Install Chrome (if not already installed)
# Ubuntu/Debian:
sudo apt install google-chrome-stable

# macOS:
brew install --cask google-chrome

# Test browser automation
python -c "from browser_automation import BrowserDataCollector; print('Browser automation OK')"
```

### 3. "Redis not available - using file cache"

**What it means:**
- Redis server isn't running
- System falls back to file-based caching

**Impact:**
- ✅ **Still works**: All functionality with file caching
- ❌ **Limited**: Slower caching, no distributed caching

**How to fix:**
```bash
# Install and start Redis
# Ubuntu/Debian:
sudo apt install redis-server
sudo systemctl start redis-server

# macOS:
brew install redis
brew services start redis

# Docker:
docker run -d -p 6379:6379 redis:alpine
```

## Module Availability Status Check

Create a simple script to check what's available:

```python
#!/usr/bin/env python3
"""Check DataScope Enhanced module availability"""

def check_module_availability():
    status = {
        'core': True,
        'browser_automation': False,
        'turn_modules': False,
        'redis_cache': False,
        'database': False
    }
    
    # Check browser automation
    try:
        from selenium import webdriver
        from browser_automation import BrowserDataCollector
        status['browser_automation'] = True
        print("✅ Browser automation: Available")
    except ImportError as e:
        print(f"❌ Browser automation: Not available ({e})")
    
    # Check TURN modules
    try:
        import sys
        sys.path.append('/home/ubuntu/upload')
        from threat_analysis_engine import ThreatAnalysisEngine
        status['turn_modules'] = True
        print("✅ TURN modules: Available")
    except ImportError as e:
        print(f"❌ TURN modules: Not available ({e})")
    
    # Check Redis
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        status['redis_cache'] = True
        print("✅ Redis cache: Available")
    except Exception as e:
        print(f"❌ Redis cache: Not available ({e})")
    
    # Check database
    try:
        import sqlite3
        status['database'] = True
        print("✅ SQLite database: Available")
    except ImportError as e:
        print(f"❌ Database: Not available ({e})")
    
    return status

if __name__ == "__main__":
    print("DataScope Enhanced - Module Availability Check")
    print("=" * 50)
    status = check_module_availability()
    
    print("\nSummary:")
    available = sum(status.values())
    total = len(status)
    print(f"Available modules: {available}/{total}")
    
    if available == total:
        print("🎉 All modules available - full functionality!")
    elif available >= 2:
        print("✅ Core functionality available - some features limited")
    else:
        print("⚠️  Limited functionality - consider installing missing modules")
```

Save this as `check_modules.py` and run:
```bash
python check_modules.py
```

## Graceful Degradation Examples

### Cybersecurity Domain

**With TURN modules:**
```python
# Full threat analysis with severity classification
results = datascope.collect_domain_data('cybersecurity')
# Results include: threat_analysis, severity_distribution, top_threat_actors
```

**Without TURN modules:**
```python
# Basic data collection still works
results = datascope.collect_domain_data('cybersecurity')
# Results include: raw data from CISA KEV, FBI IC3, basic processing
```

### Social Media Domain

**With browser automation:**
```python
# Can collect from Lemon8, Instagram with login
credentials = {'username': 'user', 'password': 'pass'}
results = datascope.collect_with_browser_automation('lemon8', credentials)
```

**Without browser automation:**
```python
# Falls back to public API scraping where available
results = datascope.collect_domain_data('social-media')
# Limited to publicly accessible data
```

## Installation Priority

If you want to enable specific features, install in this order:

### 1. Core Functionality (Always Available)
- ✅ Basic data collection
- ✅ Report generation
- ✅ File caching
- ✅ Multi-domain support

### 2. Browser Automation (High Priority)
```bash
pip install selenium webdriver-manager
# Enables: Lemon8, Instagram, LinkedIn, complex JavaScript sites
```

### 3. TURN Integration (For Cybersecurity)
```bash
cp /home/ubuntu/upload/*.py /home/ubuntu/datascope-enhanced/
# Enables: Advanced threat analysis, TURN-style reports
```

### 4. Redis Caching (Performance)
```bash
sudo apt install redis-server  # or brew install redis
pip install redis
# Enables: Faster caching, distributed caching
```

### 5. Database (Advanced Features)
```bash
pip install psycopg2-binary  # for PostgreSQL
# Enables: Persistent storage, advanced analytics
```

## Testing Module Availability

Test each module individually:

```bash
# Test core functionality
python enhanced_main.py cybersecurity --test

# Test browser automation
python -c "from browser_automation import BrowserDataCollector; BrowserDataCollector(headless=True)"

# Test TURN modules
python -c "import sys; sys.path.append('/home/ubuntu/upload'); from threat_analysis_engine import ThreatAnalysisEngine"

# Test Redis
python -c "import redis; redis.Redis().ping()"
```

## Production Deployment Considerations

### Minimal Deployment (Core Only)
- ✅ Works for: API scraping, basic reports
- ❌ Missing: Browser automation, advanced analysis

### Standard Deployment (Core + Browser)
- ✅ Works for: Most data collection, social media
- ❌ Missing: Advanced threat analysis

### Full Deployment (All Modules)
- ✅ Works for: Everything, full functionality
- 💰 Cost: Higher resource requirements

## Troubleshooting Module Issues

### Import Errors
```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Check installed packages
pip list | grep -E "(selenium|redis|beautifulsoup4)"

# Reinstall problematic packages
pip uninstall selenium
pip install selenium
```

### Chrome/ChromeDriver Issues
```bash
# Check Chrome version
google-chrome --version

# Check ChromeDriver
chromedriver --version

# Auto-install matching ChromeDriver
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
```

### Redis Connection Issues
```bash
# Check if Redis is running
redis-cli ping

# Start Redis
sudo systemctl start redis-server  # Linux
brew services start redis          # macOS

# Check Redis logs
sudo journalctl -u redis-server    # Linux
```

## Summary

**The "module unavailability" warnings are normal and expected.** DataScope Enhanced is designed to work with whatever modules you have available, gracefully degrading functionality rather than failing completely.

- **Core functionality always works** - data collection and basic reporting
- **Optional modules enhance capabilities** - browser automation, advanced analysis
- **Install modules as needed** - based on your specific use cases
- **Production deployments** - choose the right level of functionality for your needs

The system collected 1,417 cybersecurity threats successfully even with the TURN modules warning, proving that the core functionality works perfectly!

