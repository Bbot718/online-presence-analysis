from src.collectors.content_collector import ContentCollector
from src.collectors.google_collector import GoogleCollector
from src.collectors.performance_collector import PerformanceCollector
from src.collectors.seo_collector import SEOCollector
from src.collectors.technical_collector import TechnicalCollector
import json
from datetime import datetime
from pathlib import Path
import nltk

class ReportGenerator:
    def __init__(self):
        self.collectors = {
            'seo': SEOCollector(),
            #'content': ContentCollector(),
            #'performance': PerformanceCollector(),
            #'technical': TechnicalCollector()
        }
        
        # Only initialize Google collector if credentials exist
        credentials_path = Path("credentials/google-credentials.json")
        if credentials_path.exists():
            self.collectors['google'] = GoogleCollector()

    def generate_report(self, url, google_property_id=None):
        """Generate a comprehensive report using all collectors"""
        report = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'data': {}
        }

        # Collect data from each collector
        for collector_name, collector in self.collectors.items():
            try:
                print(f"Collecting {collector_name} data...")
                if collector_name == 'google' and google_property_id:
                    data = collector.collect_data(url, google_property_id)
                else:
                    data = collector.collect_data(url)
                report['data'][collector_name] = data
            except Exception as e:
                print(f"Error collecting {collector_name} data: {str(e)}")
                report['data'][collector_name] = None

        return report

    def save_report(self, report, output_dir='reports'):
        """Save the report to a JSON file"""
        # Create reports directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Generate filename based on URL and timestamp
        url_slug = report['url'].replace('https://', '').replace('http://', '').replace('/', '_')
        timestamp = datetime.fromisoformat(report['timestamp']).strftime('%Y%m%d_%H%M%S')
        filename = f"{url_slug}_{timestamp}.json"
        filepath = Path(output_dir) / filename

        # Save report with pretty printing
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return filepath 