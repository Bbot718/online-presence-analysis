import requests

def get_instagram_data(user_id, access_token):
    """
    Fetch Instagram metrics using the Instagram Graph API.
    """
    if not user_id or not access_token:
        return {"Error": "Instagram account not configured."}

    url = f"https://graph.facebook.com/v12.0/{user_id}"
    params = {
        "fields": "followers_count,media_count",
        "access_token": access_token
    }
    response = requests.get(url, params=params)
    return response.json()

def get_facebook_data(page_id, access_token):
    """
    Fetch Facebook metrics using the Facebook Graph API.
    """
    if not page_id or not access_token:
        return {"Error": "Facebook page not configured."}

    url = f"https://graph.facebook.com/v12.0/{page_id}"
    params = {
        "fields": "fan_count,posts.limit(5){likes.summary(true),comments.summary(true)}",
        "access_token": access_token
    }
    response = requests.get(url, params=params)
    return response.json()

def get_linkedin_data(page_id, access_token):
    """
    Fetch LinkedIn metrics using the LinkedIn API.
    """
    if not page_id or not access_token:
        return {"Error": "LinkedIn account not configured."}

    # Placeholder API endpoint for LinkedIn (requires actual implementation)
    url = f"https://api.linkedin.com/v2/organizationPageStatistics/{page_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def analyze_social_media(instagram_user_id, facebook_page_id, linkedin_page_id, access_token):
    """
    Analyze social media presence for Instagram, Facebook, and LinkedIn.
    """
    analysis = {
        "Instagram": get_instagram_data(instagram_user_id, access_token),
        "Facebook": get_facebook_data(facebook_page_id, access_token),
        "LinkedIn": get_linkedin_data(linkedin_page_id, access_token)
    }

    return analysis
