import requests
import ssl
import socket
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import urllib3
import json
from pathlib import Path

class TechnicalCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # Disable SSL warnings for internal checks
        urllib3.disable_warnings()

    def collect_data(self, url):
        """Collect technical data about the website"""
        try:
            technical_data = {
                'ssl_info': self._check_ssl(url),
                'security_headers': self._check_security_headers(url),
                'robots_txt': self._analyze_robots_txt(url),
                'sitemap': self._analyze_sitemap(url),
                'schema_markup': self._check_schema_markup(url),
                'mobile_responsive': self._check_mobile_responsive(url),
                'accessibility': self._check_accessibility(url),
                'w3c_validity': self._check_w3c_validity(url),
                'pagespeed': self._get_pagespeed_data(url),
                'mozilla_observatory': self._check_mozilla_observatory(url)
            }
            return technical_data
        except Exception as e:
            print(f"Error collecting technical data: {str(e)}")
            return None

    def _check_ssl(self, url):
        """Check SSL certificate status"""
        parsed_url = urlparse(url)
        try:
            context = ssl.create_default_context()
            with socket.create_connection((parsed_url.netloc, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=parsed_url.netloc) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        'valid': True,
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'expiry_date': cert['notAfter'],
                        'version': cert['version']
                    }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }

    def _check_security_headers(self, url):
        """Check security headers"""
        try:
            response = requests.get(url, headers=self.headers)
            headers = response.headers
            
            return {
                'strict_transport_security': headers.get('Strict-Transport-Security'),
                'x_frame_options': headers.get('X-Frame-Options'),
                'x_content_type_options': headers.get('X-Content-Type-Options'),
                'x_xss_protection': headers.get('X-XSS-Protection'),
                'content_security_policy': headers.get('Content-Security-Policy'),
                'referrer_policy': headers.get('Referrer-Policy'),
                'permissions_policy': headers.get('Permissions-Policy')
            }
        except Exception:
            return None

    def _analyze_robots_txt(self, url):
        """Analyze robots.txt file"""
        try:
            robots_url = f"{url.rstrip('/')}/robots.txt"
            response = requests.get(robots_url, headers=self.headers)
            if response.status_code == 200:
                content = response.text
                return {
                    'exists': True,
                    'size': len(content),
                    'user_agents': self._parse_robots_txt(content),
                    'has_sitemap': 'sitemap:' in content.lower()
                }
            return {'exists': False}
        except Exception:
            return {'exists': False}

    def _analyze_sitemap(self, url):
        """Analyze sitemap.xml"""
        try:
            sitemap_url = f"{url.rstrip('/')}/sitemap.xml"
            response = requests.get(sitemap_url, headers=self.headers)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
                return {
                    'exists': True,
                    'url_count': len(urls),
                    'last_modified': self._get_latest_sitemap_date(urls)
                }
            return {'exists': False}
        except Exception:
            return {'exists': False}

    def _check_schema_markup(self, url):
        """Check for schema.org markup"""
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            schemas = []
            
            # Check JSON-LD
            json_ld = soup.find_all('script', type='application/ld+json')
            for script in json_ld:
                try:
                    schemas.append(json.loads(script.string))
                except:
                    continue

            # Check microdata
            microdata = soup.find_all(attrs={"itemtype": True})
            schemas.extend([item['itemtype'] for item in microdata])

            return {
                'has_schema': len(schemas) > 0,
                'schema_types': schemas
            }
        except Exception:
            return {'has_schema': False}

    def _check_mobile_responsive(self, url):
        """Check mobile responsiveness"""
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            media_queries = len(soup.find_all('link', attrs={'media': True}))
            
            return {
                'has_viewport': viewport is not None,
                'viewport_content': viewport['content'] if viewport else None,
                'media_queries': media_queries,
                'responsive_images': self._check_responsive_images(soup)
            }
        except Exception:
            return None

    def _check_accessibility(self, url):
        """Check basic accessibility features"""
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return {
                'images_with_alt': len(soup.find_all('img', alt=True)),
                'images_without_alt': len(soup.find_all('img', alt=False)),
                'aria_landmarks': len(soup.find_all(attrs={"role": True})),
                'form_labels': len(soup.find_all('label')),
                'skip_links': len(soup.find_all('a', attrs={'href': '#main'}))
            }
        except Exception:
            return None

    def _check_w3c_validity(self, url):
        """Check W3C validity with detailed messages"""
        try:
            validator_url = f"https://validator.w3.org/nu/?doc={url}&out=json"
            response = requests.get(validator_url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            })
            
            if response.status_code == 200:
                results = response.json()
                return {
                    'errors': len([m for m in results['messages'] if m['type'] == 'error']),
                    'warnings': len([m for m in results['messages'] if m['type'] == 'warning']),
                    'messages': [
                        {
                            'type': msg['type'],
                            'message': msg['message'],
                            'line': msg.get('lastLine', 'unknown'),
                            'extract': msg.get('extract', ''),
                            'selector': msg.get('selector', '')
                        }
                        for msg in results['messages']
                    ]
                }
            return None
        except Exception as e:
            print(f"Error checking W3C validity: {str(e)}")
            return None

    def _get_pagespeed_data(self, url):
        """Get PageSpeed Insights data"""
        try:
            api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return {
                    'performance_score': data['lighthouseResult']['categories']['performance']['score'] * 100,
                    'first_contentful_paint': data['lighthouseResult']['audits']['first-contentful-paint']['displayValue'],
                    'speed_index': data['lighthouseResult']['audits']['speed-index']['displayValue'],
                    'time_to_interactive': data['lighthouseResult']['audits']['interactive']['displayValue']
                }
            return None
        except Exception:
            return None

    def _check_mozilla_observatory(self, url):
        """Check Mozilla Observatory security score"""
        try:
            api_url = f"https://http-observatory.security.mozilla.org/api/v1/analyze?host={urlparse(url).netloc}"
            response = requests.post(api_url)
            if response.status_code == 200:
                data = response.json()
                return {
                    'score': data.get('score'),
                    'grade': data.get('grade'),
                    'tests_passed': data.get('tests_passed'),
                    'tests_failed': data.get('tests_failed')
                }
            return None
        except Exception:
            return None

    def _parse_robots_txt(self, content):
        """Parse robots.txt content"""
        user_agents = {}
        current_agent = None
        
        for line in content.split('\n'):
            line = line.strip().lower()
            if line.startswith('user-agent:'):
                current_agent = line.split(':', 1)[1].strip()
                user_agents[current_agent] = []
            elif line.startswith('disallow:') or line.startswith('allow:'):
                if current_agent:
                    user_agents[current_agent].append(line)
                    
        return user_agents

    def _get_latest_sitemap_date(self, urls):
        """Get the latest modification date from sitemap"""
        latest_date = None
        for url in urls:
            lastmod = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
            if lastmod is not None and (latest_date is None or lastmod.text > latest_date):
                latest_date = lastmod.text
        return latest_date

    def _check_responsive_images(self, soup):
        """Check for responsive image features"""
        images = soup.find_all('img')
        return {
            'total': len(images),
            'srcset': len([img for img in images if img.get('srcset')]),
            'sizes': len([img for img in images if img.get('sizes')])
        } 