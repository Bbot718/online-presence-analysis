from bs4 import BeautifulSoup
import requests

def analyze_technical_seo(url):
    """
    Analyzes technical SEO for page titles, meta descriptions, and alt text coverage.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Title and Meta Description
    title = soup.find("title").text if soup.find("title") else "No title"
    meta_description = soup.find("meta", attrs={"name": "description"})
    meta_description = meta_description["content"] if meta_description else "No meta description"

    # Alt Text Coverage
    images = soup.find_all("img")
    missing_alt = sum(1 for img in images if not img.get("alt"))

    return {
        "Title": title,
        "Meta Description": meta_description,
        "Total Images": len(images),
        "Missing Alt Text": missing_alt
    }
