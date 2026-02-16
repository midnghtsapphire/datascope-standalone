#!/usr/bin/env python3
"""
FBI IC3 PSA Data Collection Script
Collects recent Public Service Announcements for threat intelligence reporting
"""

import requests
from bs4 import BeautifulSoup
import json
import datetime
import re
from typing import List, Dict, Any

def get_ic3_psa_list() -> List[Dict[str, Any]]:
    """Scrape IC3 PSA list page for recent announcements"""
    url = "https://www.ic3.gov/PSA"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        psa_list = []
        
        # Find PSA links and dates
        psa_links = soup.find_all('a', href=re.compile(r'/PSA/\d{4}/PSA\d+'))
        
        for link in psa_links[:10]:  # Get top 10 recent PSAs
            psa_info = {
                'title': link.get_text().strip(),
                'url': 'https://www.ic3.gov' + link.get('href'),
                'psa_id': link.get('href').split('/')[-1]
            }
            
            # Try to find date from surrounding elements
            date_element = link.find_next('li') or link.find_previous('li')
            if date_element:
                date_text = date_element.get_text()
                # Extract date pattern
                date_match = re.search(r'(\w{3}, \d{2} \w{3} \d{4})', date_text)
                if date_match:
                    try:
                        psa_info['date'] = datetime.datetime.strptime(
                            date_match.group(1), '%a, %d %b %Y'
                        ).strftime('%Y-%m-%d')
                    except:
                        psa_info['date'] = 'Unknown'
                else:
                    psa_info['date'] = 'Unknown'
            
            psa_list.append(psa_info)
        
        return psa_list
        
    except Exception as e:
        print(f"Error fetching IC3 PSA list: {e}")
        return []

def get_psa_details(psa_url: str) -> Dict[str, Any]:
    """Get detailed content from a specific PSA"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(psa_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('h1')
        title_text = title.get_text().strip() if title else "Unknown Title"
        
        # Extract alert number and date
        alert_info = soup.find(text=re.compile(r'Alert Number:'))
        alert_number = "Unknown"
        alert_date = "Unknown"
        
        if alert_info:
            alert_text = alert_info.parent.get_text()
            alert_match = re.search(r'Alert Number:\s*([^\n]+)', alert_text)
            date_match = re.search(r'(\w+ \d{1,2}, \d{4})', alert_text)
            
            if alert_match:
                alert_number = alert_match.group(1).strip()
            if date_match:
                alert_date = date_match.group(1).strip()
        
        # Extract main content
        content_div = soup.find('div', class_='field-item') or soup.find('div', id='content')
        content_text = ""
        if content_div:
            # Remove script and style elements
            for script in content_div(["script", "style"]):
                script.decompose()
            content_text = content_div.get_text().strip()
        
        # Extract threat indicators
        threat_indicators = extract_threat_indicators(content_text)
        
        return {
            'title': title_text,
            'alert_number': alert_number,
            'alert_date': alert_date,
            'content': content_text[:2000],  # Limit content length
            'threat_indicators': threat_indicators,
            'url': psa_url
        }
        
    except Exception as e:
        print(f"Error fetching PSA details from {psa_url}: {e}")
        return {}

def extract_threat_indicators(content: str) -> Dict[str, List[str]]:
    """Extract threat indicators from PSA content"""
    indicators = {
        'cves': [],
        'threat_actors': [],
        'malware': [],
        'domains': [],
        'ips': []
    }
    
    # Extract CVEs
    cve_pattern = r'CVE-\d{4}-\d{4,7}'
    indicators['cves'] = list(set(re.findall(cve_pattern, content, re.IGNORECASE)))
    
    # Extract common threat actor names
    threat_actor_patterns = [
        r'APT\d+', r'Lazarus', r'Fancy Bear', r'Cozy Bear', r'Dragonfly',
        r'Berserk Bear', r'Static Tundra', r'Russian', r'Chinese', r'North Korean',
        r'Iranian', r'FSB', r'GRU', r'MSS'
    ]
    
    for pattern in threat_actor_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        indicators['threat_actors'].extend(matches)
    
    # Extract domain patterns (simplified)
    domain_pattern = r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.([a-zA-Z]{2,})\b'
    potential_domains = re.findall(domain_pattern, content)
    # Filter for suspicious domains (basic filtering)
    for domain_parts in potential_domains:
        domain = '.'.join(domain_parts)
        if any(suspicious in domain.lower() for suspicious in ['malware', 'phish', 'scam', 'fake']):
            indicators['domains'].append(domain)
    
    # Extract IP addresses
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    indicators['ips'] = list(set(re.findall(ip_pattern, content)))
    
    # Remove duplicates and clean up
    for key in indicators:
        indicators[key] = list(set(indicators[key]))
    
    return indicators

def categorize_psa_severity(psa: Dict[str, Any]) -> str:
    """Categorize PSA by threat severity"""
    title = psa.get('title', '').lower()
    content = psa.get('content', '').lower()
    
    # Critical indicators
    critical_keywords = [
        'critical infrastructure', 'nation-state', 'ransomware', 'zero-day',
        'active exploitation', 'immediate', 'urgent', 'widespread'
    ]
    
    # High indicators
    high_keywords = [
        'vulnerability', 'compromise', 'breach', 'attack', 'malware',
        'phishing', 'scam', 'fraud'
    ]
    
    # Check for critical indicators
    if any(keyword in title or keyword in content for keyword in critical_keywords):
        return "🔴 Critical"
    
    # Check for high indicators
    elif any(keyword in title or keyword in content for keyword in high_keywords):
        return "🟧 High"
    
    # Check for anomaly indicators (unusual patterns)
    elif any(word in title for word in ['new', 'emerging', 'novel', 'unusual']):
        return "🔵 Anomaly"
    
    # Default to medium
    else:
        return "🟡 Medium"

def main():
    """Main collection function"""
    print("Collecting FBI IC3 PSA data...")
    
    # Get PSA list
    psa_list = get_ic3_psa_list()
    print(f"Found {len(psa_list)} recent PSAs")
    
    # Get detailed information for each PSA
    detailed_psas = []
    for psa in psa_list[:5]:  # Limit to top 5 to avoid overwhelming the server
        print(f"Fetching details for: {psa['title'][:50]}...")
        details = get_psa_details(psa['url'])
        if details:
            details.update(psa)
            details['severity'] = categorize_psa_severity(details)
            detailed_psas.append(details)
    
    # Save results
    results = {
        'collection_timestamp': datetime.datetime.now().isoformat(),
        'total_psas_found': len(psa_list),
        'detailed_psas': detailed_psas
    }
    
    with open('ic3_psa_data.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nCollected {len(detailed_psas)} detailed PSAs:")
    for psa in detailed_psas:
        print(f"- {psa['severity']} {psa['title'][:60]}...")
        if psa.get('threat_indicators', {}).get('cves'):
            print(f"  CVEs: {', '.join(psa['threat_indicators']['cves'])}")
        if psa.get('threat_indicators', {}).get('threat_actors'):
            print(f"  Threat Actors: {', '.join(psa['threat_indicators']['threat_actors'][:3])}")
    
    print("\nIC3 PSA data collection complete. Results saved to ic3_psa_data.json")

if __name__ == "__main__":
    main()

