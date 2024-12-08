import logging
import yaml
from modules.website.lighthouse import analyze_website_with_pagespeed
from modules.customer.review_analysis import scrape_reviews, analyze_sentiment
from modules.advertising.ads_analysis import scrape_facebook_ads
from modules.social_media.social_media_analysis import analyze_social_media
from utils.pdf_generator import create_pdf

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load configuration
    with open('config/settings.yaml', 'r') as file:
        settings = yaml.safe_load(file)

    # Load settings from configuration
    target_url = settings.get("default_website")
    api_key = settings.get("google_api_key")
    competitors = settings.get("competitors", [])
    social_media_urls = settings.get("social_media_urls", {})
    ads_url = settings.get("ads_urls", {}).get("facebook_ad_library")
    review_url = settings.get("review_url")

    # Initialize the report data dictionary
    report_data = {}

    # Analyze the target website
    logger.info("Analyzing the target website...")
    target_report = analyze_website_with_pagespeed(target_url, api_key)
    if "Error" in target_report:
        logger.error(f"Failed to analyze the website: {target_report['Error']}")
        report_data["Target Website Analysis"] = {"Error": target_report["Error"]}
    else:
        logger.info("Target website analysis completed.")
        report_data["Target Website Analysis"] = target_report

    # Analyze competitors
    logger.info("Analyzing competitors...")
    competitor_reports = []
    for competitor in competitors:
        competitor_report = analyze_website_with_pagespeed(competitor, api_key)
        competitor_reports.append({competitor: competitor_report})
    report_data["Competitor Reports"] = competitor_reports

    # Analyze social media metrics and growth trends
    logger.info("Analyzing social media presence and growth trends...")
    social_media_data = analyze_social_media(
        instagram_url=social_media_urls.get("instagram"),
        facebook_url=social_media_urls.get("facebook"),
        linkedin_url=social_media_urls.get("linkedin")
    )
    if social_media_data:
        logger.info("Social media analysis and growth trends completed successfully.")
    report_data["Social Media Analysis"] = social_media_data

    # Analyze customer reviews and sentiment
    logger.info("Scraping customer reviews...")
    reviews = scrape_reviews(review_url)
    if "Error" in reviews:
        logger.error(reviews["Error"])
        report_data["Customer Sentiment"] = {"Error": reviews["Error"]}
    else:
        logger.info("Analyzing review sentiment...")
        sentiment_report = analyze_sentiment(reviews)
        report_data["Customer Sentiment"] = sentiment_report

    # Analyze competitor ads
    logger.info("Analyzing competitor ads...")
    ads = scrape_facebook_ads(ads_url)
    if "Error" in ads:
        logger.error(ads["Error"])
        report_data["Advertising Insights"] = {"Error": ads["Error"]}
    else:
        logger.info(f"Fetched {len(ads)} active ads.")
        report_data["Advertising Insights"] = ads

    # Generate the final PDF report
    logger.info("Generating the PDF report...")
    create_pdf(report_data, filename="final_report.pdf")
    logger.info("Report generation complete.")

if __name__ == "__main__":
    main()