#!/usr/bin/env python3
"""
CISA Advisories Data Collection Script
Collects recent CISA cybersecurity advisories for threat intelligence reporting
"""

import requests
from bs4 import BeautifulSoup
import json
import datetime
import re
from typing import List, Dict, Any

def get_cisa_advisories() -> List[Dict[str, Any]]:
    """Scrape CISA advisories page for recent announcements"""
    url = "https://www.cisa.gov/news-events/cybersecurity-advisories"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        advisories = []
        
        # Find advisory entries
        advisory_items = soup.find_all('div', class_='views-row') or soup.find_all('article')
        
        for item in advisory_items[:10]:  # Get top 10 recent advisories
            # Extract title and link
            title_link = item.find('a') or item.find('h3').find('a') if item.find('h3') else None
            if not title_link:
                continue
                
            advisory_info = {
                'title': title_link.get_text().strip(),
                'url': title_link.get('href')
            }
            
            # Ensure full URL
            if advisory_info['url'].startswith('/'):
                advisory_info['url'] = 'https://www.cisa.gov' + advisory_info['url']
            
            # Extract date
            date_element = item.find(text=re.compile(r'\w+ \d{1,2}, \d{4}'))
            if date_element:
                try:
                    date_str = date_element.strip()
                    advisory_info['date'] = datetime.datetime.strptime(
                        date_str, '%b %d, %Y'
                    ).strftime('%Y-%m-%d')
                except:
                    advisory_info['date'] = 'Unknown'
            else:
                advisory_info['date'] = 'Unknown'
            
            # Extract advisory type
            type_element = item.find(text=re.compile(r'(Alert|Advisory|ICS Advisory|Analysis Report)'))
            advisory_info['type'] = type_element.strip() if type_element else 'Advisory'
            
            advisories.append(advisory_info)
        
        return advisories
        
    except Exception as e:
        print(f"Error fetching CISA advisories: {e}")
        return []

def categorize_advisory_severity(advisory: Dict[str, Any]) -> str:
    """Categorize advisory by threat severity"""
    title = advisory.get('title', '').lower()
    advisory_type = advisory.get('type', '').lower()
    
    # Critical indicators
    critical_keywords = [
        'critical', 'urgent', 'immediate', 'active exploitation',
        'zero-day', 'nation-state', 'ransomware', 'widespread'
    ]
    
    # High indicators
    high_keywords = [
        'high', 'vulnerability', 'compromise', 'breach', 'attack',
        'malware', 'remote code execution', 'privilege escalation'
    ]
    
    # ICS advisories are often high priority
    if 'ics' in advisory_type:
        if any(keyword in title for keyword in critical_keywords):
            return "🔴 Critical"
        else:
            return "🟧 High"
    
    # Check for critical indicators
    if any(keyword in title for keyword in critical_keywords):
        return "🔴 Critical"
    
    # Check for high indicators
    elif any(keyword in title for keyword in high_keywords):
        return "🟧 High"
    
    # Alerts are typically medium to high
    elif 'alert' in advisory_type:
        return "🟡 Medium"
    
    # Analysis reports are informational
    elif 'analysis' in advisory_type:
        return "🔵 Anomaly"
    
    # Default to medium
    else:
        return "🟡 Medium"

def extract_advisory_indicators(title: str) -> Dict[str, List[str]]:
    """Extract threat indicators from advisory title"""
    indicators = {
        'vendors': [],
        'products': [],
        'threat_types': [],
        'sectors': []
    }
    
    # Common vendor patterns
    vendor_patterns = [
        r'Microsoft', r'Apple', r'Google', r'Adobe', r'Oracle', r'Cisco',
        r'VMware', r'Citrix', r'Fortinet', r'Palo Alto', r'SonicWall',
        r'Siemens', r'Schneider', r'Rockwell', r'GE', r'Honeywell'
    ]
    
    for pattern in vendor_patterns:
        if re.search(pattern, title, re.IGNORECASE):
            indicators['vendors'].append(pattern)
    
    # Common threat types
    threat_patterns = [
        r'ransomware', r'malware', r'phishing', r'vulnerability',
        r'backdoor', r'trojan', r'rootkit', r'botnet', r'ddos'
    ]
    
    for pattern in threat_patterns:
        if re.search(pattern, title, re.IGNORECASE):
            indicators['threat_types'].append(pattern)
    
    # Critical infrastructure sectors
    sector_patterns = [
        r'energy', r'water', r'transportation', r'healthcare',
        r'financial', r'manufacturing', r'communications',
        r'critical infrastructure', r'industrial'
    ]
    
    for pattern in sector_patterns:
        if re.search(pattern, title, re.IGNORECASE):
            indicators['sectors'].append(pattern)
    
    return indicators

def main():
    """Main collection function"""
    print("Collecting CISA advisories data...")
    
    # Get advisories list
    advisories = get_cisa_advisories()
    print(f"Found {len(advisories)} recent advisories")
    
    # Process and categorize advisories
    processed_advisories = []
    for advisory in advisories:
        advisory['severity'] = categorize_advisory_severity(advisory)
        advisory['indicators'] = extract_advisory_indicators(advisory['title'])
        processed_advisories.append(advisory)
    
    # Sort by severity
    severity_order = {"🔴 Critical": 0, "🟧 High": 1, "🔵 Anomaly": 2, "🟡 Medium": 3}
    processed_advisories.sort(key=lambda x: severity_order.get(x['severity'], 4))
    
    # Save results
    results = {
        'collection_timestamp': datetime.datetime.now().isoformat(),
        'total_advisories': len(processed_advisories),
        'advisories': processed_advisories
    }
    
    with open('cisa_advisories_data.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nCollected {len(processed_advisories)} CISA advisories:")
    for advisory in processed_advisories:
        print(f"- {advisory['severity']} [{advisory['type']}] {advisory['title'][:60]}...")
        if advisory['date'] != 'Unknown':
            print(f"  Date: {advisory['date']}")
    
    print("\nCISA advisories data collection complete. Results saved to cisa_advisories_data.json")

if __name__ == "__main__":
    main()

