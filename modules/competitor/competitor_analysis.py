from modules.website.lighthouse import analyze_website

def analyze_competitors(target_url, competitor_urls):
    results = {}
    all_urls = [target_url] + competitor_urls

    for url in all_urls:
        results[url] = analyze_website(url)

    comparison = {}
    metrics = results[target_url].keys()

    for metric in metrics:
        comparison[metric] = {url: results[url][metric] for url in all_urls}

    return comparison