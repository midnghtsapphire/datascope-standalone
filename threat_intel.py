"""
TURN Global Fusion Digest - Web API Routes
Provides REST API endpoints for threat intelligence data
"""

import os
import json
import datetime
import subprocess
import sys
from flask import Blueprint, jsonify, request, send_file
from pathlib import Path

threat_intel_bp = Blueprint('threat_intel', __name__)

# Get the source directory path
SRC_DIR = Path(__file__).parent.parent

@threat_intel_bp.route('/status')
def get_status():
    """Get system status and last update information"""
    try:
        # Check for latest analysis results
        reports_dir = SRC_DIR / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        # Find latest report files
        latest_reports = []
        for report_file in reports_dir.glob('TURN_*_Summary.json'):
            latest_reports.append({
                'filename': report_file.name,
                'date': report_file.stat().st_mtime
            })
        
        latest_reports.sort(key=lambda x: x['date'], reverse=True)
        
        status = {
            'system': 'TURN Global Fusion Digest',
            'status': 'operational',
            'last_update': datetime.datetime.now().isoformat(),
            'reports_available': len(latest_reports),
            'latest_report': latest_reports[0]['filename'] if latest_reports else None
        }
        
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@threat_intel_bp.route('/threats/current')
def get_current_threats():
    """Get current threat intelligence analysis"""
    try:
        # Look for the most recent threat analysis results
        reports_dir = SRC_DIR / 'reports'
        analysis_files = list(reports_dir.glob('*_threat_analysis_results.json'))
        
        if not analysis_files:
            return jsonify({'error': 'No threat analysis data available'}), 404
        
        # Get the most recent file
        latest_file = max(analysis_files, key=lambda x: x.stat().st_mtime)
        
        with open(latest_file, 'r') as f:
            analysis_data = json.load(f)
        
        return jsonify(analysis_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@threat_intel_bp.route('/threats/summary')
def get_threats_summary():
    """Get summarized threat intelligence for dashboard"""
    try:
        # Get current threats data
        reports_dir = SRC_DIR / 'reports'
        analysis_files = list(reports_dir.glob('*_threat_analysis_results.json'))
        
        if not analysis_files:
            return jsonify({'error': 'No threat analysis data available'}), 404
        
        latest_file = max(analysis_files, key=lambda x: x.stat().st_mtime)
        
        with open(latest_file, 'r') as f:
            analysis_data = json.load(f)
        
        consolidated = analysis_data.get('consolidated_analysis', {})
        
        # Create summary for dashboard
        summary = {
            'total_threats': consolidated.get('total_threats', 0),
            'severity_distribution': consolidated.get('severity_distribution', {}),
            'top_threat_actors': consolidated.get('top_threat_actors', [])[:5],
            'top_vendors': consolidated.get('top_vendors', [])[:5],
            'top_cves': consolidated.get('top_cves', [])[:10],
            'resilience_tips': analysis_data.get('resilience_tips', []),
            'last_updated': analysis_data.get('analysis_timestamp', 'Unknown')
        }
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@threat_intel_bp.route('/reports/latest')
def get_latest_report():
    """Get the latest operational report"""
    try:
        reports_dir = SRC_DIR / 'reports'
        report_files = list(reports_dir.glob('TURN_*_Operational_Report.md'))
        
        if not report_files:
            return jsonify({'error': 'No reports available'}), 404
        
        latest_report = max(report_files, key=lambda x: x.stat().st_mtime)
        
        with open(latest_report, 'r') as f:
            report_content = f.read()
        
        return jsonify({
            'filename': latest_report.name,
            'content': report_content,
            'generated': datetime.datetime.fromtimestamp(latest_report.stat().st_mtime).isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@threat_intel_bp.route('/reports/public')
def get_public_brief():
    """Get the latest public brief"""
    try:
        reports_dir = SRC_DIR / 'reports'
        brief_files = list(reports_dir.glob('TURN_*_Public_Brief.md'))
        
        if not brief_files:
            return jsonify({'error': 'No public briefs available'}), 404
        
        latest_brief = max(brief_files, key=lambda x: x.stat().st_mtime)
        
        with open(latest_brief, 'r') as f:
            brief_content = f.read()
        
        return jsonify({
            'filename': latest_brief.name,
            'content': brief_content,
            'generated': datetime.datetime.fromtimestamp(latest_brief.stat().st_mtime).isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@threat_intel_bp.route('/generate', methods=['POST'])
def generate_report():
    """Trigger manual report generation"""
    try:
        # Change to source directory for script execution
        original_cwd = os.getcwd()
        os.chdir(SRC_DIR)
        
        # Run the threat intelligence collection and analysis
        steps = [
            ('analyze_kev_data.py', 'CISA KEV Analysis'),
            ('collect_ic3_data.py', 'FBI IC3 Collection'),
            ('collect_cisa_advisories.py', 'CISA Advisories Collection'),
            ('threat_analysis_engine.py', 'Threat Analysis'),
            ('report_generator.py', 'Report Generation')
        ]
        
        results = []
        for script, description in steps:
            try:
                result = subprocess.run([sys.executable, script], 
                                      capture_output=True, text=True, timeout=120)
                
                results.append({
                    'step': description,
                    'success': result.returncode == 0,
                    'output': result.stdout if result.returncode == 0 else result.stderr
                })
                
                if result.returncode != 0:
                    break
                    
            except subprocess.TimeoutExpired:
                results.append({
                    'step': description,
                    'success': False,
                    'output': 'Timeout expired'
                })
                break
        
        # Move generated reports to reports directory
        reports_dir = SRC_DIR / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        turn_number = datetime.datetime.now().strftime('%Y%m%d')
        
        # Move reports if they exist
        for report_type in ['Operational_Report', 'Public_Brief']:
            report_file = SRC_DIR / f'TURN_{turn_number}_{report_type}.md'
            if report_file.exists():
                report_file.rename(reports_dir / f'TURN_{turn_number}_{report_type}.md')
        
        # Move analysis data files
        for data_file in ['threat_analysis_results.json', 'kev_analysis_results.json', 
                         'ic3_psa_data.json', 'cisa_advisories_data.json']:
            src_file = SRC_DIR / data_file
            if src_file.exists():
                src_file.rename(reports_dir / f'{turn_number}_{data_file}')
        
        os.chdir(original_cwd)
        
        return jsonify({
            'success': all(r['success'] for r in results),
            'steps': results,
            'turn_number': turn_number,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        os.chdir(original_cwd)
        return jsonify({'error': str(e)}), 500

@threat_intel_bp.route('/download/report/<filename>')
def download_report(filename):
    """Download a specific report file"""
    try:
        reports_dir = SRC_DIR / 'reports'
        file_path = reports_dir / filename
        
        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

