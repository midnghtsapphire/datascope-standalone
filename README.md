# DataScope Enhanced — Standalone

> AI-powered multi-domain data intelligence platform with natural language querying, auto-generated reports, and cybersecurity threat analysis.

DataScope Enhanced is a fully standalone data intelligence platform that combines a Python Flask backend with a React cybersecurity threat dashboard. It uses intelligent prompts, browser automation, and smart caching to gather data from any source — including platforms without APIs like Lemon8, Instagram, and LinkedIn.

### Blue Ocean Enhancements
- **AI-Powered Data Insights** — Automatic trend detection, anomaly identification, pattern recognition, and correlation analysis.
- **Natural Language Querying (NLQ)** — Ask questions in plain English and get structured results with suggested visualizations.
- **Auto-Generated Reports** — AI engine produces comprehensive reports with executive summaries and actionable recommendations.
- **Smart Filters** — Zillow-style filtering interface for any data domain.

## 🌟 Key Features

### Universal Data Collection
- **Prompt-Driven Intelligence**: Generate smart collection strategies for any domain
- **Browser Automation**: Collect data from JavaScript-heavy sites and platforms requiring login
- **API Integration**: Seamlessly integrate with available APIs
- **Smart Caching**: Intelligent data caching with freshness management
- **Multi-Source Fusion**: Combine data from multiple sources into unified reports

### Supported Domains
- **Cybersecurity**: CISA KEV, FBI IC3, threat intelligence
- **Real Estate**: Zillow-style property data, market analysis
- **Social Media**: Lemon8, Instagram, LinkedIn (with login)
- **Healthcare**: CDC data, health trends, outbreak monitoring
- **Custom Domains**: Extensible framework for any data source

### Advanced Analytics
- **Threat Analysis**: TURN-style cybersecurity threat categorization
- **Market Intelligence**: Real estate market analysis and trends
- **Engagement Analytics**: Social media engagement pattern analysis
- **Smart Filtering**: Auto-generated filters based on collected data

### Automated Reporting
- **Multi-Format Reports**: Operational reports, public briefs, executive summaries
- **Social Media Ready**: Generate summary images for LinkedIn, Facebook, Instagram, TikTok
- **Scheduled Automation**: Daily, weekly, or custom scheduling
- **Export Options**: PDF, JSON, CSV, Markdown

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Chrome browser (for browser automation features)
- Internet connection

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-org/datascope-enhanced.git
cd datascope-enhanced
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Install Chrome WebDriver** (for browser automation):
```bash
# Option 1: Automatic installation
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"

# Option 2: Manual installation
# Download from https://chromedriver.chromium.org/
# Add to PATH or place in project directory
```

