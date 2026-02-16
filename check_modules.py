#!/usr/bin/env python3
"""
DataScope Enhanced - Module Availability Checker
Check which optional modules are available and provide installation guidance
"""

import sys
import subprocess
import importlib.util
from pathlib import Path

def check_module_availability():
    """Check availability of all DataScope Enhanced modules"""
    
    print("DataScope Enhanced - Module Availability Check")
    print("=" * 60)
    
    status = {
        'core': True,
        'browser_automation': False,
        'turn_modules': False,
        'redis_cache': False,
        'database': False,
        'optional_analysis': False
    }
    
    # Check core modules (should always be available)
    try:
        from prompt_engine import PromptEngine
        print("✅ Core modules: Available")
        status['core'] = True
    except ImportError as e:
        print(f"❌ Core modules: Not available ({e})")
        status['core'] = False
    
    # Check browser automation
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        print("✅ Browser automation (Selenium): Available")
        
        # Check if Chrome is available
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options=options)
            driver.quit()
            print("✅ Chrome WebDriver: Available")
            status['browser_automation'] = True
        except Exception as e:
            print(f"⚠️  Chrome WebDriver: Issues ({e})")
            print("   Browser automation partially available")
            status['browser_automation'] = False
            
    except ImportError as e:
        print(f"❌ Browser automation: Not available ({e})")
        print("   Install with: pip install selenium webdriver-manager")
        status['browser_automation'] = False
    
    # Check TURN modules
    try:
        from turn_integration import turn_integration, ReportGenerator
        if turn_integration.is_available():
            print("✅ TURN modules: Available (with integration)")
            status['turn_modules'] = True
        else:
            print("⚠️  TURN modules: Partial (fallback mode)")
            print("   Some TURN features available via integration layer")
            status['turn_modules'] = True  # Partial availability
    except ImportError as e:
        print(f"❌ TURN modules: Not available ({e})")
        print("   Copy TURN files: cp /home/ubuntu/upload/*.py ./")
        status['turn_modules'] = False
    
    # Check Redis
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=2)
        r.ping()
        print("✅ Redis cache: Available and connected")
        status['redis_cache'] = True
    except ImportError:
        print("❌ Redis cache: Module not installed")
        print("   Install with: pip install redis")
        status['redis_cache'] = False
    except Exception as e:
        print(f"❌ Redis cache: Not connected ({e})")
        print("   Start Redis: sudo systemctl start redis-server")
        status['redis_cache'] = False
    
    # Check database modules
    database_modules = ['sqlite3', 'psycopg2', 'pymongo']
    available_dbs = []
    
    for db_module in database_modules:
        try:
            if db_module == 'sqlite3':
                import sqlite3
                available_dbs.append('SQLite')
            elif db_module == 'psycopg2':
                import psycopg2
                available_dbs.append('PostgreSQL')
            elif db_module == 'pymongo':
                import pymongo
                available_dbs.append('MongoDB')
        except ImportError:
            pass
    
    if available_dbs:
        print(f"✅ Database support: {', '.join(available_dbs)}")
        status['database'] = True
    else:
        print("❌ Database support: Limited to file storage")
        status['database'] = False
    
    # Check optional analysis modules
    analysis_modules = []
    try:
        import nltk
        analysis_modules.append('NLTK')
    except ImportError:
        pass
    
    try:
        import textblob
        analysis_modules.append('TextBlob')
    except ImportError:
        pass
    
    try:
        import numpy
        analysis_modules.append('NumPy')
    except ImportError:
        pass
    
    try:
        import pandas
        analysis_modules.append('Pandas')
    except ImportError:
        pass
    
    if analysis_modules:
        print(f"✅ Analysis modules: {', '.join(analysis_modules)}")
        status['optional_analysis'] = True
    else:
        print("❌ Analysis modules: Basic analysis only")
        print("   Install with: pip install nltk textblob numpy pandas")
        status['optional_analysis'] = False
    
    return status

