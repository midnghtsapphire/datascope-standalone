#!/usr/bin/env python3
"""
DataScope Enhanced - Prompt-Driven Data Collection Engine
Intelligently gathers data from any source using browser automation and smart prompts
"""

import os
import json
import datetime
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
from bs4 import BeautifulSoup
import time
import random

class PromptEngine:
    """Intelligent prompt-driven data collection system"""
    
    def __init__(self, cache_dir="./cache", output_dir="./data"):
        self.cache_dir = Path(cache_dir)
        self.output_dir = Path(output_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Load domain-specific prompts and strategies
        self.domain_strategies = self._load_domain_strategies()
        
    def _load_domain_strategies(self) -> Dict[str, Dict]:
        """Load domain-specific data collection strategies"""
        return {
            'cybersecurity': {
                'sources': [
                    {
                        'name': 'CISA KEV',
                        'url': 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json',
                        'type': 'api',
                        'parser': 'json'
                    },
                    {
                        'name': 'FBI IC3',
                        'url': 'https://www.ic3.gov/PSA',
                        'type': 'scrape',
                        'parser': 'html',
                        'selectors': {
                            'items': '.view-content .views-row',
                            'title': '.field-content a',
                            'date': '.date-display-single',
                            'link': '.field-content a'
                        }
                    }
                ],
                'filters': ['severity', 'date', 'vendor', 'cve'],
                'keywords': ['vulnerability', 'exploit', 'malware', 'ransomware', 'phishing']
            },
            'real-estate': {
                'sources': [
                    {
                        'name': 'Zillow',
                        'url': 'https://www.zillow.com',
                        'type': 'scrape',
                        'parser': 'html',
                        'requires_location': True,
                        'selectors': {
                            'items': '[data-testid="property-card"]',
                            'price': '[data-testid="price"]',
                            'address': '[data-testid="property-card-addr"]',
                            'beds': '[data-testid="property-card-specification"]',
                            'link': 'a'
                        }
                    }
                ],
                'filters': ['price_range', 'location', 'bedrooms', 'property_type'],
                'keywords': ['sale', 'rent', 'property', 'home', 'condo', 'apartment']
            },
            'social-media': {
                'sources': [
                    {
                        'name': 'Lemon8',
                        'url': 'https://www.lemon8-app.com',
                        'type': 'browser_automation',
                        'requires_login': True,
                        'selectors': {
                            'posts': '[data-testid="post-item"]',
                            'content': '.post-content',
                            'author': '.author-name',
                            'engagement': '.engagement-stats'
                        }
                    }
                ],
                'filters': ['hashtags', 'author', 'engagement', 'date'],
                'keywords': ['trending', 'viral', 'lifestyle', 'fashion', 'beauty']
            },
            'healthcare': {
                'sources': [
                    {
                        'name': 'CDC',
                        'url': 'https://www.cdc.gov',
                        'type': 'scrape',
                        'parser': 'html'
                    }
                ],
                'filters': ['condition', 'location', 'date', 'severity'],
                'keywords': ['outbreak', 'disease', 'health', 'medical', 'treatment']
            }
        }
    
    def generate_collection_prompt(self, domain: str, location: str = None, 
                                 filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate intelligent data collection prompt for a domain"""
        
        if domain not in self.domain_strategies:
            return self._generate_generic_prompt(domain, location, filters)
        
        strategy = self.domain_strategies[domain]
        
        prompt = {
            'domain': domain,
            'location': location,
            'filters': filters or {},
            'sources': strategy['sources'],
            'collection_plan': [],
            'expected_data_types': strategy.get('keywords', []),
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Generate collection plan for each source
        for source in strategy['sources']:
            plan_item = {
                'source_name': source['name'],
                'collection_method': source['type'],
                'url': self._build_url(source, location, filters),
                'parser_config': {
                    'type': source.get('parser', 'html'),
                    'selectors': source.get('selectors', {})
                },
                'requires_login': source.get('requires_login', False),
                'rate_limit': source.get('rate_limit', 1.0)
            }
            prompt['collection_plan'].append(plan_item)
        
        return prompt
    
    def _build_url(self, source: Dict, location: str = None, 
                   filters: Dict[str, Any] = None) -> str:
        """Build URL with location and filter parameters"""
        base_url = source['url']
        
        if source.get('requires_location') and location:
            # For real estate sites like Zillow
            if 'zillow' in base_url.lower():
                return f"{base_url}/homes/{location.replace(' ', '-').lower()}_rb/"
        
        # Add filter parameters if supported
        if filters and source.get('supports_filters'):
            params = []
            for key, value in filters.items():
                if key in source.get('filter_mapping', {}):
                    param_name = source['filter_mapping'][key]
                    params.append(f"{param_name}={value}")
            
            if params:
                separator = '&' if '?' in base_url else '?'
                return f"{base_url}{separator}{'&'.join(params)}"
        
        return base_url
    
    def _generate_generic_prompt(self, domain: str, location: str = None, 
                               filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a generic collection prompt for unknown domains"""
        
        # Use search engines and common data sources
        search_queries = [
            f"{domain} data {location or ''}",
            f"{domain} statistics {location or ''}",
            f"{domain} trends {location or ''}",
            f"{domain} news {location or ''}"
        ]
        
        return {
            'domain': domain,
            'location': location,
            'filters': filters or {},
            'collection_plan': [
                {
                    'source_name': 'Google Search',
                    'collection_method': 'search',
                    'queries': search_queries,
                    'parser_config': {'type': 'search_results'}
                },
                {
                    'source_name': 'News Sources',
                    'collection_method': 'news_scrape',
                    'queries': search_queries,
                    'parser_config': {'type': 'news_articles'}
                }
            ],
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def execute_collection_prompt(self, prompt: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the data collection based on the prompt"""
        
        results = {
            'domain': prompt['domain'],
            'location': prompt.get('location'),
            'collection_timestamp': datetime.datetime.now().isoformat(),
            'sources_processed': 0,
            'total_items_collected': 0,
            'data': [],
            'errors': []
        }
        
        for plan_item in prompt['collection_plan']:
            try:
                self.logger.info(f"Collecting from: {plan_item['source_name']}")
                
                if plan_item['collection_method'] == 'api':
                    data = self._collect_api_data(plan_item)
                elif plan_item['collection_method'] == 'scrape':
                    data = self._collect_scrape_data(plan_item)
                elif plan_item['collection_method'] == 'browser_automation':
                    data = self._collect_browser_data(plan_item)
                elif plan_item['collection_method'] == 'search':
                    data = self._collect_search_data(plan_item)
                else:
                    self.logger.warning(f"Unknown collection method: {plan_item['collection_method']}")
                    continue
                
                if data:
                    results['data'].extend(data)
                    results['total_items_collected'] += len(data)
                
                results['sources_processed'] += 1
                
                # Rate limiting
                time.sleep(plan_item.get('rate_limit', 1.0))
                
            except Exception as e:
                error_msg = f"Error collecting from {plan_item['source_name']}: {str(e)}"
                self.logger.error(error_msg)
                results['errors'].append(error_msg)
        
        # Cache the results
        self._cache_results(prompt['domain'], results)
        
        return results
    
    def _collect_api_data(self, plan_item: Dict) -> List[Dict]:
        """Collect data from API endpoints"""
        try:
            response = self.session.get(plan_item['url'], timeout=30)
            response.raise_for_status()
            
            if plan_item['parser_config']['type'] == 'json':
                data = response.json()
                
                # Handle different JSON structures
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    # Look for common list keys
                    for key in ['vulnerabilities', 'items', 'data', 'results']:
                        if key in data and isinstance(data[key], list):
                            return data[key]
                    return [data]
            
            return []
            
        except Exception as e:
            self.logger.error(f"API collection error: {str(e)}")
            return []
    
    def _collect_scrape_data(self, plan_item: Dict) -> List[Dict]:
        """Collect data by scraping web pages"""
        try:
            response = self.session.get(plan_item['url'], timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            selectors = plan_item['parser_config'].get('selectors', {})
            
            items = []
            
            if 'items' in selectors:
                # Extract structured data
                item_elements = soup.select(selectors['items'])
                
                for element in item_elements:
                    item_data = {}
                    
                    for field, selector in selectors.items():
                        if field == 'items':
                            continue
                        
                        field_element = element.select_one(selector)
                        if field_element:
                            if field == 'link':
                                item_data[field] = field_element.get('href', '')
                            else:
                                item_data[field] = field_element.get_text(strip=True)
                    
                    if item_data:
                        items.append(item_data)
            else:
                # Generic text extraction
                items.append({
                    'content': soup.get_text(strip=True),
                    'url': plan_item['url'],
                    'title': soup.title.string if soup.title else ''
                })
            
            return items
            
        except Exception as e:
            self.logger.error(f"Scraping error: {str(e)}")
            return []
    
    def _collect_browser_data(self, plan_item: Dict) -> List[Dict]:
        """Collect data using browser automation (for sites requiring JS/login)"""
        # This would integrate with browser automation tools
        # For now, return placeholder indicating browser automation needed
        
        return [{
            'source': plan_item['source_name'],
            'message': 'Browser automation required - user login needed',
            'url': plan_item['url'],
            'requires_manual_setup': True
        }]
    
    def _collect_search_data(self, plan_item: Dict) -> List[Dict]:
        """Collect data using search queries"""
        # This would integrate with search APIs or scraping
        # For now, return placeholder search results
        
        results = []
        for query in plan_item.get('queries', []):
            results.append({
                'query': query,
                'type': 'search_result',
                'message': f'Search results for: {query}',
                'requires_search_api': True
            })
        
        return results
    
    def _cache_results(self, domain: str, results: Dict[str, Any]) -> None:
        """Cache collection results for future use"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        cache_file = self.cache_dir / f"{domain}_{timestamp}_results.json"
        
        with open(cache_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.logger.info(f"Results cached to: {cache_file}")
    
    def get_cached_data(self, domain: str, max_age_hours: int = 24) -> Optional[Dict[str, Any]]:
        """Retrieve cached data if available and fresh"""
        
        cache_files = list(self.cache_dir.glob(f"{domain}_*_results.json"))
        
        if not cache_files:
            return None
        
        # Get the most recent cache file
        latest_cache = max(cache_files, key=lambda x: x.stat().st_mtime)
        
        # Check if cache is still fresh
        cache_age = time.time() - latest_cache.stat().st_mtime
        if cache_age > (max_age_hours * 3600):
            return None
        
        try:
            with open(latest_cache, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error reading cache: {str(e)}")
            return None
    
    def generate_smart_filters(self, domain: str, data: List[Dict]) -> Dict[str, List]:
        """Generate intelligent filter options based on collected data"""
        
        filters = {
            'locations': set(),
            'dates': set(),
            'categories': set(),
            'sources': set()
        }
        
        for item in data:
            # Extract location information
            for location_field in ['location', 'address', 'city', 'state']:
                if location_field in item and item[location_field]:
                    filters['locations'].add(item[location_field])
            
            # Extract date information
            for date_field in ['date', 'timestamp', 'created_at', 'published']:
                if date_field in item and item[date_field]:
                    filters['dates'].add(item[date_field])
            
            # Extract category information
            for category_field in ['category', 'type', 'severity', 'tag']:
                if category_field in item and item[category_field]:
                    filters['categories'].add(item[category_field])
            
            # Track sources
            if 'source' in item:
                filters['sources'].add(item['source'])
        
        # Convert sets to sorted lists
        return {key: sorted(list(values)) for key, values in filters.items()}

def main():
    """Test the prompt engine"""
    logging.basicConfig(level=logging.INFO)
    
    engine = PromptEngine()
    
    # Test cybersecurity domain
    prompt = engine.generate_collection_prompt('cybersecurity', location='federal')
    print("Generated prompt:")
    print(json.dumps(prompt, indent=2))
    
    # Execute collection
    results = engine.execute_collection_prompt(prompt)
    print(f"\nCollection results: {results['total_items_collected']} items from {results['sources_processed']} sources")

if __name__ == "__main__":
    main()

