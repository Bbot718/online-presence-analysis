import requests
import json
from pathlib import Path
import subprocess
import tempfile
import os

class PerformanceCollector:
    def __init__(self):
        # Check if lighthouse is installed
        try:
            subprocess.run(['lighthouse', '--version'], 
                         capture_output=True, 
                         text=True)
        except FileNotFoundError:
            print("Lighthouse not found. Please install with: npm install -g lighthouse")
            print("Make sure you have Node.js installed first.")
            raise

    def collect_data(self, url):
        """Collect performance data using Lighthouse"""
        try:
            # Create temporary directory for lighthouse report
            with tempfile.TemporaryDirectory() as tmp_dir:
                output_path = Path(tmp_dir) / 'lighthouse-report.json'
                
                # Run lighthouse
                subprocess.run([
                    'lighthouse',
                    url,
                    '--output=json',
                    '--output-path=' + str(output_path),
                    '--chrome-flags="--headless"',
                    '--only-categories=performance'
                ], capture_output=True)

                # Read the lighthouse report
                with open(output_path) as f:
                    lighthouse_data = json.load(f)

                return self._process_lighthouse_data(lighthouse_data)

        except Exception as e:
            print(f"Error collecting performance data: {str(e)}")
            return None

    def _process_lighthouse_data(self, lighthouse_data):
        """Process and structure the Lighthouse data"""
        audits = lighthouse_data.get('audits', {})
        
        performance_data = {
            'score': int(lighthouse_data.get('categories', {}).get('performance', {}).get('score', 0) * 100),
            'metrics': {
                'first_contentful_paint': {
                    'score': audits.get('first-contentful-paint', {}).get('score', 0),
                    'value': audits.get('first-contentful-paint', {}).get('numericValue', 0),
                    'display_value': audits.get('first-contentful-paint', {}).get('displayValue', '')
                },
                'largest_contentful_paint': {
                    'score': audits.get('largest-contentful-paint', {}).get('score', 0),
                    'value': audits.get('largest-contentful-paint', {}).get('numericValue', 0),
                    'display_value': audits.get('largest-contentful-paint', {}).get('displayValue', '')
                },
                'total_blocking_time': {
                    'score': audits.get('total-blocking-time', {}).get('score', 0),
                    'value': audits.get('total-blocking-time', {}).get('numericValue', 0),
                    'display_value': audits.get('total-blocking-time', {}).get('displayValue', '')
                },
                'cumulative_layout_shift': {
                    'score': audits.get('cumulative-layout-shift', {}).get('score', 0),
                    'value': audits.get('cumulative-layout-shift', {}).get('numericValue', 0),
                    'display_value': audits.get('cumulative-layout-shift', {}).get('displayValue', '')
                },
                'speed_index': {
                    'score': audits.get('speed-index', {}).get('score', 0),
                    'value': audits.get('speed-index', {}).get('numericValue', 0),
                    'display_value': audits.get('speed-index', {}).get('displayValue', '')
                }
            },
            'opportunities': self._extract_opportunities(audits),
            'diagnostics': self._extract_diagnostics(audits)
        }

        return performance_data

    def _extract_opportunities(self, audits):
        """Extract improvement opportunities from audit data"""
        opportunity_audits = [
            'render-blocking-resources',
            'unused-css-rules',
            'unused-javascript',
            'unminified-css',
            'unminified-javascript',
            'unused-javascript',
            'modern-image-formats',
            'offscreen-images',
            'uses-optimized-images'
        ]

        opportunities = {}
        for audit_id in opportunity_audits:
            if audit_id in audits:
                audit = audits[audit_id]
                if audit.get('score', 1) < 1:  # Only include if there's room for improvement
                    opportunities[audit_id] = {
                        'title': audit.get('title', ''),
                        'description': audit.get('description', ''),
                        'score': audit.get('score', 0),
                        'savings_ms': audit.get('numericValue', 0),
                        'display_value': audit.get('displayValue', '')
                    }

        return opportunities

    def _extract_diagnostics(self, audits):
        """Extract diagnostic information from audit data"""
        diagnostic_audits = [
            'total-byte-weight',
            'dom-size',
            'critical-request-chains',
            'network-requests',
            'network-rtt',
            'network-server-latency',
            'main-thread-tasks',
            'bootup-time'
        ]

        diagnostics = {}
        for audit_id in diagnostic_audits:
            if audit_id in audits:
                audit = audits[audit_id]
                diagnostics[audit_id] = {
                    'title': audit.get('title', ''),
                    'description': audit.get('description', ''),
                    'score': audit.get('score', 0),
                    'display_value': audit.get('displayValue', '')
                }

        return diagnostics 