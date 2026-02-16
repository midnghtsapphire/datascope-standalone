#!/usr/bin/env python3
"""
TURN Global Fusion Digest - Threat Analysis Engine
Comprehensive threat categorization and analysis system for automated reporting
"""

import json
import datetime
import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class ThreatSeverity(Enum):
    CRITICAL = ("🔴", "Critical", 0)
    HIGH = ("🟧", "High", 1)
    ANOMALY = ("🔵", "Anomaly", 2)
    MEDIUM = ("🟡", "Medium", 3)
    LOW = ("⚪", "Low", 4)
    
    def __init__(self, emoji, display_name, priority):
        self.emoji = emoji
        self.display_name = display_name
        self.priority = priority

@dataclass
class ThreatIndicator:
    """Represents a threat indicator with metadata"""
    source: str
    threat_id: str
    title: str
    description: str
    severity: ThreatSeverity
    date_added: str
    due_date: str = None
    threat_actors: List[str] = None
    cves: List[str] = None
    affected_vendors: List[str] = None
    affected_products: List[str] = None
    sectors: List[str] = None
    mitigation: str = None
    confidence: float = 1.0
    
    def __post_init__(self):
        if self.threat_actors is None:
            self.threat_actors = []
        if self.cves is None:
            self.cves = []
        if self.affected_vendors is None:
            self.affected_vendors = []
        if self.affected_products is None:
            self.affected_products = []
        if self.sectors is None:
            self.sectors = []

