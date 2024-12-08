import requests

def analyze_website_with_pagespeed(url, api_key):
    """
    Fetches website metrics using Google PageSpeed Insights API.

    Args:
        url (str): The URL of the website to analyze.
        api_key (str): Google API key.

    Returns:
        dict: A dictionary of website performance metrics.
    """
    # Define the API endpoint
    endpoint = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}"
    response = requests.get(endpoint)

    # Handle API response errors
    if response.status_code != 200:
        return {"Error": f"API request failed with status code {response.status_code}"}

    data = response.json()

    try:
        # Extract Lighthouse scores
        performance = data['lighthouseResult']['categories']['performance']['score'] * 100
        seo = data['lighthouseResult']['categories']['seo']['score'] * 100
        accessibility = data['lighthouseResult']['categories']['accessibility']['score'] * 100
        best_practices = data['lighthouseResult']['categories']['best-practices']['score'] * 100

        # Extract Core Web Vitals
        core_web_vitals = {
            "Largest Contentful Paint (LCP)": data['loadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS']['percentile'],
            "First Input Delay (FID)": data['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['percentile'],
            "Cumulative Layout Shift (CLS)": data['loadingExperience']['metrics']['CUMULATIVE_LAYOUT_SHIFT_SCORE']['percentile']
        }

        # Extract additional opportunities and diagnostics
        diagnostics = {
            "Unused CSS/JavaScript Size": data['lighthouseResult']['audits']['unused-css-rules']['details']['overallSavingsBytes'] / 1024,
            "Image Optimization Savings": data['lighthouseResult']['audits']['uses-optimized-images']['details']['overallSavingsBytes'] / 1024,
            "Main Thread Blocking Time": data['lighthouseResult']['audits']['mainthread-work-breakdown']['details']['summary']['total']
        }

        return {
            "Performance": performance,
            "SEO": seo,
            "Accessibility": accessibility,
            "Best Practices": best_practices,
            "Core Web Vitals": core_web_vitals,
            "Diagnostics": diagnostics
        }

    except KeyError as e:
        return {"Error": f"Missing data in API response: {e}"}

def analyze_competitors_with_pagespeed(urls, api_key):
    """
    Analyzes multiple websites and compares their metrics.

    Args:
        urls (list): A list of website URLs to analyze.
        api_key (str): Google API key.

    Returns:
        list: A list of analysis results for each URL.
    """
    results = {}
    for url in urls:
        results[url] = analyze_website_with_pagespeed(url, api_key)
    return results