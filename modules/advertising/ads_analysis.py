from bs4 import BeautifulSoup
import requests

def scrape_facebook_ads(url):
    """
    Scrapes active ad data from the Facebook Ad Library.

    Args:
        url (str): The URL of the Facebook Ad Library page for the competitor.

    Returns:
        list: A list of dictionaries containing ad details.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract ad details (modify selectors based on Facebook Ad Library structure)
        ads = []
        ad_elements = soup.find_all("div", class_="ad-card")  # Replace with actual class or tag
        for ad in ad_elements:
            ad_details = {
                "Ad Text": ad.find("div", class_="ad-text").text.strip() if ad.find("div", class_="ad-text") else "N/A",
                "Media Type": ad.find("div", class_="ad-media-type").text.strip() if ad.find("div", class_="ad-media-type") else "N/A",
                "Published Date": ad.find("div", class_="ad-date").text.strip() if ad.find("div", class_="ad-date") else "N/A",
            }
            ads.append(ad_details)

        return ads

    except requests.exceptions.RequestException as e:
        return {"Error": f"Failed to fetch ads: {e}"}