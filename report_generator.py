


#!/usr/bin/env python3
"""
TURN Global Fusion Digest - Report Generator
Creates formatted operational and public reports from threat analysis data
"""

import json
import datetime
from typing import Dict, Any, List


OPERATIONAL_REPORT_TEMPLATE = """
# TURN [#] — GLOBAL FUSION DIGEST (OPERATIONAL REPORT)

**Date:** {date}
**Turn Number:** {turn_number}
**Analysis Timestamp:** {analysis_timestamp}

## 1. EXECUTIVE SUMMARY

This report provides a comprehensive overview of the current global threat landscape based on real-time intelligence from official government sources. Over the last 24 hours, **{total_threats_analyzed}** significant threats have been identified and analyzed, with a primary focus on vulnerabilities and threat actor activity impacting critical infrastructure and enterprise networks.

### Key Findings:
- **Severity Distribution:** {severity_distribution_summary}
- **Top Threat Actors:** {top_threat_actors}
- **Top Affected Vendors:** {top_vendors}
- **Most Common Vulnerabilities:** {top_cves}

## 2. THREAT INTELLIGENCE OVERVIEW

### 🔴 CRITICAL THREATS

{critical_threats}

### 🟧 HIGH-SEVERITY THREATS

{high_threats}

### 🔵 ANOMALIES & EMERGING THREATS

{anomaly_threats}

### 🟡 MEDIUM-SEVERITY THREATS

{medium_threats}

### ⚪ LOW-SEVERITY THREATS

{low_threats}

## 3. ✅ RESILIENCE TIPS

{resilience_tips}

## 4. 🚧 AD-HOC NOTES

- This report is automatically generated based on the latest available threat intelligence. Manual verification is recommended for critical decision-making.
- Threat actor attributions are based on information provided by government agencies and may be subject to change.

## 5. 📞 CONTACTS

- **CISA:** https://www.cisa.gov/report
- **FBI IC3:** https://www.ic3.gov
- **NSA Cybersecurity:** https://www.nsa.gov/cybersecurity/
"""

PUBLIC_BRIEF_TEMPLATE = """
# TURN [#] — GLOBAL FUSION DIGEST (PUBLIC BRIEF)

**Date:** {date}

Stay informed on the latest cybersecurity threats with our daily digest. Here are the key highlights from the last 24 hours:

### Key Threats:
{public_threats}

### ✅ Resilience Tip of the Day:
> {resilience_tip_of_the_day}

For more details, visit official sources:
- CISA: cisa.gov
- FBI: ic3.gov

#Cybersecurity #ThreatIntel #InfoSec #TURNReport
"""

def format_threat_details(threats: List[Dict[str, Any]]) -> str:
    """Formats a list of threats for the operational report."""
    if not threats:
        return "No significant threats identified in this category."
    
    formatted_threats = []
    for threat in threats:
        details = f"""
#### {threat['severity']} - {threat['title']}

- **Source:** {threat['source']}
- **ID:** {threat['threat_id']}
- **Date Added:** {threat['date_added']}
- **Description:** {threat['description']}
"""
        if threat.get('cves'):
            details += f"- **CVEs:** {', '.join(threat['cves'])}\n"
        if threat.get('threat_actors'):
           details += f"- **Threat Actors:** {', '.join(threat['threat_actors'])}\n"
        if threat.get('affected_vendors'):
           details += f"- **Affected Vendors:** {', '.join(threat['affected_vendors'])}\n"
        formatted_threats.append(details)
        
    return "\n".join(formatted_threats)

def format_public_threats(threats: List[Dict[str, Any]]) -> str:
    """Formats the top threats for the public brief."""
    if not threats:
        return "No major threats to report today."
        
    public_threats = []
    # Select top 3 critical/high threats for public brief
    top_threats = sorted(threats, key=lambda x: ('🔴' not in x['severity'], '🟧' not in x['severity']))[:3]
    
    for threat in top_threats:
        public_threats.append(f"- **{threat['severity']} {threat['title']}**: {threat['description'][:100]}...")
        
    return "\n".join(public_threats)

def main():
    """Main report generation function."""
    print("Generating TURN Global Fusion Digest reports...")
    
    # Load analysis results
    try:
        with open('threat_analysis_results.json', 'r') as f:
            analysis_data = json.load(f)
    except FileNotFoundError:
        print("Threat analysis results not found. Please run the analysis engine first.")
        return

    # Prepare data for templates
    turn_number = datetime.datetime.now().strftime('%Y%m%d')
    report_date = datetime.datetime.now().strftime('%Y-%m-%d')
    analysis_timestamp = analysis_data.get('analysis_timestamp', 'Unknown')
    consolidated = analysis_data.get('consolidated_analysis', {})
    threat_details = analysis_data.get('threat_details', [])

    severity_dist = consolidated.get('severity_distribution', {})
    severity_summary = ", ".join([f"{count} {sev}" for sev, count in severity_dist.items()])

    # --- Generate Operational Report ---
    operational_report = OPERATIONAL_REPORT_TEMPLATE.format(
        date=report_date,
        turn_number=turn_number,
        analysis_timestamp=analysis_timestamp,
        total_threats_analyzed=consolidated.get('total_threats', 0),
        severity_distribution_summary=severity_summary,
        top_threat_actors=", ".join([f"{actor[0]} ({actor[1]})" for actor in consolidated.get('top_threat_actors', [])]),
        top_vendors=", ".join([f"{vendor[0]} ({vendor[1]})" for vendor in consolidated.get('top_vendors', [])]),
        top_cves=", ".join([f"{cve[0]} ({cve[1]})" for cve in consolidated.get('top_cves', [])]),
        critical_threats=format_threat_details([t for t in threat_details if '🔴' in t['severity']]),
        high_threats=format_threat_details([t for t in threat_details if '🟧' in t['severity']]),
        anomaly_threats=format_threat_details([t for t in threat_details if '🔵' in t['severity']]),
        medium_threats=format_threat_details([t for t in threat_details if '🟡' in t['severity']]),
        low_threats=format_threat_details([t for t in threat_details if '⚪' in t['severity']]),
        resilience_tips="\n".join([f"- {tip}" for tip in analysis_data.get('resilience_tips', [])])
    )

    with open(f"TURN_{turn_number}_Operational_Report.md", "w") as f:
        f.write(operational_report)

    # --- Generate Public Brief ---
    public_brief = PUBLIC_BRIEF_TEMPLATE.format(
        date=report_date,
        public_threats=format_public_threats(threat_details),
        resilience_tip_of_the_day=analysis_data.get('resilience_tips', ["Stay vigilant."])[0]
    )

    with open(f"TURN_{turn_number}_Public_Brief.md", "w") as f:
        f.write(public_brief)

    print("Reports generated successfully:")
    print(f"- TURN_{turn_number}_Operational_Report.md")
    print(f"- TURN_{turn_number}_Public_Brief.md")

if __name__ == "__main__":
    main()