class ThreatAnalysisEngine:
    """Main threat analysis and categorization engine"""
    
    def __init__(self):
        self.critical_keywords = [
            'critical infrastructure', 'nation-state', 'ransomware', 'zero-day',
            'active exploitation', 'immediate', 'urgent', 'widespread',
            'remote code execution', 'privilege escalation', 'authentication bypass'
        ]
        
        self.high_keywords = [
            'vulnerability', 'compromise', 'breach', 'attack', 'malware',
            'phishing', 'scam', 'fraud', 'backdoor', 'trojan', 'botnet'
        ]
        
        self.anomaly_keywords = [
            'new', 'emerging', 'novel', 'unusual', 'unknown', 'sophisticated',
            'advanced persistent threat', 'apt', 'campaign'
        ]
        
        self.nation_state_actors = [
            'apt1', 'apt28', 'apt29', 'apt40', 'lazarus', 'fancy bear', 'cozy bear',
            'dragonfly', 'berserk bear', 'static tundra', 'russian', 'chinese',
            'north korean', 'iranian', 'fsb', 'gru', 'mss', 'pla'
        ]
        
        self.critical_sectors = [
            'energy', 'water', 'transportation', 'healthcare', 'financial',
            'manufacturing', 'communications', 'defense', 'government'
        ]
    
    def analyze_kev_vulnerability(self, vuln: Dict[str, Any]) -> ThreatIndicator:
        """Analyze a CISA KEV vulnerability"""
        # Calculate time-based severity
        date_added = datetime.datetime.strptime(vuln['dateAdded'], '%Y-%m-%d')
        due_date = datetime.datetime.strptime(vuln['dueDate'], '%Y-%m-%d')
        days_to_due = (due_date - datetime.datetime.now()).days
        days_since_added = (datetime.datetime.now() - date_added).days
        
        # Determine severity
        severity = ThreatSeverity.MEDIUM
        
        # Critical conditions
        if (vuln.get('knownRansomwareCampaignUse', '').lower() == 'known' or
            days_to_due <= 7 or
            days_since_added <= 3 or
            any(keyword in vuln['shortDescription'].lower() for keyword in self.critical_keywords)):
            severity = ThreatSeverity.CRITICAL
        
        # High conditions
        elif (days_to_due <= 21 or
              days_since_added <= 7 or
              any(keyword in vuln['shortDescription'].lower() for keyword in self.high_keywords)):
            severity = ThreatSeverity.HIGH
        
        # Medium conditions
        elif days_to_due <= 45:
            severity = ThreatSeverity.MEDIUM
        
        # Low conditions
        else:
            severity = ThreatSeverity.LOW
        
        return ThreatIndicator(
            source="CISA KEV",
            threat_id=vuln['cveID'],
            title=vuln['vulnerabilityName'],
            description=vuln['shortDescription'],
            severity=severity,
            date_added=vuln['dateAdded'],
            due_date=vuln['dueDate'],
            cves=[vuln['cveID']],
            affected_vendors=[vuln['vendorProject']],
            affected_products=[vuln['product']],
            mitigation=vuln['requiredAction']
        )
    
    def analyze_ic3_psa(self, psa: Dict[str, Any]) -> ThreatIndicator:
        """Analyze an FBI IC3 PSA"""
        title = psa.get('title', '').lower()
        content = psa.get('content', '').lower()
        
        # Determine severity
        severity = ThreatSeverity.MEDIUM
        
        # Critical conditions
        if (any(keyword in title or keyword in content for keyword in self.critical_keywords) or
            any(actor in content for actor in self.nation_state_actors) or
            any(sector in content for sector in self.critical_sectors)):
            severity = ThreatSeverity.CRITICAL
        
        # High conditions
        elif any(keyword in title or keyword in content for keyword in self.high_keywords):
            severity = ThreatSeverity.HIGH
        
        # Anomaly conditions
        elif any(keyword in title for keyword in self.anomaly_keywords):
            severity = ThreatSeverity.ANOMALY
        
        # Extract threat actors
        threat_actors = []
        for actor in self.nation_state_actors:
            if actor in content:
                threat_actors.append(actor.title())
        
        return ThreatIndicator(
            source="FBI IC3",
            threat_id=psa.get('psa_id', 'Unknown'),
            title=psa.get('title', 'Unknown'),
            description=psa.get('content', '')[:500],  # Limit description
            severity=severity,
            date_added=psa.get('date', 'Unknown'),
            threat_actors=threat_actors,
            cves=psa.get('threat_indicators', {}).get('cves', []),
            sectors=psa.get('threat_indicators', {}).get('sectors', [])
        )
    
    def analyze_cisa_advisory(self, advisory: Dict[str, Any]) -> ThreatIndicator:
        """Analyze a CISA advisory"""
        title = advisory.get('title', '').lower()
        advisory_type = advisory.get('type', '').lower()
        
        # Determine severity
        severity = ThreatSeverity.MEDIUM
        
        # Critical conditions for ICS advisories
        if ('ics' in advisory_type and
            any(keyword in title for keyword in self.critical_keywords)):
            severity = ThreatSeverity.CRITICAL
        
        # High conditions
        elif ('ics' in advisory_type or
              any(keyword in title for keyword in self.high_keywords)):
            severity = ThreatSeverity.HIGH
        
        # Anomaly conditions for analysis reports
        elif 'analysis' in advisory_type:
            severity = ThreatSeverity.ANOMALY
        
        # Alert conditions
        elif 'alert' in advisory_type:
            severity = ThreatSeverity.MEDIUM
        
        return ThreatIndicator(
            source="CISA Advisory",
            threat_id=advisory.get('url', '').split('/')[-1],
            title=advisory.get('title', 'Unknown'),
            description=f"{advisory_type.title()}: {advisory.get('title', '')}",
            severity=severity,
            date_added=advisory.get('date', 'Unknown'),
            affected_vendors=advisory.get('indicators', {}).get('vendors', []),
            sectors=advisory.get('indicators', {}).get('sectors', [])
        )
    
    def consolidate_threats(self, threats: List[ThreatIndicator]) -> Dict[str, Any]:
        """Consolidate and analyze threat patterns"""
        # Group by severity
        severity_groups = {}
        for severity in ThreatSeverity:
            severity_groups[severity] = [t for t in threats if t.severity == severity]
        
        # Analyze patterns
        all_threat_actors = []
        all_cves = []
        all_vendors = []
        all_sectors = []
        
        for threat in threats:
            all_threat_actors.extend(threat.threat_actors)
            all_cves.extend(threat.cves)
            all_vendors.extend(threat.affected_vendors)
            all_sectors.extend(threat.sectors)
        
        # Count occurrences
        from collections import Counter
        actor_counts = Counter(all_threat_actors)
        cve_counts = Counter(all_cves)
        vendor_counts = Counter(all_vendors)
        sector_counts = Counter(all_sectors)
        
        return {
            'total_threats': len(threats),
            'severity_distribution': {
                severity.display_name: len(threats_list) 
                for severity, threats_list in severity_groups.items()
            },
            'top_threat_actors': actor_counts.most_common(5),
            'top_cves': cve_counts.most_common(10),
            'top_vendors': vendor_counts.most_common(10),
            'top_sectors': sector_counts.most_common(5),
            'threats_by_severity': {
                severity.display_name: [
                    {
                        'source': t.source,
                        'id': t.threat_id,
                        'title': t.title,
                        'date': t.date_added,
                        'cves': t.cves,
                        'actors': t.threat_actors
                    }
                    for t in threats_list
                ]
                for severity, threats_list in severity_groups.items()
            }
        }
    
    def generate_resilience_tips(self, threats: List[ThreatIndicator]) -> List[str]:
        """Generate contextual resilience tips based on current threats"""
        tips = []
        
        # Analyze threat patterns to generate relevant tips
        has_ransomware = any('ransomware' in t.description.lower() for t in threats)
        has_nation_state = any(t.threat_actors for t in threats)
        has_ics = any('ics' in t.source.lower() for t in threats)
        has_recent_cves = any(t.cves for t in threats)
        
        if has_ransomware:
            tips.append("Implement robust backup strategies with offline copies and regular restoration testing")
            tips.append("Deploy endpoint detection and response (EDR) solutions with behavioral analysis")
        
        if has_nation_state:
            tips.append("Enhance network segmentation and implement zero-trust architecture principles")
            tips.append("Conduct regular threat hunting exercises focusing on advanced persistent threats")
        
        if has_ics:
            tips.append("Isolate operational technology (OT) networks from corporate IT infrastructure")
            tips.append("Implement industrial control system security monitoring and anomaly detection")
        
        if has_recent_cves:
            tips.append("Prioritize patching for vulnerabilities in the CISA KEV catalog")
            tips.append("Establish vulnerability management processes with risk-based prioritization")
        
        # Add general tips
        tips.extend([
            "Enable multi-factor authentication (MFA) for all administrative and remote access",
            "Maintain current incident response plans and conduct regular tabletop exercises",
            "Implement security awareness training focusing on current threat landscapes"
        ])
        
        return tips[:5]  # Return top 5 tips