5. **Configure environment** (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Basic Usage

#### Command Line Interface

**Single Domain Collection**:
```bash
python enhanced_main.py cybersecurity federal
python enhanced_main.py real-estate "New York"
python enhanced_main.py social-media
```

**Multi-Domain Automation**:
```bash
python enhanced_main.py
```

#### Python API

```python
from enhanced_main import DataScopeEnhanced

# Initialize the platform
datascope = DataScopeEnhanced()

# Collect cybersecurity data
cyber_data = datascope.collect_domain_data('cybersecurity', location='federal')

# Generate comprehensive report
report_path = datascope.generate_comprehensive_report('cybersecurity', cyber_data)

# Browser automation for social media
credentials = {'username': 'your_username', 'password': 'your_password'}
social_data = datascope.collect_with_browser_automation('lemon8', credentials)
```

## 📖 Detailed Documentation

### Architecture Overview

DataScope Enhanced follows a modular architecture:

```
DataScope Enhanced
├── Prompt Engine          # Intelligent data collection strategy generation
├── Browser Automation     # Selenium-based data collection for complex sites
├── Domain Processors      # Specialized processing for different domains
├── Caching System        # Smart data caching and freshness management
├── Report Generator      # Multi-format report generation
└── API Interface         # RESTful API for integration
```

### Core Components

#### 1. Prompt Engine (`prompt_engine.py`)

The heart of DataScope Enhanced, responsible for generating intelligent data collection strategies.

**Key Features**:
- Domain-specific collection strategies
- Smart URL building with location and filter parameters
- Generic prompt generation for unknown domains
- Intelligent filter generation from collected data

**Usage**:
```python
from prompt_engine import PromptEngine

engine = PromptEngine()

# Generate collection prompt
prompt = engine.generate_collection_prompt('cybersecurity', location='federal')

# Execute collection
results = engine.execute_collection_prompt(prompt)

# Generate smart filters
filters = engine.generate_smart_filters('cybersecurity', results['data'])
```

#### 2. Browser Automation (`browser_automation.py`)

Handles data collection from sites requiring JavaScript execution or user authentication.

**Supported Platforms**:
- Lemon8 (with login support)
- Instagram (with login support)
- LinkedIn (with login support)
- Generic web scraping

**Usage**:
```python
from browser_automation import BrowserDataCollector

collector = BrowserDataCollector(headless=True)

# Collect with login
credentials = {'username': 'user', 'password': 'pass'}
results = collector.collect_with_login('lemon8', credentials, {
    'max_items': 50,
    'max_scrolls': 5
})

# Collect public data
results = collector.collect_public_data('lemon8', {
    'url': 'https://www.lemon8-app.com/trending',
    'max_items': 20
})
```

#### 3. Enhanced Main (`enhanced_main.py`)

The main orchestration system that combines all components.

**Key Features**:
- Multi-domain data collection
- Domain-specific processing
- Automated report generation
- Caching management

### Domain-Specific Processing

#### Cybersecurity Domain
- CISA KEV catalog analysis
- FBI IC3 PSA collection
- Threat categorization and severity analysis
- TURN-style operational reports

#### Real Estate Domain
- Property listing collection
- Market analysis (average price, price ranges)
- Location-based filtering
- Comparative market reports

#### Social Media Domain
- Post content extraction
- Engagement metrics analysis
- Author and hashtag tracking
- Trend identification

#### Healthcare Domain
- Health trend monitoring
- Outbreak tracking
- Topic mention analysis
- Public health intelligence

### Configuration

#### Environment Variables

Create a `.env` file in the project root:

```env
# Browser Automation
CHROME_DRIVER_PATH=/path/to/chromedriver
HEADLESS_BROWSER=true

# Caching
CACHE_DURATION_HOURS=24
CACHE_DIRECTORY=./cache

# Output
OUTPUT_DIRECTORY=./reports
LOG_LEVEL=INFO

# API Configuration (optional)
API_HOST=0.0.0.0
API_PORT=5000

# Social Media Credentials (optional)
LEMON8_USERNAME=your_username
LEMON8_PASSWORD=your_password
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

#### Domain Configuration

Customize domain strategies in `prompt_engine.py`:

```python
self.domain_strategies = {
    'your_domain': {
        'sources': [
            {
                'name': 'Your Source',
                'url': 'https://your-source.com',
                'type': 'scrape',  # or 'api', 'browser_automation'
                'parser': 'html',
                'selectors': {
                    'items': '.item-selector',
                    'title': '.title-selector',
                    'content': '.content-selector'
                }
            }
        ],
        'filters': ['your', 'custom', 'filters'],
        'keywords': ['relevant', 'keywords']
    }
}
```

## 🔧 Advanced Usage

### Custom Domain Implementation

1. **Add domain strategy** to `prompt_engine.py`
2. **Create domain processor** in `enhanced_main.py`
3. **Add domain-specific report template**

Example:
```python
def _process_your_domain_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
    """Process your domain data with custom analysis"""
    data = results['data']
    
    # Your custom processing logic
    analysis = self.analyze_your_domain_data(data)
    
    results['your_analysis'] = analysis
    return results
```

### Browser Automation Customization

Add new platform support:

```python
# In browser_automation.py
self.platform_configs['your_platform'] = {
    'login_url': 'https://your-platform.com/login',
    'selectors': {
        'username_field': '#username',
        'password_field': '#password',
        'login_button': '.login-btn',
        'posts': '.post-item',
        'post_content': '.content'
    },
    'wait_time': 3,
    'scroll_pause': 2
}
```

### API Integration

DataScope Enhanced can be extended with a REST API:

```python
from flask import Flask, jsonify, request
from enhanced_main import DataScopeEnhanced

app = Flask(__name__)
datascope = DataScopeEnhanced()

@app.route('/api/collect/<domain>')
def collect_domain_data(domain):
    location = request.args.get('location')
    filters = request.args.to_dict()
    
    results = datascope.collect_domain_data(domain, location, filters)
    return jsonify(results)

@app.route('/api/report/<domain>')
def generate_report(domain):
    # Implementation here
    pass
```

### Scheduled Automation

Set up automated data collection using cron:

```bash
# Add to crontab (crontab -e)
0 6 * * * cd /path/to/datascope-enhanced && python enhanced_main.py
```

Or use the built-in scheduler:

```python
import schedule
import time

def automated_collection():
    datascope = DataScopeEnhanced()
    domains = ['cybersecurity', 'real-estate', 'healthcare']
    datascope.run_automated_collection(domains)

schedule.every().day.at("06:00").do(automated_collection)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Run specific test
pytest tests/test_prompt_engine.py
```

## 📊 Performance Optimization

### Caching Strategies
- **Memory Caching**: For frequently accessed data
- **File Caching**: For large datasets
- **Redis Caching**: For distributed deployments

### Browser Automation Optimization
- **Headless Mode**: Faster execution
- **Image Blocking**: Reduced bandwidth
- **Parallel Collection**: Multiple browser instances

### Data Processing Optimization
- **Batch Processing**: Process data in chunks
- **Async Operations**: Non-blocking I/O
- **Smart Filtering**: Reduce data processing overhead

## 🚀 Deployment

### Local Development
```bash
python enhanced_main.py
```

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

#### Using Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Chrome for browser automation
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

COPY . .
CMD ["python", "enhanced_main.py"]
```

#### Cloud Deployment
- **AWS**: Use EC2 with scheduled Lambda functions
- **Google Cloud**: Use Compute Engine with Cloud Scheduler
- **Azure**: Use Virtual Machines with Logic Apps

## 🔒 Security Considerations

### Data Protection
- **Credential Management**: Use environment variables or secure vaults
- **Data Encryption**: Encrypt sensitive cached data
- **Access Control**: Implement API authentication

### Browser Automation Security
- **Headless Mode**: Reduce attack surface
- **Sandbox Environment**: Isolate browser processes
- **Regular Updates**: Keep Chrome and WebDriver updated

### Network Security
- **HTTPS Only**: Use secure connections
- **Rate Limiting**: Respect target site limits
- **User Agent Rotation**: Avoid detection

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style
- Use Black for code formatting
- Follow PEP 8 guidelines
- Add docstrings to all functions
- Include type hints

## License

Proprietary — All rights reserved by Audrey Evans.

## 🆘 Support

- **Documentation**: [Full Documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-org/datascope-enhanced/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/datascope-enhanced/discussions)
- **Email**: support@datascope-enhanced.com

## 🙏 Acknowledgments

- Inspired by TURN Global Fusion Digest for cybersecurity intelligence
- Built with love for the open-source community
- Special thanks to all contributors

---

*DataScope Enhanced provided by free sources and APIs. Built with Python, Flask, React, and Vite.*

