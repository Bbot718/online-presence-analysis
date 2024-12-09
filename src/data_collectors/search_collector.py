import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re

class SearchCollector:
    def __init__(self, domain: str):
        self.domain = domain
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_search_data(self) -> dict:
        """Collect search-related data using free methods"""
        try:
            # Use DuckDuckGo's HTML (no API key needed)
            query = quote(f"site:{self.domain}")
            url = f"https://html.duckduckgo.com/html/?q={query}"
            
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return {
                'indexed_pages': self._count_results(soup),
                'top_keywords': self._extract_keywords(soup),
                'search_suggestions': self._get_search_suggestions(self.domain)
            }
        except Exception as e:
            print(f"Error collecting search data: {str(e)}")
            return {} 