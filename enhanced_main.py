#!/usr/bin/env python3
"""
DataScope Enhanced - Main Orchestration System
Combines TURN-style automation with prompt-driven multi-domain data collection
"""

import os
import sys
import json
import datetime
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the current directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompt_engine import PromptEngine

# Optional imports
try:
    from browser_automation import BrowserDataCollector
    BROWSER_AUTOMATION_AVAILABLE = True
except ImportError:
    BROWSER_AUTOMATION_AVAILABLE = False
    logging.warning("Browser automation not available - some features limited")

# Check for TURN modules
try:
    from turn_integration import turn_integration, ReportGenerator
    TURN_AVAILABLE = turn_integration.is_available()
    if TURN_AVAILABLE:
        logging.info("TURN integration available - enhanced cybersecurity analysis enabled")
    else:
        logging.warning("TURN modules not available - using fallback cybersecurity analysis")
except ImportError:
    TURN_AVAILABLE = False
    logging.warning("TURN integration not available - cybersecurity features limited")

class DataScopeEnhanced:
    """Enhanced multi-domain data intelligence platform"""
    
    def __init__(self, output_dir="./reports", cache_dir="./cache"):
        self.output_dir = Path(output_dir)
        self.cache_dir = Path(cache_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.prompt_engine = PromptEngine(cache_dir=str(self.cache_dir))
        self.browser_collector = None  # Lazy initialization
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        
        # Domain-specific processors
        self.domain_processors = {
            'cybersecurity': self._process_cybersecurity_data,
            'real-estate': self._process_real_estate_data,
            'social-media': self._process_social_media_data,
            'healthcare': self._process_healthcare_data
        }
    
    def _setup_logging(self):
        """Configure logging for the system"""
        log_file = self.output_dir / 'datascope_enhanced.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def collect_domain_data(self, domain: str, location: str = None, 
                           filters: Dict[str, Any] = None, 
                           use_cache: bool = True) -> Dict[str, Any]:
        """Collect data for a specific domain using intelligent prompts"""
        
        self.logger.info(f"Starting data collection for domain: {domain}")
        
        # Check cache first
        if use_cache:
            cached_data = self.prompt_engine.get_cached_data(domain)
            if cached_data:
                self.logger.info(f"Using cached data for {domain}")
                return cached_data
        
        # Generate collection prompt
        prompt = self.prompt_engine.generate_collection_prompt(domain, location, filters)
        self.logger.info(f"Generated collection prompt with {len(prompt['collection_plan'])} sources")
        
        # Execute collection
        results = self.prompt_engine.execute_collection_prompt(prompt)
        
        # Process domain-specific data
        if domain in self.domain_processors:
            results = self.domain_processors[domain](results)
        
        # Generate smart filters
        if results['data']:
            smart_filters = self.prompt_engine.generate_smart_filters(domain, results['data'])
            results['available_filters'] = smart_filters
        
        self.logger.info(f"Collected {results['total_items_collected']} items for {domain}")
        return results
    
    def collect_with_browser_automation(self, platform: str, credentials: Dict[str, str] = None,
                                      collection_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Collect data using browser automation for complex sites"""
        
        if not BROWSER_AUTOMATION_AVAILABLE:
            return {
                'platform': platform,
                'success': False,
                'error': 'Browser automation not available - install selenium and chrome driver',
                'data': []
            }
        
        if not self.browser_collector:
            self.browser_collector = BrowserDataCollector(headless=True)
        
        collection_params = collection_params or {}
        
        if credentials:
            self.logger.info(f"Collecting data from {platform} with login")
            return self.browser_collector.collect_with_login(platform, credentials, collection_params)
        else:
            self.logger.info(f"Collecting public data from {platform}")
            return self.browser_collector.collect_public_data(platform, collection_params)
    
    def _process_cybersecurity_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Process cybersecurity data using TURN-style analysis"""
        
        if not TURN_AVAILABLE:
            self.logger.warning("TURN modules not available - basic processing only")
            return results
        
        try:
            # Use TURN threat analysis if available
            analyzer = ThreatAnalysisEngine()
            
            # Convert our data format to TURN format
            turn_data = self._convert_to_turn_format(results['data'])
            
            # Analyze threats
            analysis = analyzer.analyze_threats(turn_data)
            
            # Add analysis to results
            results['threat_analysis'] = analysis
            results['severity_distribution'] = analysis.get('severity_distribution', {})
            
        except Exception as e:
            self.logger.error(f"Error in cybersecurity processing: {str(e)}")
        
        return results
    
    def _process_real_estate_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Process real estate data with market analysis"""
        
        data = results['data']
        
        # Extract price information
        prices = []
        for item in data:
            if 'price' in item:
                # Clean price data
                price_str = item['price'].replace('$', '').replace(',', '').replace('M', '000000').replace('K', '000')
                try:
                    prices.append(float(price_str))
                except ValueError:
                    continue
        
        if prices:
            results['market_analysis'] = {
                'average_price': sum(prices) / len(prices),
                'min_price': min(prices),
                'max_price': max(prices),
                'total_listings': len(prices)
            }
        
        return results
    
    def _process_social_media_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Process social media data with engagement analysis"""
        
        data = results['data']
        
        # Analyze engagement patterns
        total_engagement = 0
        engagement_count = 0
        
        for item in data:
            if 'engagement' in item:
                try:
                    # Extract numeric engagement
                    engagement_str = item['engagement'].replace(',', '')
                    engagement_num = float(engagement_str)
                    total_engagement += engagement_num
                    engagement_count += 1
                except ValueError:
                    continue
        
        if engagement_count > 0:
            results['engagement_analysis'] = {
                'average_engagement': total_engagement / engagement_count,
                'total_posts_analyzed': engagement_count
            }
        
        return results
    
    def _process_healthcare_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Process healthcare data with trend analysis"""
        
        # Basic healthcare data processing
        data = results['data']
        
        # Count mentions of key health topics
        health_topics = ['outbreak', 'disease', 'vaccine', 'treatment', 'symptoms']
        topic_counts = {topic: 0 for topic in health_topics}
        
        for item in data:
            content = item.get('content', '').lower()
            for topic in health_topics:
                if topic in content:
                    topic_counts[topic] += 1
        
        results['health_trends'] = topic_counts
        
        return results
    
    def _convert_to_turn_format(self, data: List[Dict]) -> Dict[str, Any]:
        """Convert our data format to TURN-compatible format"""
        
        turn_data = {
            'vulnerabilities': [],
            'advisories': [],
            'threats': []
        }
        
        for item in data:
            if 'cve' in item.get('title', '').lower() or 'vulnerability' in item.get('title', '').lower():
                turn_data['vulnerabilities'].append(item)
            elif 'advisory' in item.get('title', '').lower():
                turn_data['advisories'].append(item)
            else:
                turn_data['threats'].append(item)
        
        return turn_data
    
    def generate_comprehensive_report(self, domain: str, data: Dict[str, Any], 
                                    report_type: str = 'operational') -> str:
        """Generate comprehensive reports for any domain"""
        
        timestamp = datetime.datetime.now()
        report_id = f"{domain}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        if domain == 'cybersecurity' and TURN_AVAILABLE:
            # Use TURN report generator for cybersecurity
            try:
                generator = ReportGenerator()
                report_content = generator.generate_operational_report(data)
            except Exception as e:
                self.logger.error(f"TURN report generation failed: {str(e)}")
                report_content = self._generate_generic_report(domain, data, report_type)
        else:
            # Use generic report generator
            report_content = self._generate_generic_report(domain, data, report_type)
        
        # Save report
        report_filename = f"{report_id}_{report_type}_report.md"
        report_path = self.output_dir / report_filename
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        self.logger.info(f"Report generated: {report_path}")
        return str(report_path)
    
    def _generate_generic_report(self, domain: str, data: Dict[str, Any], 
                               report_type: str) -> str:
        """Generate a generic report for any domain"""
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# {domain.title()} Intelligence Report
        
**Generated:** {timestamp}
**Domain:** {domain.title()}
**Report Type:** {report_type.title()}

## Executive Summary

This report contains intelligence data collected for the {domain} domain.

### Collection Summary
- **Total Items Collected:** {data.get('total_items_collected', 0)}
- **Sources Processed:** {data.get('sources_processed', 0)}
- **Collection Timestamp:** {data.get('collection_timestamp', 'Unknown')}

"""
        
        # Add domain-specific sections
        if domain == 'real-estate' and 'market_analysis' in data:
            market = data['market_analysis']
            report += f"""## Market Analysis
- **Average Price:** ${market['average_price']:,.2f}
- **Price Range:** ${market['min_price']:,.2f} - ${market['max_price']:,.2f}
- **Total Listings:** {market['total_listings']}

"""
        
        elif domain == 'social-media' and 'engagement_analysis' in data:
            engagement = data['engagement_analysis']
            report += f"""## Engagement Analysis
- **Average Engagement:** {engagement['average_engagement']:.2f}
- **Posts Analyzed:** {engagement['total_posts_analyzed']}

"""
        
        elif domain == 'healthcare' and 'health_trends' in data:
            trends = data['health_trends']
            report += f"""## Health Trends
"""
            for topic, count in trends.items():
                report += f"- **{topic.title()}:** {count} mentions\n"
            report += "\n"
        
        # Add data samples
        if data.get('data'):
            report += "## Data Samples\n\n"
            for i, item in enumerate(data['data'][:5]):  # Show first 5 items
                report += f"### Item {i+1}\n"
                for key, value in item.items():
                    if key not in ['links', 'images']:  # Skip complex fields
                        report += f"- **{key.title()}:** {value}\n"
                report += "\n"
        
        # Add available filters
        if data.get('available_filters'):
            report += "## Available Filters\n\n"
            for filter_type, values in data['available_filters'].items():
                if values:
                    report += f"### {filter_type.title()}\n"
                    for value in values[:10]:  # Show first 10 values
                        report += f"- {value}\n"
                    report += "\n"
        
        report += f"""## Collection Details

### Sources
"""
        for i, error in enumerate(data.get('errors', [])):
            report += f"{i+1}. {error}\n"
        
        report += f"""
---
*Generated by DataScope Enhanced - Multi-Domain Intelligence Platform*
*Report ID: {domain}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}*
"""
        
        return report
    
    def run_automated_collection(self, domains: List[str], location: str = None) -> Dict[str, Any]:
        """Run automated data collection for multiple domains"""
        
        self.logger.info(f"Starting automated collection for domains: {domains}")
        
        results = {
            'timestamp': datetime.datetime.now().isoformat(),
            'domains_processed': [],
            'total_items_collected': 0,
            'reports_generated': [],
            'errors': []
        }
        
        for domain in domains:
            try:
                self.logger.info(f"Processing domain: {domain}")
                
                # Collect data
                domain_data = self.collect_domain_data(domain, location)
                
                # Generate report
                report_path = self.generate_comprehensive_report(domain, domain_data)
                
                results['domains_processed'].append(domain)
                results['total_items_collected'] += domain_data.get('total_items_collected', 0)
                results['reports_generated'].append(report_path)
                
            except Exception as e:
                error_msg = f"Error processing {domain}: {str(e)}"
                self.logger.error(error_msg)
                results['errors'].append(error_msg)
        
        # Save execution summary
        summary_file = self.output_dir / f"automated_collection_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.logger.info(f"Automated collection complete. Summary: {summary_file}")
        return results

def main():
    """Main entry point for DataScope Enhanced"""
    
    # Initialize system
    datascope = DataScopeEnhanced()
    
    if len(sys.argv) > 1:
        domain = sys.argv[1]
        location = sys.argv[2] if len(sys.argv) > 2 else None
        
        # Single domain collection
        print(f"Collecting data for domain: {domain}")
        results = datascope.collect_domain_data(domain, location)
        
        # Generate report
        report_path = datascope.generate_comprehensive_report(domain, results)
        print(f"Report generated: {report_path}")
        
    else:
        # Multi-domain automated collection
        domains = ['cybersecurity', 'real-estate', 'healthcare']
        print("Running automated multi-domain collection...")
        
        results = datascope.run_automated_collection(domains)
        print(f"Collection complete. Processed {len(results['domains_processed'])} domains.")
        print(f"Total items collected: {results['total_items_collected']}")

if __name__ == "__main__":
    main()

