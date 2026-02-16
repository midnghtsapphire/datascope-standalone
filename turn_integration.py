#!/usr/bin/env python3
"""
TURN Integration Module for DataScope Enhanced
Bridges the original TURN Global Fusion Digest modules with the enhanced platform
"""

import sys
import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add current directory to path for TURN module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from threat_analysis_engine import ThreatAnalysisEngine
    from threat_intel import ThreatIntelCollector
    from analyze_kev_data import analyze_kev_data
    from collect_cisa_advisories import collect_cisa_advisories
    from collect_ic3_data import collect_ic3_data
    TURN_MODULES_AVAILABLE = True
except ImportError as e:
    logging.warning(f"TURN modules not fully available: {e}")
    TURN_MODULES_AVAILABLE = False

class TURNIntegration:
    """
    Integration layer between TURN Global Fusion Digest and DataScope Enhanced
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.turn_available = TURN_MODULES_AVAILABLE
        
        if self.turn_available:
            try:
                self.threat_analyzer = ThreatAnalysisEngine()
                self.threat_collector = ThreatIntelCollector()
                self.logger.info("TURN modules initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize TURN modules: {e}")
                self.turn_available = False
        else:
            self.logger.warning("TURN modules not available - using basic analysis")
    
    def is_available(self) -> bool:
        """Check if TURN modules are available"""
        return self.turn_available
    
    def collect_cybersecurity_data(self, location: Optional[str] = None) -> Dict[str, Any]:
        """
        Collect cybersecurity data using TURN methods
        
        Args:
            location: Geographic location filter (e.g., 'federal', 'state')
            
        Returns:
            Dictionary containing collected threat intelligence data
        """
        if not self.turn_available:
            return self._fallback_cybersecurity_collection(location)
        
        try:
            # Use TURN collection methods
            results = {
                'collection_timestamp': datetime.now().isoformat(),
                'location': location,
                'sources': [],
                'data': [],
                'total_items_collected': 0
            }
            
            # Collect CISA KEV data
            try:
                kev_data = self._collect_kev_data()
                if kev_data:
                    results['sources'].append('CISA KEV')
                    results['data'].extend(kev_data)
                    results['total_items_collected'] += len(kev_data)
            except Exception as e:
                self.logger.error(f"Failed to collect KEV data: {e}")
            
            # Collect FBI IC3 data
            try:
                ic3_data = self._collect_ic3_data()
                if ic3_data:
                    results['sources'].append('FBI IC3')
                    results['data'].extend(ic3_data)
                    results['total_items_collected'] += len(ic3_data)
            except Exception as e:
                self.logger.error(f"Failed to collect IC3 data: {e}")
            
            # Collect CISA advisories
            try:
                advisory_data = self._collect_cisa_advisories()
                if advisory_data:
                    results['sources'].append('CISA Advisories')
                    results['data'].extend(advisory_data)
                    results['total_items_collected'] += len(advisory_data)
            except Exception as e:
                self.logger.error(f"Failed to collect CISA advisories: {e}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"TURN data collection failed: {e}")
            return self._fallback_cybersecurity_collection(location)
    
    def analyze_threats(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze threats using TURN threat analysis engine
        
        Args:
            data: List of threat data to analyze
            
        Returns:
            Dictionary containing threat analysis results
        """
        if not self.turn_available or not data:
            return self._fallback_threat_analysis(data)
        
        try:
            # Use TURN threat analysis
            analysis_results = self.threat_analyzer.analyze_threats(data)
            
            # Enhance with additional analysis
            enhanced_analysis = {
                'analysis_timestamp': datetime.now().isoformat(),
                'total_threats_analyzed': len(data),
                'turn_analysis': analysis_results,
                'severity_distribution': self._calculate_severity_distribution(data),
                'top_vendors': self._get_top_vendors(data),
                'top_threat_actors': self._get_top_threat_actors(data),
                'recent_trends': self._analyze_trends(data)
            }
            
            return enhanced_analysis
            
        except Exception as e:
            self.logger.error(f"TURN threat analysis failed: {e}")
            return self._fallback_threat_analysis(data)
    
    def generate_turn_report(self, analysis_data: Dict[str, Any], report_type: str = 'operational') -> str:
        """
        Generate TURN-style report
        
        Args:
            analysis_data: Analyzed threat data
            report_type: Type of report ('operational', 'public', 'executive')
            
        Returns:
            Path to generated report file
        """
        if not self.turn_available:
            return self._fallback_report_generation(analysis_data, report_type)
        
        try:
            # Generate TURN-style report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            turn_number = self._generate_turn_number()
            
            if report_type == 'operational':
                report_content = self._generate_operational_report(analysis_data, turn_number)
                filename = f"TURN_{turn_number}_Operational_Report_{timestamp}.md"
            elif report_type == 'public':
                report_content = self._generate_public_brief(analysis_data, turn_number)
                filename = f"TURN_{turn_number}_Public_Brief_{timestamp}.md"
            else:
                report_content = self._generate_executive_summary(analysis_data, turn_number)
                filename = f"TURN_{turn_number}_Executive_Summary_{timestamp}.md"
            
            # Write report to file
            report_path = os.path.join('reports', filename)
            os.makedirs('reports', exist_ok=True)
            
            with open(report_path, 'w') as f:
                f.write(report_content)
            
            self.logger.info(f"TURN report generated: {report_path}")
            return report_path
            
        except Exception as e:
            self.logger.error(f"TURN report generation failed: {e}")
            return self._fallback_report_generation(analysis_data, report_type)
    
    def _collect_kev_data(self) -> List[Dict[str, Any]]:
        """Collect CISA KEV data using TURN methods"""
        try:
            # Use the original TURN KEV collection
            kev_results = analyze_kev_data()
            return kev_results if kev_results else []
        except Exception as e:
            self.logger.error(f"KEV collection failed: {e}")
            return []
    
    def _collect_ic3_data(self) -> List[Dict[str, Any]]:
        """Collect FBI IC3 data using TURN methods"""
        try:
            # Use the original TURN IC3 collection
            ic3_results = collect_ic3_data()
            return ic3_results if ic3_results else []
        except Exception as e:
            self.logger.error(f"IC3 collection failed: {e}")
            return []
    
    def _collect_cisa_advisories(self) -> List[Dict[str, Any]]:
        """Collect CISA advisories using TURN methods"""
        try:
            # Use the original TURN CISA advisory collection
            advisory_results = collect_cisa_advisories()
            return advisory_results if advisory_results else []
        except Exception as e:
            self.logger.error(f"CISA advisory collection failed: {e}")
            return []
    
    def _calculate_severity_distribution(self, data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate severity distribution from threat data"""
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'unknown': 0}
        
        for item in data:
            severity = item.get('severity', '').lower()
            if 'critical' in severity:
                severity_counts['critical'] += 1
            elif 'high' in severity:
                severity_counts['high'] += 1
            elif 'medium' in severity:
                severity_counts['medium'] += 1
            elif 'low' in severity:
                severity_counts['low'] += 1
            else:
                severity_counts['unknown'] += 1
        
        return severity_counts
    
    def _get_top_vendors(self, data: List[Dict[str, Any]], limit: int = 10) -> List[tuple]:
        """Get top affected vendors from threat data"""
        vendor_counts = {}
        
        for item in data:
            vendor = item.get('vendorproject', item.get('vendor', 'Unknown'))
            vendor_counts[vendor] = vendor_counts.get(vendor, 0) + 1
        
        return sorted(vendor_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    def _get_top_threat_actors(self, data: List[Dict[str, Any]], limit: int = 10) -> List[tuple]:
        """Get top threat actors from threat data"""
        actor_counts = {}
        
        for item in data:
            actors = item.get('threat_actors', [])
            if isinstance(actors, str):
                actors = [actors]
            
            for actor in actors:
                if actor and actor != 'Unknown':
                    actor_counts[actor] = actor_counts.get(actor, 0) + 1
        
        return sorted(actor_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    def _analyze_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends in threat data"""
        trends = {
            'total_threats': len(data),
            'recent_threats': len([item for item in data if self._is_recent(item)]),
            'trending_cves': self._get_trending_cves(data),
            'emerging_threats': self._identify_emerging_threats(data)
        }
        
        return trends
    
    def _is_recent(self, item: Dict[str, Any], days: int = 7) -> bool:
        """Check if threat item is recent"""
        try:
            date_added = item.get('dateadded', item.get('date_added', ''))
            if date_added:
                item_date = datetime.strptime(date_added, '%Y-%m-%d')
                return (datetime.now() - item_date).days <= days
        except:
            pass
        return False
    
    def _get_trending_cves(self, data: List[Dict[str, Any]], limit: int = 5) -> List[str]:
        """Get trending CVEs from threat data"""
        cve_counts = {}
        
        for item in data:
            cve = item.get('cveid', item.get('cve_id', ''))
            if cve and cve.startswith('CVE-'):
                cve_counts[cve] = cve_counts.get(cve, 0) + 1
        
        return [cve for cve, count in sorted(cve_counts.items(), key=lambda x: x[1], reverse=True)[:limit]]
    
    def _identify_emerging_threats(self, data: List[Dict[str, Any]]) -> List[str]:
        """Identify emerging threats from data"""
        emerging = []
        
        for item in data:
            if self._is_recent(item, days=3):  # Very recent threats
                threat_name = item.get('vulnerabilityname', item.get('title', 'Unknown'))
                if threat_name not in emerging:
                    emerging.append(threat_name)
        
        return emerging[:5]  # Top 5 emerging threats
    
    def _generate_turn_number(self) -> str:
        """Generate TURN number for reports"""
        return datetime.now().strftime("%Y%m%d")
    
    def _generate_operational_report(self, analysis_data: Dict[str, Any], turn_number: str) -> str:
        """Generate TURN operational report"""
        template = """# TURN {turn_number} — GLOBAL FUSION DIGEST (OPERATIONAL REPORT)

**Date:** {date}
**Turn Number:** {turn_number}
**Analysis Timestamp:** {analysis_timestamp}

## 1. EXECUTIVE SUMMARY

This report provides a comprehensive overview of the current global threat landscape based on real-time intelligence from official government sources. Over the last 24 hours, **{total_threats}** significant threats have been identified and analyzed.

### Key Findings:
- **Total Threats Analyzed:** {total_threats}
- **Critical Threats:** {critical_count}
- **High Severity Threats:** {high_count}
- **Top Affected Vendors:** {top_vendors}
- **Trending CVEs:** {trending_cves}

## 2. THREAT ANALYSIS

### Severity Distribution
{severity_analysis}

### Recent Trends
{trends_analysis}

### Emerging Threats
{emerging_threats}

## 3. RECOMMENDATIONS

- Monitor systems for the identified vulnerabilities
- Apply security patches as soon as possible
- Implement additional monitoring for affected vendors
- Review incident response procedures

---
*This report was generated by DataScope Enhanced with TURN integration*
"""
        
        severity_dist = analysis_data.get('severity_distribution', {})
        top_vendors = analysis_data.get('top_vendors', [])[:5]
        trending_cves = analysis_data.get('recent_trends', {}).get('trending_cves', [])
        
        return template.format(
            turn_number=turn_number,
            date=datetime.now().strftime("%Y-%m-%d"),
            analysis_timestamp=analysis_data.get('analysis_timestamp', datetime.now().isoformat()),
            total_threats=analysis_data.get('total_threats_analyzed', 0),
            critical_count=severity_dist.get('critical', 0),
            high_count=severity_dist.get('high', 0),
            top_vendors=", ".join([f"{v[0]} ({v[1]})" for v in top_vendors]),
            trending_cves=", ".join(trending_cves),
            severity_analysis=self._format_severity_analysis(severity_dist),
            trends_analysis=self._format_trends_analysis(analysis_data.get('recent_trends', {})),
            emerging_threats=self._format_emerging_threats(analysis_data.get('recent_trends', {}).get('emerging_threats', []))
        )
    
    def _generate_public_brief(self, analysis_data: Dict[str, Any], turn_number: str) -> str:
        """Generate TURN public brief"""
        template = """# TURN {turn_number} — CYBERSECURITY BRIEF

**Date:** {date}

## Today's Cyber Threat Landscape

{total_threats} cybersecurity threats have been identified and analyzed today. Here are the key highlights:

### 🔴 Critical Alerts
{critical_alerts}

### 📊 Threat Summary
- **Total Threats:** {total_threats}
- **Critical:** {critical_count}
- **High:** {high_count}
- **Medium:** {medium_count}

### 💡 Security Tip of the Day
{security_tip}

Stay informed. Stay secure.

#Cybersecurity #ThreatIntel #InfoSec #TURNReport
"""
        
        severity_dist = analysis_data.get('severity_distribution', {})
        
        return template.format(
            turn_number=turn_number,
            date=datetime.now().strftime("%Y-%m-%d"),
            total_threats=analysis_data.get('total_threats_analyzed', 0),
            critical_count=severity_dist.get('critical', 0),
            high_count=severity_dist.get('high', 0),
            medium_count=severity_dist.get('medium', 0),
            critical_alerts=self._format_critical_alerts(analysis_data),
            security_tip="Keep your systems updated and monitor for unusual activity."
        )
    
    def _generate_executive_summary(self, analysis_data: Dict[str, Any], turn_number: str) -> str:
        """Generate TURN executive summary"""
        template = """# TURN {turn_number} — EXECUTIVE SUMMARY

**Date:** {date}
**Prepared for:** Executive Leadership

## Key Metrics
- **Threats Analyzed:** {total_threats}
- **Critical Risk Level:** {risk_level}
- **Top Threat Vector:** {top_vector}

## Strategic Recommendations
{recommendations}

## Risk Assessment
{risk_assessment}

---
*Confidential - Executive Distribution Only*
"""
        
        return template.format(
            turn_number=turn_number,
            date=datetime.now().strftime("%Y-%m-%d"),
            total_threats=analysis_data.get('total_threats_analyzed', 0),
            risk_level=self._calculate_risk_level(analysis_data),
            top_vector=self._identify_top_threat_vector(analysis_data),
            recommendations=self._generate_executive_recommendations(analysis_data),
            risk_assessment=self._generate_risk_assessment(analysis_data)
        )
    
    def _format_severity_analysis(self, severity_dist: Dict[str, int]) -> str:
        """Format severity distribution for reports"""
        total = sum(severity_dist.values())
        if total == 0:
            return "No threats analyzed."
        
        analysis = []
        for severity, count in severity_dist.items():
            percentage = (count / total) * 100
            analysis.append(f"- **{severity.title()}:** {count} ({percentage:.1f}%)")
        
        return "\n".join(analysis)
    
    def _format_trends_analysis(self, trends: Dict[str, Any]) -> str:
        """Format trends analysis for reports"""
        return f"""
- **Total Threats:** {trends.get('total_threats', 0)}
- **Recent Threats (7 days):** {trends.get('recent_threats', 0)}
- **Trending CVEs:** {', '.join(trends.get('trending_cves', []))}
"""
    
    def _format_emerging_threats(self, emerging: List[str]) -> str:
        """Format emerging threats for reports"""
        if not emerging:
            return "No new emerging threats identified."
        
        return "\n".join([f"- {threat}" for threat in emerging])
    
    def _format_critical_alerts(self, analysis_data: Dict[str, Any]) -> str:
        """Format critical alerts for public brief"""
        critical_count = analysis_data.get('severity_distribution', {}).get('critical', 0)
        
        if critical_count == 0:
            return "No critical threats identified today."
        
        return f"{critical_count} critical vulnerabilities require immediate attention."
    
    def _calculate_risk_level(self, analysis_data: Dict[str, Any]) -> str:
        """Calculate overall risk level"""
        severity_dist = analysis_data.get('severity_distribution', {})
        critical = severity_dist.get('critical', 0)
        high = severity_dist.get('high', 0)
        
        if critical > 10:
            return "CRITICAL"
        elif critical > 5 or high > 20:
            return "HIGH"
        elif high > 10:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _identify_top_threat_vector(self, analysis_data: Dict[str, Any]) -> str:
        """Identify top threat vector"""
        top_vendors = analysis_data.get('top_vendors', [])
        if top_vendors:
            return f"Vulnerabilities in {top_vendors[0][0]} products"
        return "Mixed threat vectors"
    
    def _generate_executive_recommendations(self, analysis_data: Dict[str, Any]) -> str:
        """Generate executive recommendations"""
        return """
1. **Immediate Actions:** Review and patch critical vulnerabilities
2. **Strategic Focus:** Enhance monitoring for top affected vendors
3. **Resource Allocation:** Consider additional cybersecurity investments
4. **Risk Management:** Update incident response procedures
"""
    
    def _generate_risk_assessment(self, analysis_data: Dict[str, Any]) -> str:
        """Generate risk assessment"""
        risk_level = self._calculate_risk_level(analysis_data)
        total_threats = analysis_data.get('total_threats_analyzed', 0)
        
        return f"""
**Current Risk Level:** {risk_level}
**Threat Volume:** {total_threats} threats analyzed
**Trend:** {"Increasing" if total_threats > 100 else "Stable"}
**Recommendation:** {"Immediate action required" if risk_level in ["CRITICAL", "HIGH"] else "Continue monitoring"}
"""
    
    def _fallback_cybersecurity_collection(self, location: Optional[str] = None) -> Dict[str, Any]:
        """Fallback cybersecurity data collection when TURN modules unavailable"""
        self.logger.info("Using fallback cybersecurity collection")
        
        # Basic collection without TURN modules
        import requests
        from datetime import datetime
        
        results = {
            'collection_timestamp': datetime.now().isoformat(),
            'location': location,
            'sources': [],
            'data': [],
            'total_items_collected': 0,
            'fallback_mode': True
        }
        
        try:
            # Collect CISA KEV data directly
            response = requests.get('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json')
            if response.status_code == 200:
                kev_data = response.json()
                vulnerabilities = kev_data.get('vulnerabilities', [])
                results['sources'].append('CISA KEV')
                results['data'].extend(vulnerabilities)
                results['total_items_collected'] = len(vulnerabilities)
        except Exception as e:
            self.logger.error(f"Fallback KEV collection failed: {e}")
        
        return results
    
    def _fallback_threat_analysis(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback threat analysis when TURN modules unavailable"""
        self.logger.info("Using fallback threat analysis")
        
        return {
            'analysis_timestamp': datetime.now().isoformat(),
            'total_threats_analyzed': len(data),
            'severity_distribution': self._calculate_severity_distribution(data),
            'top_vendors': self._get_top_vendors(data),
            'recent_trends': self._analyze_trends(data),
            'fallback_mode': True
        }
    
    def _fallback_report_generation(self, analysis_data: Dict[str, Any], report_type: str) -> str:
        """Fallback report generation when TURN modules unavailable"""
        self.logger.info("Using fallback report generation")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cybersecurity_{timestamp}_{report_type}_report.md"
        
        # Generate basic report
        report_content = f"""# Cybersecurity Report - {report_type.title()}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Report Type:** {report_type.title()}

## Summary

Total threats analyzed: {analysis_data.get('total_threats_analyzed', 0)}

## Analysis

{self._format_severity_analysis(analysis_data.get('severity_distribution', {}))}

---
*Generated by DataScope Enhanced (Fallback Mode)*
"""
        
        # Write report to file
        report_path = os.path.join('reports', filename)
        os.makedirs('reports', exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        return report_path


# Create a global instance for easy access
turn_integration = TURNIntegration()


class ReportGenerator:
    """
    Compatibility class for TURN report generation
    Provides the ReportGenerator interface expected by the module checker
    """
    
    def __init__(self):
        self.turn_integration = turn_integration
    
    def generate_report(self, analysis_data: Dict[str, Any], report_type: str = 'operational') -> str:
        """Generate report using TURN integration"""
        return self.turn_integration.generate_turn_report(analysis_data, report_type)
    
    def is_available(self) -> bool:
        """Check if report generation is available"""
        return True  # Always available (fallback mode if needed)


# Export the compatibility class
__all__ = ['TURNIntegration', 'ReportGenerator', 'turn_integration']

