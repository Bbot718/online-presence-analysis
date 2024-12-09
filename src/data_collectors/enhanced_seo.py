def get_enhanced_seo_data(self):
    """Collect SEO data using multiple free sources"""
    data = {}
    
    # Archive.org API for historical data
    archive_url = f"https://archive.org/wayback/available?url={self.domain}"
    archive_data = requests.get(archive_url).json()
    
    # W3C Validator API for HTML validation
    w3c_url = f"https://validator.w3.org/nu/?doc={self.url}&out=json"
    w3c_data = requests.get(w3c_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    # DNS data using dnspython
    dns_info = dns.resolver.resolve(self.domain, 'A')
    
    # Combine all data
    return {
        'historical_data': archive_data,
        'html_validation': w3c_data.json(),
        'dns_info': str(dns_info)
    } 