def check_system_requirements():
    """Check system-level requirements"""
    
    print("\n" + "=" * 60)
    print("System Requirements Check")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 11):
        print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"❌ Python version: {python_version.major}.{python_version.minor}.{python_version.micro} (requires 3.11+)")
    
    # Check Chrome
    try:
        result = subprocess.run(['google-chrome', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Chrome browser: {result.stdout.strip()}")
        else:
            print("❌ Chrome browser: Not found")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Chrome browser: Not found or not in PATH")
    
    # Check available disk space
    try:
        import shutil
        total, used, free = shutil.disk_usage('.')
        free_gb = free // (1024**3)
        if free_gb >= 10:
            print(f"✅ Disk space: {free_gb} GB available")
        else:
            print(f"⚠️  Disk space: {free_gb} GB available (recommend 10+ GB)")
    except Exception as e:
        print(f"❌ Disk space: Could not check ({e})")

def provide_installation_guidance(status):
    """Provide installation guidance based on missing modules"""
    
    print("\n" + "=" * 60)
    print("Installation Guidance")
    print("=" * 60)
    
    if not status['core']:
        print("🚨 CRITICAL: Core modules missing!")
        print("   Ensure you're in the correct directory with prompt_engine.py")
        return
    
    missing_modules = []
    
    if not status['browser_automation']:
        missing_modules.append("Browser Automation")
        print("\n📱 Browser Automation Setup:")
        print("   pip install selenium webdriver-manager")
        print("   # For Ubuntu/Debian:")
        print("   sudo apt install google-chrome-stable")
        print("   # For macOS:")
        print("   brew install --cask google-chrome")
    
    if not status['turn_modules']:
        missing_modules.append("TURN Modules")
        print("\n🔒 TURN Cybersecurity Modules:")
        print("   cp /home/ubuntu/upload/*.py /home/ubuntu/datascope-enhanced/")
        print("   # Enables advanced threat analysis")
    
    if not status['redis_cache']:
        missing_modules.append("Redis Cache")
        print("\n⚡ Redis Cache Setup:")
        print("   pip install redis")
        print("   # For Ubuntu/Debian:")
        print("   sudo apt install redis-server")
        print("   sudo systemctl start redis-server")
        print("   # For macOS:")
        print("   brew install redis")
        print("   brew services start redis")
    
    if not status['optional_analysis']:
        missing_modules.append("Analysis Modules")
        print("\n📊 Optional Analysis Modules:")
        print("   pip install nltk textblob numpy pandas")
        print("   # Enables advanced text analysis and data processing")
    
    if not missing_modules:
        print("\n🎉 All modules are available!")
        print("   DataScope Enhanced is ready for full functionality!")
    else:
        print(f"\n📋 Missing modules: {', '.join(missing_modules)}")
        print("   Install the modules above based on your needs.")

def test_functionality(status):
    """Test basic functionality of available modules"""
    
    print("\n" + "=" * 60)
    print("Functionality Tests")
    print("=" * 60)
    
    if status['core']:
        try:
            from prompt_engine import PromptEngine
            engine = PromptEngine()
            prompt = engine.generate_collection_prompt('cybersecurity')
            print("✅ Core functionality: Working")
        except Exception as e:
            print(f"❌ Core functionality: Error ({e})")
    
    if status['browser_automation']:
        try:
            from browser_automation import BrowserDataCollector
            collector = BrowserDataCollector(headless=True)
            print("✅ Browser automation: Working")
        except Exception as e:
            print(f"❌ Browser automation: Error ({e})")
    
    if status['turn_modules']:
        try:
            from turn_integration import turn_integration
            if turn_integration.is_available():
                print("✅ TURN modules: Working (full functionality)")
            else:
                print("⚠️  TURN modules: Working (fallback mode)")
        except Exception as e:
            print(f"❌ TURN modules: Error ({e})")

def main():
    """Main function to run all checks"""
    
    # Check module availability
    status = check_module_availability()
    
    # Check system requirements
    check_system_requirements()
    
    # Provide installation guidance
    provide_installation_guidance(status)
    
    # Test functionality
    test_functionality(status)
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    available = sum(status.values())
    total = len(status)
    percentage = (available / total) * 100
    
    print(f"Available modules: {available}/{total} ({percentage:.1f}%)")
    
    if percentage == 100:
        print("🎉 Perfect! All modules available - full functionality!")
    elif percentage >= 80:
        print("✅ Excellent! Most modules available - nearly full functionality")
    elif percentage >= 60:
        print("👍 Good! Core modules available - basic functionality working")
    elif percentage >= 40:
        print("⚠️  Limited functionality - consider installing missing modules")
    else:
        print("🚨 Very limited functionality - please install core modules")
    
    print("\nNext steps:")
    if percentage < 100:
        print("1. Follow the installation guidance above")
        print("2. Run this script again to verify installation")
        print("3. Test DataScope Enhanced with: python enhanced_main.py cybersecurity --test")
    else:
        print("1. Test DataScope Enhanced: python enhanced_main.py cybersecurity federal")
        print("2. Explore the API: python api_server.py")
        print("3. Read the documentation: README.md")

if __name__ == "__main__":
    main()

