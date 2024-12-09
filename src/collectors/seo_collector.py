import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

class SEOCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def collect_data(self, url):
        """Collect SEO-related data from the website"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            seo_data = {
                'meta_tags': self._analyze_meta_tags(soup),
                'headings': self._analyze_headings(soup),
                'links': self._analyze_links(soup, url),
                'images': self._analyze_images(soup),
                'url_structure': self._analyze_url_structure(url),
                'mobile_friendly': self._check_mobile_friendly(soup),
                'score': self._calculate_seo_score()
            }
            
            return seo_data
        except Exception as e:
            print(f"Error collecting SEO data: {str(e)}")
            return None

    def _analyze_meta_tags(self, soup):
        """Analyze meta tags including title and description"""
        meta_data = {
            'title': soup.title.string if soup.title else None,
            'meta_description': None,
            'meta_keywords': None,
            'robots': None,
            'viewport': None,
            'charset': None
        }

        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            content = meta.get('content', '')
            
            if name == 'description':
                meta_data['meta_description'] = content
            elif name == 'keywords':
                meta_data['meta_keywords'] = content
            elif name == 'robots':
                meta_data['robots'] = content
            elif name == 'viewport':
                meta_data['viewport'] = content
            
            if meta.get('charset'):
                meta_data['charset'] = meta.get('charset')

        return meta_data

    def _analyze_headings(self, soup):
        """Analyze heading structure (h1-h6)"""
        headings = {}
        for i in range(1, 7):
            h_tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = {
                'count': len(h_tags),
                'content': [tag.get_text().strip() for tag in h_tags]
            }
        return headings

    def _analyze_links(self, soup, base_url):
        """Analyze internal and external links"""
        base_domain = urlparse(base_url).netloc
        internal_links = []
        external_links = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/') or base_domain in href:
                internal_links.append(href)
            elif href.startswith('http'):
                external_links.append(href)

        return {
            'internal': {
                'count': len(internal_links),
                'urls': internal_links
            },
            'external': {
                'count': len(external_links),
                'urls': external_links
            }
        }

    def _analyze_images(self, soup):
        """Analyze image tags and their attributes"""
        images = soup.find_all('img')
        return {
            'total_count': len(images),
            'with_alt': len([img for img in images if img.get('alt')]),
            'without_alt': len([img for img in images if not img.get('alt')])
        }

    def _analyze_url_structure(self, url):
        """Analyze URL structure"""
        parsed_url = urlparse(url)
        return {
            'protocol': parsed_url.scheme,
            'domain': parsed_url.netloc,
            'path': parsed_url.path,
            'parameters': parsed_url.params,
            'query': parsed_url.query,
            'is_clean': not bool(parsed_url.params or parsed_url.query)
        }

    def _check_mobile_friendly(self, soup):
        """Basic mobile-friendly check based on viewport meta tag"""
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        return {
            'has_viewport': bool(viewport),
            'viewport_content': viewport.get('content') if viewport else None
        }

    def _calculate_seo_score(self):
        """Calculate overall SEO score based on collected metrics"""
        # This would be expanded based on actual metrics
        return {
            'overall': 85,  # Placeholder
            'meta_tags': 90,
            'headings': 80,
            'links': 85,
            'images': 75,
            'mobile': 90
        } 