def main():
    """Main analysis function"""
    print("Initializing TURN Threat Analysis Engine...")
    
    engine = ThreatAnalysisEngine()
    all_threats = []
    
    # Load and analyze KEV data
    try:
        with open('kev_analysis_results.json', 'r') as f:
            kev_data = json.load(f)
        
        print(f"Analyzing {len(kev_data['recent_threats'])} recent KEV threats...")
        for vuln in kev_data['recent_threats']:
            threat = engine.analyze_kev_vulnerability(vuln)
            all_threats.append(threat)
    except FileNotFoundError:
        print("KEV analysis results not found")
    
    # Load and analyze IC3 PSA data
    try:
        with open('ic3_psa_data.json', 'r') as f:
            ic3_data = json.load(f)
        
        print(f"Analyzing {len(ic3_data['detailed_psas'])} IC3 PSAs...")
        for psa in ic3_data['detailed_psas']:
            threat = engine.analyze_ic3_psa(psa)
            all_threats.append(threat)
    except FileNotFoundError:
        print("IC3 PSA data not found")
    
    # Load and analyze CISA advisories
    try:
        with open('cisa_advisories_data.json', 'r') as f:
            cisa_data = json.load(f)
        
        print(f"Analyzing {len(cisa_data['advisories'])} CISA advisories...")
        for advisory in cisa_data['advisories']:
            threat = engine.analyze_cisa_advisory(advisory)
            all_threats.append(threat)
    except FileNotFoundError:
        print("CISA advisories data not found")
    
    # Consolidate analysis
    print(f"\nConsolidating analysis for {len(all_threats)} total threats...")
    consolidated = engine.consolidate_threats(all_threats)
    
    # Generate resilience tips
    resilience_tips = engine.generate_resilience_tips(all_threats)
    
    # Prepare final analysis results
    analysis_results = {
        'analysis_timestamp': datetime.datetime.now().isoformat(),
        'total_threats_analyzed': len(all_threats),
        'consolidated_analysis': consolidated,
        'resilience_tips': resilience_tips,
        'threat_details': [
            {
                'source': t.source,
                'threat_id': t.threat_id,
                'title': t.title,
                'severity': f"{t.severity.emoji} {t.severity.display_name}",
                'date_added': t.date_added,
                'due_date': t.due_date,
                'description': t.description[:200],
                'cves': t.cves,
                'threat_actors': t.threat_actors,
                'affected_vendors': t.affected_vendors,
                'sectors': t.sectors
            }
            for t in sorted(all_threats, key=lambda x: x.severity.priority)
        ]
    }
    
    # Save results
    with open('threat_analysis_results.json', 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    # Display summary
    print("\n" + "="*60)
    print("THREAT ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"Total Threats Analyzed: {len(all_threats)}")
    print("\nSeverity Distribution:")
    for severity, count in consolidated['severity_distribution'].items():
        # Find the enum member by display_name
        severity_enum = next(s for s in ThreatSeverity if s.display_name == severity)
        emoji = severity_enum.emoji
        print(f"  {emoji} {severity}: {count}")
    
    print(f"\nTop Threat Actors:")
    for actor, count in consolidated['top_threat_actors']:
        print(f"  - {actor}: {count} mentions")
    
    print(f"\nTop Affected Vendors:")
    for vendor, count in consolidated['top_vendors'][:5]:
        print(f"  - {vendor}: {count} threats")
    
    print(f"\nResilience Tips Generated: {len(resilience_tips)}")
    for i, tip in enumerate(resilience_tips, 1):
        print(f"  {i}. {tip}")
    
    print(f"\nAnalysis complete. Results saved to threat_analysis_results.json")

if __name__ == "__main__":
    main()

