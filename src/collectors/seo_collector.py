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
            
            # Store the data as instance variables
            self._meta_data = self._analyze_meta_tags(soup)
            self._headings = self._analyze_headings(soup)
            self._links = self._analyze_links(soup, url)
            self._images = self._analyze_images(soup)
            self._url_structure = self._analyze_url_structure(url)
            self._mobile_friendly = self._check_mobile_friendly(soup)
            
            seo_data = {
                'meta_tags': self._meta_data,
                'headings': self._headings,
                'links': self._links,
                'images': self._images,
                'url_structure': self._url_structure,
                'mobile_friendly': self._mobile_friendly,
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
        scores = {}
        
        # Meta Tags Score (max 100)
        meta_score = 0
        if hasattr(self, '_meta_data'):
            meta = self._meta_data
            meta_score += 20 if meta.get('title') else 0
            meta_score += 20 if meta.get('meta_description') else 0
            meta_score += 15 if meta.get('meta_keywords') else 0
            meta_score += 15 if meta.get('robots') else 0
            meta_score += 15 if meta.get('viewport') else 0
            meta_score += 15 if meta.get('charset') else 0
        scores['meta_tags'] = meta_score

        # Headings Score (max 100)
        heading_score = 0
        if hasattr(self, '_headings'):
            h = self._headings
            heading_score += 40 if h.get('h1', {}).get('count') == 1 else 0  # One H1 tag
            heading_score += 20 if h.get('h2', {}).get('count') > 0 else 0   # Has H2 tags
            heading_score += 20 if all(len(content) < 70 for content in h.get('h1', {}).get('content', [])) else 0  # H1 length
            heading_score += 20 if sum(h.get(f'h{i}', {}).get('count', 0) for i in range(1, 7)) < 15 else 0  # Not too many headings
        scores['headings'] = heading_score

        # Links Score (max 100)
        links_score = 0
        if hasattr(self, '_links'):
            links = self._links
            internal_count = links.get('internal', {}).get('count', 0)
            external_count = links.get('external', {}).get('count', 0)
            total_links = internal_count + external_count
            
            links_score += 40 if internal_count > 0 else 0  # Has internal links
            links_score += 30 if external_count > 0 else 0  # Has external links
            links_score += 30 if total_links < 100 else 0   # Not too many links
        scores['links'] = links_score

        # Images Score (max 100)
        images_score = 0
        if hasattr(self, '_images'):
            img = self._images
            total_images = img.get('total_count', 0)
            with_alt = img.get('with_alt', 0)
            
            if total_images > 0:
                alt_ratio = with_alt / total_images
                images_score += min(100, alt_ratio * 100)
        scores['images'] = images_score

        # Mobile Score (max 100)
        mobile_score = 0
        if hasattr(self, '_mobile_friendly'):
            mobile = self._mobile_friendly
            mobile_score += 50 if mobile.get('has_viewport') else 0
            if mobile.get('viewport_content'):
                if 'width=device-width' in mobile.get('viewport_content'):
                    mobile_score += 25
                if 'initial-scale=1' in mobile.get('viewport_content'):
                    mobile_score += 25
        scores['mobile'] = mobile_score

        # Calculate overall score (average of all scores)
        scores['overall'] = int(sum(scores.values()) / len(scores))
        
        return scores
        