import argparse
from src.report.section_generators import ReportSectionGenerator
from src.utils.error_handler import ErrorHandler
from pathlib import Path

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Generate website analysis report')
    parser.add_argument('url', help='URL of the website to analyze')
    parser.add_argument('--output', help='Output directory', default='reports')
    args = parser.parse_args()

    # Setup error handling
    error_handler = ErrorHandler()

    try:
        # Create output directory
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate report
        generator = ReportSectionGenerator(args.url)
        report_path = generator.generate_report()
        
        print(f"Report generated successfully: {report_path}")
        
    except Exception as e:
        error_handler.log_error(e, "Main", args.url)
        print(f"Error generating report: {str(e)}")

if __name__ == "__main__":
    main() 