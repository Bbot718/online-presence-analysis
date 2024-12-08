from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def setup_driver():
    """
    Sets up the Selenium WebDriver.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_service = Service("path/to/chromedriver")  # Replace with the path to your ChromeDriver

    return webdriver.Chrome(service=chrome_service, options=chrome_options)

def scrape_instagram(instagram_url):
    """
    Scrapes public data from an Instagram profile.
    """
    driver = setup_driver()
    driver.get(instagram_url)
    time.sleep(3)

    try:
        followers = driver.find_element(By.XPATH, "//span[@title]").get_attribute("title").replace(",", "")
        likes = driver.find_element(By.XPATH, "//xpath_for_likes").text  # Placeholder for real XPath
        comments = driver.find_element(By.XPATH, "//xpath_for_comments").text  # Placeholder for real XPath
        return {"Followers": int(followers), "Likes": int(likes), "Comments": int(comments)}
    except Exception as e:
        return {"Error": f"Failed to scrape Instagram: {e}"}
    finally:
        driver.quit()

def scrape_facebook(facebook_url):
    """
    Scrapes public data from a Facebook page.
    """
    driver = setup_driver()
    driver.get(facebook_url)
    time.sleep(3)

    try:
        likes = driver.find_element(By.XPATH, "//div[contains(text(),'likes')]").text.replace(",", "")
        followers = driver.find_element(By.XPATH, "//div[contains(text(),'followers')]").text.replace(",", "")
        return {"Likes": int(likes), "Followers": int(followers)}
    except Exception as e:
        return {"Error": f"Failed to scrape Facebook: {e}"}
    finally:
        driver.quit()

def scrape_linkedin(linkedin_url):
    """
    Scrapes public data from a LinkedIn company page.
    """
    driver = setup_driver()
    driver.get(linkedin_url)
    time.sleep(3)

    try:
        followers = driver.find_element(By.XPATH, "//span[contains(text(),'followers')]").text.replace(",", "")
        return {"Followers": int(followers)}
    except Exception as e:
        return {"Error": f"Failed to scrape LinkedIn: {e}"}
    finally:
        driver.quit()