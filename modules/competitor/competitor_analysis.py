from modules.website.lighthouse import analyze_website

def analyze_competitors(target_url, competitor_urls):
    """
    Compare the target website with its competitors.
    
    Parameters:
        target_url (str): The target company's website URL.
        competitor_urls (list): List of competitor website URLs.

    Returns:
        dict: Comparison data with metrics for each website.
    """
    results = {}
    all_urls = [target_url] + competitor_urls

    for url in all_urls:
        results[url] = analyze_website(url)
    
    # Create comparison dictionary
    comparison = {}
    metrics = results[target_url].keys()  # Use the target's keys for structure
    
    for metric in metrics:
        comparison[metric] = {url: results[url][metric] for url in all_urls}
    
    return comparison