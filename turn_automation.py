#!/usr/bin/env python3
"""
TURN Global Fusion Digest - Main Automation Script
Orchestrates daily threat intelligence collection, analysis, and report generation
"""

import os
import sys
import json
import datetime
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('turn_automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class TURNAutomation:
    """Main automation orchestrator for TURN Global Fusion Digest"""
    
    def __init__(self, output_dir="./reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.turn_number = datetime.datetime.now().strftime('%Y%m%d')
        self.logger = logging.getLogger(__name__)
        
    def run_script(self, script_name: str, description: str) -> bool:
        """Run a Python script and return success status"""
        try:
            self.logger.info(f"Starting: {description}")
            result = subprocess.run([sys.executable, script_name], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.logger.info(f"Completed: {description}")
                return True
            else:
                self.logger.error(f"Failed: {description}")
                self.logger.error(f"Error output: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"Timeout: {description}")
            return False
        except Exception as e:
            self.logger.error(f"Exception in {description}: {str(e)}")
            return False
    
    def collect_threat_intelligence(self) -> bool:
        """Step 1: Collect threat intelligence from all sources"""
        self.logger.info("=== PHASE 1: THREAT INTELLIGENCE COLLECTION ===")
        
        # Collect CISA KEV data
        if not self.run_script("analyze_kev_data.py", "CISA KEV Analysis"):
            return False
            
        # Collect FBI IC3 PSAs
        if not self.run_script("collect_ic3_data.py", "FBI IC3 PSA Collection"):
            return False
            
        # Collect CISA Advisories
        if not self.run_script("collect_cisa_advisories.py", "CISA Advisories Collection"):
            return False
            
        return True
    
    def analyze_threats(self) -> bool:
        """Step 2: Analyze and categorize threats"""
        self.logger.info("=== PHASE 2: THREAT ANALYSIS ===")
        
        return self.run_script("threat_analysis_engine.py", "Threat Analysis and Categorization")
    
    def generate_reports(self) -> bool:
        """Step 3: Generate formatted reports"""
        self.logger.info("=== PHASE 3: REPORT GENERATION ===")
        
        return self.run_script("report_generator.py", "Report Generation")
    
    def archive_reports(self) -> bool:
        """Step 4: Archive reports to output directory"""
        self.logger.info("=== PHASE 4: REPORT ARCHIVAL ===")
        
        try:
            # Move generated reports to output directory
            operational_report = f"TURN_{self.turn_number}_Operational_Report.md"
            public_brief = f"TURN_{self.turn_number}_Public_Brief.md"
            
            if os.path.exists(operational_report):
                os.rename(operational_report, self.output_dir / operational_report)
                self.logger.info(f"Archived: {operational_report}")
            
            if os.path.exists(public_brief):
                os.rename(public_brief, self.output_dir / public_brief)
                self.logger.info(f"Archived: {public_brief}")
            
            # Archive analysis data
            analysis_files = [
                "threat_analysis_results.json",
                "kev_analysis_results.json", 
                "ic3_psa_data.json",
                "cisa_advisories_data.json"
            ]
            
            for file in analysis_files:
                if os.path.exists(file):
                    archive_name = f"{self.turn_number}_{file}"
                    os.rename(file, self.output_dir / archive_name)
                    self.logger.info(f"Archived: {archive_name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error archiving reports: {str(e)}")
            return False
    
    def generate_summary(self) -> dict:
        """Generate execution summary"""
        summary = {
            "turn_number": self.turn_number,
            "execution_date": datetime.datetime.now().isoformat(),
            "reports_generated": [],
            "data_files_archived": []
        }
        
        # Check for generated reports
        operational_report = self.output_dir / f"TURN_{self.turn_number}_Operational_Report.md"
        public_brief = self.output_dir / f"TURN_{self.turn_number}_Public_Brief.md"
        
        if operational_report.exists():
            summary["reports_generated"].append(str(operational_report))
        if public_brief.exists():
            summary["reports_generated"].append(str(public_brief))
        
        # Check for archived data files
        for file in self.output_dir.glob(f"{self.turn_number}_*.json"):
            summary["data_files_archived"].append(str(file))
        
        return summary
    
    def run_full_automation(self) -> bool:
        """Run the complete TURN automation pipeline"""
        self.logger.info(f"Starting TURN {self.turn_number} automation pipeline")
        
        # Step 1: Collect threat intelligence
        if not self.collect_threat_intelligence():
            self.logger.error("Threat intelligence collection failed")
            return False
        
        # Step 2: Analyze threats
        if not self.analyze_threats():
            self.logger.error("Threat analysis failed")
            return False
        
        # Step 3: Generate reports
        if not self.generate_reports():
            self.logger.error("Report generation failed")
            return False
        
        # Step 4: Archive reports
        if not self.archive_reports():
            self.logger.error("Report archival failed")
            return False
        
        # Generate summary
        summary = self.generate_summary()
        summary_file = self.output_dir / f"TURN_{self.turn_number}_Summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.logger.info("=== AUTOMATION COMPLETE ===")
        self.logger.info(f"Reports generated: {len(summary['reports_generated'])}")
        self.logger.info(f"Data files archived: {len(summary['data_files_archived'])}")
        self.logger.info(f"Summary saved to: {summary_file}")
        
        return True

def main():
    """Main entry point"""
    automation = TURNAutomation()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test mode - run individual components
        print("Running in test mode...")
        automation.logger.info("Test mode execution")
        success = automation.run_full_automation()
    else:
        # Production mode - full automation
        success = automation.run_full_automation()
    
    if success:
        print(f"TURN {automation.turn_number} automation completed successfully!")
        sys.exit(0)
    else:
        print(f"TURN {automation.turn_number} automation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()

