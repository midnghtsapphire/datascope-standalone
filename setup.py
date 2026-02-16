#!/usr/bin/env python3
"""
DataScope Enhanced - Setup Script
Multi-Domain Intelligence Platform with Prompt-Driven Data Collection
"""

from setuptools import setup, find_packages
import os
import sys

# Ensure Python 3.11+
if sys.version_info < (3, 11):
    sys.exit('DataScope Enhanced requires Python 3.11 or higher')

# Read README for long description
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Version
VERSION = '1.0.0'

# Core requirements
install_requires = [
    'requests>=2.31.0',
    'beautifulsoup4>=4.12.2',
    'lxml>=4.9.3',
    'flask>=2.3.3',
    'flask-cors>=4.0.0',
    'pandas>=2.1.1',
    'numpy>=1.24.3',
    'python-json-logger>=2.0.7',
    'python-dotenv>=1.0.0',
    'pyyaml>=6.0.1',
    'python-dateutil>=2.8.2',
    'urllib3>=2.0.4',
    'certifi>=2023.7.22',
]

# Optional requirements for full functionality
extras_require = {
    'browser': [
        'selenium>=4.15.0',
        'webdriver-manager>=4.0.1',
    ],
    'cache': [
        'redis>=5.0.0',
    ],
    'analysis': [
        'nltk>=3.8.1',
        'textblob>=0.17.1',
    ],
    'images': [
        'pillow>=10.0.0',
    ],
    'async': [
        'aiohttp>=3.8.5',
    ],
    'production': [
        'gunicorn>=21.2.0',
        'cryptography>=41.0.4',
    ],
    'dev': [
        'pytest>=7.4.2',
        'pytest-cov>=4.1.0',
        'black>=23.7.0',
        'flake8>=6.0.0',
        'sphinx>=7.1.2',
        'sphinx-rtd-theme>=1.3.0',
    ]
}

# All optional dependencies
extras_require['all'] = list(set(sum(extras_require.values(), [])))

setup(
    name='datascope-enhanced',
    version=VERSION,
    description='Multi-Domain Intelligence Platform with Prompt-Driven Data Collection',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='DataScope Team',
    author_email='team@datascope-enhanced.com',
    url='https://github.com/your-org/datascope-enhanced',
    project_urls={
        'Documentation': 'https://docs.datascope-enhanced.com',
        'Source': 'https://github.com/your-org/datascope-enhanced',
        'Tracker': 'https://github.com/your-org/datascope-enhanced/issues',
    },
    packages=find_packages(exclude=['tests*', 'docs*']),
    include_package_data=True,
    package_data={
        'datascope_enhanced': [
            'templates/*.html',
            'static/*',
            'config/*.yaml',
            'schemas/*.json',
        ],
    },
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'datascope=enhanced_main:main',
            'datascope-collect=enhanced_main:collect_command',
            'datascope-report=enhanced_main:report_command',
            'datascope-api=api_server:main',
            'datascope-setup=scripts.setup:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring',
    ],
    keywords=[
        'data-collection',
        'intelligence',
        'automation',
        'cybersecurity',
        'threat-intelligence',
        'web-scraping',
        'browser-automation',
        'multi-domain',
        'reporting',
        'analytics'
    ],
    zip_safe=False,
    platforms=['any'],
    license='MIT',
)

