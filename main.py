import logging
import yaml
from modules.website.lighthouse import analyze_website
from modules.competitor.competitor_analysis import analyze_competitors
from modules.social_media.social_media_analysis import analyze_social_media
from utils.pdf_generator import create_pdf

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load settings
    with open('config/settings.yaml', 'r') as file:
        settings = yaml.safe_load(file)

    target_url = settings.get("default_website", "https://example.com")
    competitors = settings.get("competitors", [])
    social_media_ids = settings.get("social_media", {})
    access_token = settings.get("social_media_access_token", "")

    logger.info(f"Target website: {target_url}")
    logger.info(f"Competitors: {competitors}")

    # Website analysis
    target_report = analyze_website(target_url)

    # Competitor analysis
    comparison_data = analyze_competitors(target_url, competitors)

    # Social Media Analysis
    logger.info("Starting social media analysis...")
    social_media_report = analyze_social_media(
        instagram_user_id=social_media_ids.get("instagram"),
        facebook_page_id=social_media_ids.get("facebook"),
        linkedin_page_id=social_media_ids.get("linkedin"),
        access_token=access_token
    )

    # Combine all reports
    report_data = {
        "Target Website Analysis": target_report,
        "Competitor Comparison": comparison_data,
        "Social Media Analysis": social_media_report,
    }

    # Generate PDF
    pdf_filename = "final_report.pdf"
    create_pdf(report_data, filename=pdf_filename)
    logger.info(f"Report generated successfully as {pdf_filename}")

if __name__ == "__main__":
    main()