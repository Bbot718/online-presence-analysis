from src.report_generator import ReportGenerator
import sys
import argparse

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate website analysis report')
    parser.add_argument('url', help='URL to analyze (e.g., https://example.com)')
    parser.add_argument('--google-id', help='Google Analytics property ID (optional)', default=None)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize the report generator
    generator = ReportGenerator()
    
    print(f"Starting analysis for: {args.url}")
    
    # Generate report
    report = generator.generate_report(args.url, args.google_id)
    
    # Save report to file
    filepath = generator.save_report(report)
    print(f"Report saved to: {filepath}")

if __name__ == "__main__":
    main() 