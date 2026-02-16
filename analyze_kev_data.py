#!/usr/bin/env python3
"""
CISA KEV Data Analysis Script
Analyzes the Known Exploited Vulnerabilities catalog for threat intelligence reporting
"""

import json
import datetime
from collections import defaultdict
from typing import Dict, List, Any

def load_kev_data(filename: str) -> Dict[str, Any]:
    """Load KEV JSON data from file"""
    with open(filename, 'r') as f:
        return json.load(f)

def categorize_threat_severity(vuln: Dict[str, Any]) -> str:
    """Categorize vulnerability by threat severity"""
    date_added = datetime.datetime.strptime(vuln['dateAdded'], '%Y-%m-%d')
    due_date = datetime.datetime.strptime(vuln['dueDate'], '%Y-%m-%d')
    days_to_due = (due_date - datetime.datetime.now()).days
    
    # Critical: Recent additions with short due dates or known ransomware use
    if (vuln.get('knownRansomwareCampaignUse', '').lower() == 'known' or 
        days_to_due <= 7 or 
        (datetime.datetime.now() - date_added).days <= 3):
        return "🔴 Critical"
    
    # High: Recent additions or short due dates
    elif days_to_due <= 21 or (datetime.datetime.now() - date_added).days <= 7:
        return "🟧 High"
    
    # Medium: Standard timeframes
    elif days_to_due <= 45:
        return "🟡 Medium"
    
    # Low: Extended timeframes
    else:
        return "⚪ Low"

def analyze_recent_threats(kev_data: Dict[str, Any], days_back: int = 30) -> List[Dict[str, Any]]:
    """Analyze threats added in the last N days"""
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_back)
    recent_threats = []
    
    for vuln in kev_data['vulnerabilities']:
        date_added = datetime.datetime.strptime(vuln['dateAdded'], '%Y-%m-%d')
        if date_added >= cutoff_date:
            vuln_analysis = vuln.copy()
            vuln_analysis['severity'] = categorize_threat_severity(vuln)
            vuln_analysis['days_since_added'] = (datetime.datetime.now() - date_added).days
            recent_threats.append(vuln_analysis)
    
    # Sort by severity and recency
    severity_order = {"🔴 Critical": 0, "🟧 High": 1, "🟡 Medium": 2, "⚪ Low": 3}
    recent_threats.sort(key=lambda x: (severity_order[x['severity']], x['days_since_added']))
    
    return recent_threats

def generate_threat_summary(kev_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate summary statistics for threat intelligence"""
    total_vulns = kev_data['count']
    catalog_version = kev_data['catalogVersion']
    date_released = kev_data['dateReleased']
    
    # Analyze by vendor/product
    vendor_stats = defaultdict(int)
    product_stats = defaultdict(int)
    severity_stats = defaultdict(int)
    
    for vuln in kev_data['vulnerabilities']:
        vendor_stats[vuln['vendorProject']] += 1
        product_stats[vuln['product']] += 1
        severity = categorize_threat_severity(vuln)
        severity_stats[severity] += 1
    
    # Get top vendors and products
    top_vendors = sorted(vendor_stats.items(), key=lambda x: x[1], reverse=True)[:10]
    top_products = sorted(product_stats.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        'total_vulnerabilities': total_vulns,
        'catalog_version': catalog_version,
        'date_released': date_released,
        'severity_distribution': dict(severity_stats),
        'top_vendors': top_vendors,
        'top_products': top_products
    }

def main():
    """Main analysis function"""
    print("Analyzing CISA KEV Data...")
    
    # Load KEV data
    kev_data = load_kev_data('cisa_kev_current.json')
    
    # Generate summary
    summary = generate_threat_summary(kev_data)
    print(f"Total Vulnerabilities: {summary['total_vulnerabilities']}")
    print(f"Catalog Version: {summary['catalog_version']}")
    print(f"Date Released: {summary['date_released']}")
    
    print("\nSeverity Distribution:")
    for severity, count in summary['severity_distribution'].items():
        print(f"  {severity}: {count}")
    
    # Analyze recent threats (last 30 days)
    recent_threats = analyze_recent_threats(kev_data, 30)
    print(f"\nRecent Threats (Last 30 days): {len(recent_threats)}")
    
    # Save detailed analysis
    analysis_results = {
        'summary': summary,
        'recent_threats': recent_threats[:20],  # Top 20 most critical recent threats
        'analysis_timestamp': datetime.datetime.now().isoformat()
    }
    
    with open('kev_analysis_results.json', 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    print("\nTop 10 Most Critical Recent Threats:")
    for i, threat in enumerate(recent_threats[:10], 1):
        print(f"{i}. {threat['severity']} - {threat['cveID']}")
        print(f"   {threat['vendorProject']} {threat['product']}")
        print(f"   Added: {threat['dateAdded']} | Due: {threat['dueDate']}")
        print(f"   {threat['shortDescription'][:100]}...")
        print()
    
    print("Analysis complete. Results saved to kev_analysis_results.json")

if __name__ == "__main__":
    main()

