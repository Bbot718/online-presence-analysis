import os
import json
from modules.social_media.social_media_scraper import scrape_instagram, scrape_facebook, scrape_linkedin

# Path to store follower data
FOLLOWERS_DATA_PATH = "data/followers_data.json"

def load_historical_followers():
    """
    Load historical follower data from a JSON file.
    If the file doesn't exist, return an empty dictionary.
    """
    if os.path.exists(FOLLOWERS_DATA_PATH):
        with open(FOLLOWERS_DATA_PATH, "r") as file:
            return json.load(file)
    return {}

def save_current_followers(current_followers):
    """
    Save current follower data to a JSON file.

    Args:
        current_followers (dict): Dictionary of current follower counts.
    """
    with open(FOLLOWERS_DATA_PATH, "w") as file:
        json.dump(current_followers, file, indent=4)

def calculate_follower_growth(current_followers, historical_followers):
    """
    Calculate follower growth by comparing current and historical data.

    Args:
        current_followers (dict): Current follower counts.
        historical_followers (dict): Historical follower counts.

    Returns:
        dict: Follower growth trends for each platform.
    """
    growth = {}
    for platform, current_count in current_followers.items():
        historical_count = historical_followers.get(platform)
        if historical_count is not None:
            growth[platform] = current_count - historical_count
        else:
            growth[platform] = "No historical data available"
    return growth

def analyze_social_media(instagram_url=None, facebook_url=None, linkedin_url=None):
    """
    Analyze social media data for Instagram, Facebook, and LinkedIn, including follower growth trends.

    Args:
        instagram_url (str): URL of the Instagram profile.
        facebook_url (str): URL of the Facebook page.
        linkedin_url (str): URL of the LinkedIn page.

    Returns:
        dict: A dictionary containing social media analysis and growth trends.
    """
    analysis = {}
    current_followers = {}

    # Analyze Instagram
    if instagram_url:
        instagram_data = scrape_instagram(instagram_url)
        if "Error" not in instagram_data:
            followers = int(instagram_data.get("Followers", 0).replace(",", ""))
            instagram_data["Engagement Rate"] = "N/A"  # Engagement rate calculated elsewhere
            current_followers["Instagram"] = followers
        analysis["Instagram"] = instagram_data

    # Analyze Facebook
    if facebook_url:
        facebook_data = scrape_facebook(facebook_url)
        if "Error" not in facebook_data:
            followers = int(facebook_data.get("Followers", 0).replace(",", ""))
            current_followers["Facebook"] = followers
        analysis["Facebook"] = facebook_data

    # Analyze LinkedIn
    if linkedin_url:
        linkedin_data = scrape_linkedin(linkedin_url)
        if "Error" not in linkedin_data:
            followers = int(linkedin_data.get("Followers", 0).replace(",", ""))
            current_followers["LinkedIn"] = followers
        analysis["LinkedIn"] = linkedin_data

    # Load historical follower data
    historical_followers = load_historical_followers()

    # Calculate growth trends
    growth_trends = calculate_follower_growth(current_followers, historical_followers)

    # Save current followers for future runs
    save_current_followers(current_followers)

    return {
        "Analysis": analysis,
        "Growth Trends": growth_trends
    }