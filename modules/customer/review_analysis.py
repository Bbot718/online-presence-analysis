from bs4 import BeautifulSoup
import requests
from textblob import TextBlob

def scrape_reviews(url):
    """
    Scrapes reviews from a given URL.

    Args:
        url (str): The URL of the review page.

    Returns:
        list: A list of review texts.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.text, "html.parser")

        # Find reviews on the page (modify the class or tag for the specific site)
        reviews = [review.text.strip() for review in soup.find_all("div", class_="review-text")]
        return reviews

    except requests.exceptions.RequestException as e:
        return {"Error": f"Failed to fetch reviews: {e}"}

def analyze_sentiment(reviews):
    """
    Analyzes the sentiment of a list of reviews.

    Args:
        reviews (list): A list of review texts.

    Returns:
        dict: Sentiment counts and notable reviews.
    """
    sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
    notable_reviews = {"Positive": [], "Negative": []}

    for review in reviews:
        analysis = TextBlob(review)
        polarity = analysis.sentiment.polarity

        if polarity > 0:
            sentiments["Positive"] += 1
            if len(notable_reviews["Positive"]) < 3:  # Limit notable reviews
                notable_reviews["Positive"].append(review)
        elif polarity < 0:
            sentiments["Negative"] += 1
            if len(notable_reviews["Negative"]) < 3:
                notable_reviews["Negative"].append(review)
        else:
            sentiments["Neutral"] += 1

    return {
        "Sentiments": sentiments,
        "Notable Reviews": notable_reviews
    }