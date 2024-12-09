import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from llama_cpp import Llama

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
            
            # Store data as instance variables
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
                'score': self._calculate_seo_score(),
                'conclusion': self.generate_conclusion()
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
        """Calculate overall SEO score based on collected metrics with formula explanations"""
        llm = Llama(
            model_path="models/llama-2-7b-chat.Q4_K_M.gguf",
            n_ctx=2048,
            n_threads=4,
            verbose=False
        )

        # Initialize scores dictionary
        scores = {}

        # Meta Tags Score
        meta_score = 0
        if hasattr(self, '_meta_data'):
            meta = self._meta_data
            title_points = 20 if meta.get('title') else 0
            desc_points = 20 if meta.get('meta_description') else 0
            keywords_points = 15 if meta.get('meta_keywords') else 0
            robots_points = 15 if meta.get('robots') else 0
            viewport_points = 15 if meta.get('viewport') else 0
            charset_points = 15 if meta.get('charset') else 0
            meta_score = title_points + desc_points + keywords_points + robots_points + viewport_points + charset_points

        meta_prompt = f"""Score breakdown (max 100):
- Title: {20 if meta.get('title') else 0}/20 points
- Meta description: {20 if meta.get('meta_description') else 0}/20 points
- Meta keywords: {15 if meta.get('meta_keywords') else 0}/15 points
- Robots tag: {15 if meta.get('robots') else 0}/15 points
- Viewport tag: {15 if meta.get('viewport') else 0}/15 points
- Charset: {15 if meta.get('charset') else 0}/15 points"""

        scores['meta_tags'] = {
            'value': meta_score,
            'description': meta_prompt
        }

        # Similar updates for other scores...
        heading_score = 0
        if hasattr(self, '_headings'):
            h_tags = self._headings
            h1_count_points = 40 if h_tags.get('h1', {}).get('count') == 1 else 0
            h2_points = 20 if h_tags.get('h2', {}).get('count') > 0 else 0
            h1_length_points = 20 if all(len(content) < 70 for content in h_tags.get('h1', {}).get('content', [])) else 0
            total_headings_points = 20 if sum(h.get('count', 0) for h in h_tags.values()) < 15 else 0
            heading_score = h1_count_points + h2_points + h1_length_points + total_headings_points

        headings_prompt = f"""Score breakdown (max 100):
- Single H1 tag: {40 if h_tags.get('h1', {}).get('count') == 1 else 0}/40 points
- H2 tags present: {20 if h_tags.get('h2', {}).get('count') > 0 else 0}/20 points
- H1 length < 70 chars: {20 if all(len(content) < 70 for content in h_tags.get('h1', {}).get('content', [])) else 0}/20 points
- Total headings < 15: {20 if sum(h.get('count', 0) for h in h_tags.values()) < 15 else 0}/20 points"""

        scores['headings'] = {
            'value': heading_score,
            'description': headings_prompt
        }

        # Links Score
        links_score = 0
        if hasattr(self, '_links'):
            links = self._links
            internal_count = links.get('internal', {}).get('count', 0)
            external_count = links.get('external', {}).get('count', 0)
            internal_points = 40 if internal_count > 0 else 0
            external_points = 30 if external_count > 0 else 0
            ratio_points = 30 if internal_count > external_count else 0
            links_score = internal_points + external_points + ratio_points

        links_prompt = f"""Score breakdown (max 100):
- Has internal links: {40 if internal_count > 0 else 0}/40 points
- Has external links: {30 if external_count > 0 else 0}/30 points
- More internal than external: {30 if internal_count > external_count else 0}/30 points"""

        scores['links'] = {
            'value': links_score,
            'description': links_prompt
        }

        # Images Score
        images_score = 0
        if hasattr(self, '_images'):
            imgs = self._images
            total_images = imgs.get('total_count', 0)
            if total_images > 0:
                alt_ratio = imgs.get('with_alt', 0) / total_images
                images_score = int(alt_ratio * 100)

        images_prompt = f"""Score breakdown (max 100):
- Alt text coverage: {images_score}/100 points
  ({imgs.get('with_alt', 0)} of {total_images} images have alt text)"""

        scores['images'] = {
            'value': images_score,
            'description': images_prompt
        }

        # Mobile Score
        mobile_score = 0
        if hasattr(self, '_mobile_friendly'):
            mobile = self._mobile_friendly
            viewport_present = 50 if mobile.get('has_viewport') else 0
            viewport_content = mobile.get('viewport_content', '')
            device_width = 25 if 'width=device-width' in viewport_content else 0
            initial_scale = 25 if 'initial-scale=1' in viewport_content else 0
            mobile_score = viewport_present + device_width + initial_scale

        mobile_prompt = f"""Score breakdown (max 100):
- Viewport meta tag: {50 if mobile.get('has_viewport') else 0}/50 points
- width=device-width: {25 if 'width=device-width' in viewport_content else 0}/25 points
- initial-scale=1: {25 if 'initial-scale=1' in viewport_content else 0}/25 points"""

        scores['mobile'] = {
            'value': mobile_score,
            'description': mobile_prompt
        }

        # Overall Score
        weights = {
            'meta_tags': 0.25,
            'headings': 0.20,
            'links': 0.20,
            'images': 0.15,
            'mobile': 0.20
        }
        
        overall_score = sum(scores[key]['value'] * weights[key] for key in weights)

        overall_prompt = f"""Score breakdown (weighted average):
- Meta tags: {scores['meta_tags']['value']} × 25% = {scores['meta_tags']['value'] * 0.25:.1f}
- Headings: {scores['headings']['value']} × 20% = {scores['headings']['value'] * 0.20:.1f}
- Links: {scores['links']['value']} × 20% = {scores['links']['value'] * 0.20:.1f}
- Images: {scores['images']['value']} × 15% = {scores['images']['value'] * 0.15:.1f}
- Mobile: {scores['mobile']['value']} × 20% = {scores['mobile']['value'] * 0.20:.1f}"""

        scores['overall'] = {
            'value': round(overall_score),
            'description': overall_prompt
        }

        return scores

    def generate_conclusion(self):
        """Generate a structured SEO analysis report with minimal hallucination"""
        llm = Llama(
            model_path="models/llama-2-7b-chat.Q4_K_M.gguf",
            n_ctx=4096,
            n_threads=4,
            verbose=False
        )

        scores = self._calculate_seo_score()
        
        def get_completion(prompt, max_tokens=200):
            """Helper function to get completion with consistent parameters"""
            response = llm.create_completion(
                prompt,
                max_tokens=max_tokens,
                temperature=0.3,  # Reduced temperature for more focused responses
                top_p=0.1,       # Reduced top_p for less creativity
                repeat_penalty=1.2,
                stop=["<end>"]
            )
            return response['choices'][0]['text'].strip()

        # Executive Summary - restore previous version with clear data points
        executive_prompt = f"""Based on an overall SEO score of {scores['overall']['value']}/100, provide a concise overview of the website's SEO health. Include:

Current Metrics:
- Meta tags: {scores['meta_tags']['value']}/100
- Headings: {scores['headings']['value']}/100
- Links: {scores['links']['value']}/100 ({self._links['internal']['count']} internal, {self._links['external']['count']} external)
- Images: {scores['images']['value']}/100 ({self._images['with_alt']}/{self._images['total_count']} with alt text)
- Mobile: {scores['mobile']['value']}/100

Write 2-3 sentences describing the overall SEO health, mentioning both strengths and areas needing improvement. Focus on the actual scores and metrics provided."""

        # Critical Issues - only based on actual low scores and missing elements
        critical_issues = []
        if scores['meta_tags']['value'] < 100:
            if not self._meta_data.get('meta_description'):
                critical_issues.append("Missing meta description")
            if not self._meta_data.get('meta_keywords'):
                critical_issues.append("Missing meta keywords")
        
        if self._images['without_alt'] > 0:
            critical_issues.append(f"Missing alt text on {self._images['without_alt']} images")
        
        if self._links['internal']['count'] < self._links['external']['count']:
            critical_issues.append("More external links than internal links")

        issues_prompt = f"""For these specific issues, explain their SEO impact:
{chr(10).join(critical_issues)}"""

        # More creative recommendations and advantages sections
        recommendations_prompt = f"""Based on these specific SEO metrics:
- Meta score: {scores['meta_tags']['value']}/100 ({', '.join(critical_issues) if critical_issues else 'no issues'})
- Links: {self._links['internal']['count']} internal vs {self._links['external']['count']} external
- Images: {self._images['with_alt']}/{self._images['total_count']} optimized
- Overall score: {scores['overall']['value']}/100

Provide strategic recommendations in these timeframes:

1. Immediate Actions (Next 30 days): Focus on quick wins that will have immediate impact.
2. Medium-term (1-6 months): Strategic improvements that require planning.
3. Long-term Vision (6+ months): Transformative changes that could revolutionize the site's SEO.

Be specific, creative, and visionary, but ensure recommendations directly relate to the actual metrics."""

        advantages_prompt = f"""For a garage website with:
- Mobile score: {scores['mobile']['value']}/100
- Heading score: {scores['headings']['value']}/100
- Image score: {scores['images']['value']}/100
- Current strengths: {', '.join([k for k, v in scores.items() if v['value'] >= 90])}

1. Identify unique competitive advantages that set this site apart.
2. Suggest innovative growth opportunities that leverage current strengths.
3. Propose creative ways to transform weaknesses into unique selling points.

Focus on automotive industry-specific opportunities and digital transformation ideas."""

        # Split growth opportunities into practical and innovative
        practical_growth_prompt = f"""For a local garage website with:
- Current SEO score: {scores['overall']['value']}/100
- Main issues: {', '.join(critical_issues)}
- Strong points: {', '.join([k for k, v in scores.items() if v['value'] >= 90])}

Suggest practical, achievable growth opportunities that:
1. Are suitable for a small/medium local business
2. Can be implemented with limited resources
3. Focus on immediate business impact
4. Build on existing strengths
5. Address current weaknesses

Keep suggestions realistic and cost-effective for a local garage."""

        innovation_prompt = f"""For an automotive website with strong technical foundations:
- Mobile score: {scores['mobile']['value']}/100
- Overall SEO: {scores['overall']['value']}/100
- Digital presence: {self._links['internal']['count']} internal pages

Imagine future-focused innovations that could revolutionize the digital presence of automotive businesses. Consider:
1. Emerging technologies
2. Digital transformation trends
3. Future of automotive services
4. Customer experience innovations
5. Competitive differentiation

Think big and visionary, but keep the automotive industry context."""

        # Build the structured report
        report = {
            "seo_audit_report": {
                "executive_summary": {
                    "overview": get_completion(executive_prompt),
                    "key_findings": critical_issues[:3]  # Only use actual found issues
                },
                "critical_issues": [
                    {
                        "issue": issue,
                        "impact": get_completion(f"What is the SEO impact of: {issue}? Answer in one sentence.")
                    }
                    for issue in critical_issues
                ],
                "detailed_analysis": {
                    "meta_tags_and_content": {
                        "title": self._meta_data.get('title'),
                        "meta_description": self._meta_data.get('meta_description'),
                        "issues": [
                            f"Missing {tag}" for tag in ['meta_description', 'meta_keywords'] 
                            if not self._meta_data.get(tag)
                        ],
                        "score": scores['meta_tags']['value']
                    },
                    "heading_structure": {
                        "h1": self._headings['h1']['content'][0] if self._headings['h1']['content'] else None,
                        "h2_count": self._headings['h2']['count'],
                        "issues": [
                            "Multiple H1 tags" if self._headings['h1']['count'] > 1 else None,
                            "No H2 tags" if self._headings['h2']['count'] == 0 else None
                        ],
                        "score": scores['headings']['value']
                    },
                    "link_strategy": {
                        "internal_links": self._links['internal']['count'],
                        "external_links": self._links['external']['count'],
                        "distribution": f"{self._links['internal']['count']} internal vs {self._links['external']['count']} external",
                        "issues": [
                            "More external than internal links" if self._links['external']['count'] > self._links['internal']['count'] else None,
                            "Low internal link count" if self._links['internal']['count'] < 5 else None
                        ],
                        "score": scores['links']['value']
                    },
                    "image_optimization": {
                        "optimized_images": self._images['with_alt'],
                        "total_images": self._images['total_count'],
                        "issues": [
                            f"{self._images['without_alt']} images missing alt text" if self._images['without_alt'] > 0 else None
                        ],
                        "score": scores['images']['value']
                    },
                    "mobile_optimization": {
                        "viewport": self._mobile_friendly['viewport_content'],
                        "issues": [
                            "Missing viewport meta tag" if not self._mobile_friendly['has_viewport'] else None
                        ],
                        "score": scores['mobile']['value']
                    }
                },
                "actionable_recommendations": {
                    "immediate_actions": [
                        x.strip() for x in get_completion(
                            recommendations_prompt + "\nList 3-4 innovative immediate actions:",
                            max_tokens=300
                        ).split('\n') if x.strip()
                    ],
                    "medium_term_improvements": [
                        x.strip() for x in get_completion(
                            recommendations_prompt + "\nList 3-4 strategic medium-term improvements:",
                            max_tokens=300
                        ).split('\n') if x.strip()
                    ],
                    "long_term_strategy": [
                        x.strip() for x in get_completion(
                            recommendations_prompt + "\nList 3-4 visionary long-term strategies:",
                            max_tokens=300
                        ).split('\n') if x.strip()
                    ]
                },
                "competitive_advantages": {
                    "current_strengths": [
                        x.strip() for x in get_completion(
                            advantages_prompt + "\nList 3-4 unique competitive advantages:",
                            max_tokens=300
                        ).split('\n') if x.strip()
                    ],
                    "growth_opportunities": [
                        x.strip() for x in get_completion(
                            practical_growth_prompt + "\nList 3-4 practical growth opportunities:",
                            max_tokens=300
                        ).split('\n') if x.strip()
                    ],
                    "innovation_ideas": [
                        x.strip() for x in get_completion(
                            innovation_prompt + "\nList 2-3 innovative future possibilities:",
                            max_tokens=300
                        ).split('\n') if x.strip()
                    ]
                }
            }
        }

        # Clean up None values and empty lists
        report = {k: v for k, v in report.items() if v is not None}
        for section in report['seo_audit_report'].values():
            if isinstance(section, dict):
                for key, value in section.items():
                    if isinstance(value, list):
                        section[key] = [item for item in value if item is not None]

        return report
 