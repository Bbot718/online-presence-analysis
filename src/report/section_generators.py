from ..visualizations.charts import ChartGenerator
from ..utils.llm_analyzer import LLMAnalyzer
from ..collectors.seo_collector import SEOCollector
from ..collectors.performance_collector import PerformanceCollector
from ..collectors.content_collector import ContentCollector
from ..collectors.technical_collector import TechnicalCollector
from pathlib import Path
import json
from datetime import datetime

class ReportSectionGenerator:
    def __init__(self, url):
        self.url = url
        self.chart_generator = ChartGenerator()
        self.llm_analyzer = LLMAnalyzer()
        
        # Initialize collectors
        self.seo_collector = SEOCollector()
        self.performance_collector = PerformanceCollector()
        self.content_collector = ContentCollector()
        self.technical_collector = TechnicalCollector()
        
        self.output_dir = Path("data/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(self):
        """Generate complete website analysis report"""
        try:
            # Initialize base report structure
            report_data = {
                'url': self.url,
                'timestamp': datetime.now().isoformat(),
                'seo_analysis': {},
                'performance_analysis': {},
                'content_analysis': {},
                'technical_analysis': {
                    'mobile_responsiveness': {},
                    'security': {
                        'headers': {},
                        'ssl_certificate': {},
                        'mozilla_observatory': {}
                    },
                    'accessibility': {
                        'basic_checks': {},
                        'wave_results': {}
                    },
                    'seo_technical': {
                        'schema_markup': {},
                        'sitemap': {},
                        'robots_txt': {}
                    },
                    'validation': {
                        'w3c': {},
                        'pagespeed': {}
                    }
                }
            }

            # Collect all data with debug logging
            print("Collecting SEO data...")
            seo_data = self.seo_collector.collect_data(self.url)
            if seo_data:
                report_data['seo_analysis'] = seo_data
                print("SEO data collected successfully")
            else:
                print("No SEO data collected")
            
            print("Collecting performance data...")
            performance_data = self.performance_collector.collect_data(self.url)
            if performance_data:
                report_data['performance_analysis'] = performance_data
                print("Performance data collected successfully")
            else:
                print("No performance data collected")
            
            print("Collecting content data...")
            content_data = self.content_collector.collect_data(self.url)
            if content_data:
                report_data['content_analysis'] = content_data
                print("Content data collected successfully")
            else:
                print("No content data collected")
            
            print("Collecting technical data...")
            technical_data = self.technical_collector.collect_data(self.url)
            if technical_data:
                report_data['technical_analysis'].update({
                    'mobile_responsiveness': technical_data.get('mobile_responsive', {}),
                    'security': {
                        'headers': technical_data.get('security_headers', {}),
                        'ssl_certificate': technical_data.get('ssl_info', {}),
                        'mozilla_observatory': technical_data.get('mozilla_observatory', {})
                    },
                    'accessibility': {
                        'basic_checks': technical_data.get('accessibility', {}),
                        'wave_results': technical_data.get('wave_analysis', {})
                    },
                    'seo_technical': {
                        'schema_markup': technical_data.get('schema_markup', {}),
                        'sitemap': technical_data.get('sitemap', {}),
                        'robots_txt': technical_data.get('robots_txt', {})
                    },
                    'validation': {
                        'w3c': technical_data.get('w3c_validity', {}),
                        'pagespeed': technical_data.get('pagespeed', {})
                    }
                })
                print("Technical data collected successfully")
            else:
                print("No technical data collected")

            # Generate analysis for each section with debug logging
            print("Generating section analyses...")
            
            if report_data['seo_analysis']:
                print("Analyzing SEO data...")
                report_data['seo_analysis']['recommendations'] = self.llm_analyzer.analyze_section('seo', report_data['seo_analysis'])

            if report_data['performance_analysis']:
                print("Analyzing performance data...")
                report_data['performance_analysis']['recommendations'] = self.llm_analyzer.analyze_section('performance', report_data['performance_analysis'])

            if report_data['content_analysis']:
                print("Analyzing content data...")
                report_data['content_analysis']['recommendations'] = self.llm_analyzer.analyze_section('content', report_data['content_analysis'])

            if report_data['technical_analysis']:
                print("Analyzing technical data...")
                report_data['technical_analysis']['recommendations'] = self.llm_analyzer.analyze_section('technical', report_data['technical_analysis'])

            # Generate overall summary
            print("Generating summary...")
            report_data['summary'] = self.llm_analyzer.generate_summary(report_data)

            # Save report
            print("Saving report...")
            self._save_report(report_data)
            print("Report generation completed")

            return report_data

        except Exception as e:
            print(f"Error generating report: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def _save_report(self, report):
        """Save report to file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_path = self.output_dir / f"report_{timestamp}.json"
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"Report saved to {report_path}")
            
        except Exception as e:
            print(f"Error saving report: {str(e)}")