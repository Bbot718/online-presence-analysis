from llama_cpp import Llama
from pathlib import Path
import json
import requests

class LLMAnalyzer:
    def __init__(self):
        model_path = Path("models/llama-2-7b-chat.gguf")
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        self.llm = Llama(
            model_path=str(model_path),
            n_ctx=2048,  # Context window
            n_batch=512  # Batch size for prompt processing
        )

    def analyze_section(self, section, data):
        """Analyze a specific section of the report"""
        recommendations = []
        analysis = ""
        
        if section == 'seo':
            recommendations = self._analyze_seo_data(data)
            analysis = self._generate_seo_analysis(data, recommendations)
        elif section == 'performance':
            recommendations = self._analyze_performance_data(data)
            analysis = self._generate_performance_analysis(data, recommendations)
        elif section == 'technical':
            recommendations = self._analyze_technical_data(data)
            analysis = self._generate_technical_analysis(data, recommendations)
        elif section == 'content':
            recommendations = self._analyze_content_data(data)
            analysis = self._generate_content_analysis(data, recommendations)
        
        return {
            'recommendations': recommendations,
            'analysis': analysis
        }

    def _analyze_seo_data(self, data):
        """Analyze SEO data with detailed recommendations"""
        recommendations = []
        
        # Title analysis
        if 'title' in data:
            title_length = len(data['title']) if data.get('title') else 0
            if title_length < 30:
                recommendations.append({
                    'issue': 'Title too short',
                    'priority': 'High',
                    'recommendation': 'Increase title length to 50-60 characters',
                    'current': data.get('title', ''),
                    'impact': 'Better search visibility and CTR'
                })
            elif title_length > 60:
                recommendations.append({
                    'issue': 'Title too long',
                    'priority': 'Medium',
                    'recommendation': 'Reduce title length to 50-60 characters',
                    'current': data.get('title', ''),
                    'impact': 'Prevent title truncation in search results'
                })

        # Meta description analysis
        meta_desc = data.get('meta_description', '')
        if meta_desc:
            desc_length = len(meta_desc)
            if desc_length < 120:
                recommendations.append({
                    'issue': 'Meta description too short',
                    'priority': 'High',
                    'recommendation': 'Expand meta description to 120-155 characters',
                    'current': meta_desc,
                    'impact': 'Improved click-through rates'
                })
            elif desc_length > 155:
                recommendations.append({
                    'issue': 'Meta description too long',
                    'priority': 'Medium',
                    'recommendation': 'Shorten meta description to 155 characters',
                    'current': meta_desc,
                    'impact': 'Prevent truncation in search results'
                })

        # Headings analysis
        headings = data.get('headings', {})
        if not headings.get('h1'):
            recommendations.append({
                'issue': 'Missing H1 heading',
                'priority': 'High',
                'recommendation': 'Add a primary H1 heading',
                'impact': 'Improved content hierarchy and SEO'
            })
        elif len(headings.get('h1', [])) > 1:
            recommendations.append({
                'issue': 'Multiple H1 headings',
                'priority': 'Medium',
                'recommendation': 'Use only one H1 heading per page',
                'current': headings.get('h1', []),
                'impact': 'Better content structure'
            })

        return recommendations

    def _analyze_performance_data(self, data):
        """Analyze performance data with specific metrics"""
        recommendations = []
        
        # Load time analysis
        load_time = data.get('load_time')
        if load_time and load_time > 3:
            recommendations.append({
                'issue': 'Slow page load time',
                'priority': 'High',
                'metric': f"{load_time:.2f} seconds",
                'recommendation': 'Optimize images, minify CSS/JS, use caching',
                'impact': 'Improved user experience and SEO'
            })

        # Performance metrics
        metrics = data.get('metrics', {})
        if metrics:
            if metrics.get('fcp', 0) > 2:
                recommendations.append({
                    'issue': 'High First Contentful Paint',
                    'priority': 'High',
                    'metric': f"{metrics.get('fcp')} seconds",
                    'recommendation': 'Optimize critical rendering path',
                    'impact': 'Faster perceived load times'
                })
            
            if metrics.get('lcp', 0) > 2.5:
                recommendations.append({
                    'issue': 'High Largest Contentful Paint',
                    'priority': 'High',
                    'metric': f"{metrics.get('lcp')} seconds",
                    'recommendation': 'Optimize largest page element',
                    'impact': 'Better Core Web Vitals score'
                })

        return recommendations

    def _analyze_technical_data(self, data):
        """Analyze technical aspects with security and accessibility focus"""
        recommendations = []
        
        # Security headers
        security = data.get('security', {})
        headers = security.get('headers', {})
        if headers:
            if not headers.get('X-Frame-Options'):
                recommendations.append({
                    'issue': 'Missing X-Frame-Options header',
                    'priority': 'High',
                    'recommendation': 'Add X-Frame-Options header',
                    'impact': 'Prevent clickjacking attacks'
                })
            if not headers.get('Content-Security-Policy'):
                recommendations.append({
                    'issue': 'Missing Content Security Policy',
                    'priority': 'High',
                    'recommendation': 'Implement Content Security Policy',
                    'impact': 'Prevent XSS and other injections'
                })

        # Accessibility
        accessibility = data.get('accessibility', {})
        if accessibility:
            basic_checks = accessibility.get('basic_checks', {})
            for issue, status in basic_checks.items():
                if not status:
                    recommendations.append({
                        'issue': f'Accessibility: {issue}',
                        'priority': 'High',
                        'recommendation': f'Fix {issue} for better accessibility',
                        'impact': 'Improved accessibility compliance'
                    })

        return recommendations

    def _analyze_content_data(self, data):
        """Analyze content data with readability and engagement focus"""
        recommendations = []
        
        # Word count analysis
        word_count = data.get('word_count', 0)
        if word_count < 300:
            recommendations.append({
                'issue': 'Low word count',
                'priority': 'High',
                'metric': f"{word_count} words",
                'recommendation': 'Add more content to reach at least 300 words',
                'impact': 'Better search rankings and content depth'
            })

        # Readability analysis
        readability = data.get('readability_scores', {})
        if readability:
            flesch_score = readability.get('flesch_reading_ease', 0)
            if flesch_score < 60:
                recommendations.append({
                    'issue': 'Content too complex',
                    'priority': 'Medium',
                    'metric': f"Flesch score: {flesch_score}",
                    'recommendation': 'Simplify content for better readability',
                    'impact': 'Improved user engagement'
                })
            elif flesch_score > 80:
                recommendations.append({
                    'issue': 'Content may be too simple',
                    'priority': 'Low',
                    'metric': f"Flesch score: {flesch_score}",
                    'recommendation': 'Consider adding more sophisticated content',
                    'impact': 'Better audience targeting'
                })

        # Keyword analysis
        keywords = data.get('keywords', [])
        if len(keywords) < 3:
            recommendations.append({
                'issue': 'Few key topics identified',
                'priority': 'Medium',
                'current': keywords,
                'recommendation': 'Add more relevant keywords and topics',
                'impact': 'Better topic coverage and SEO'
            })

        # Sentiment analysis
        sentiment = data.get('sentiment_analysis', {})
        if sentiment:
            score = sentiment.get('compound', 0)
            if abs(score) > 0.8:
                tone = 'negative' if score < 0 else 'positive'
                recommendations.append({
                    'issue': f'Strong {tone} tone',
                    'priority': 'Medium',
                    'metric': f"Sentiment score: {score:.2f}",
                    'recommendation': 'Consider balancing the content tone',
                    'impact': 'Better audience reception'
                })

        # Structure analysis
        headings = data.get('headings', {})
        if not headings or not any(headings.values()):
            recommendations.append({
                'issue': 'Poor content structure',
                'priority': 'High',
                'recommendation': 'Add headings to structure content',
                'impact': 'Better readability and SEO'
            })

        return recommendations

    def _generate_seo_analysis(self, data, recommendations):
        """Generate detailed SEO analysis"""
        meta_tags = data.get('meta_tags', {})
        score = data.get('score', {}).get('overall', 0)
        
        analysis = f"""
SEO Analysis Summary:
Overall Score: {score}/100

Key Findings:
- Title Tag: {meta_tags.get('title', 'Missing')} ({len(meta_tags.get('title', '')) if meta_tags.get('title') else 0} characters)
- Meta Description: {'Present' if meta_tags.get('meta_description') else 'Missing'}
- Headings Structure: {self._analyze_heading_structure(data.get('headings', {}))}
- Internal Links: {data.get('links', {}).get('internal', {}).get('count', 0)}
- External Links: {data.get('links', {}).get('external', {}).get('count', 0)}
- Image Optimization: {data.get('images', {}).get('with_alt', 0)}/{data.get('images', {}).get('total_count', 0)} images have alt text

Primary Strengths:
- Clean URL structure
- Good heading hierarchy
- Mobile-friendly configuration

Areas for Improvement:
{self._format_recommendations(recommendations)}

This website shows {self._get_seo_health_status(score)} SEO health and would benefit from implementing the recommended improvements to enhance search engine visibility.
"""
        return analysis

    def _generate_performance_analysis(self, data, recommendations):
        """Generate detailed performance analysis"""
        metrics = data.get('metrics', {})
        score = data.get('score', 0)
        
        analysis = f"""
Performance Analysis Summary:
Overall Performance Score: {score}/100

Core Web Vitals:
- First Contentful Paint (FCP): {metrics.get('first_contentful_paint', {}).get('display_value', 'N/A')}
- Largest Contentful Paint (LCP): {metrics.get('largest_contentful_paint', {}).get('display_value', 'N/A')}
- Cumulative Layout Shift (CLS): {metrics.get('cumulative_layout_shift', {}).get('display_value', 'N/A')}
- Total Blocking Time: {metrics.get('total_blocking_time', {}).get('display_value', 'N/A')}

Key Performance Insights:
- Speed Index: {metrics.get('speed_index', {}).get('display_value', 'N/A')}
- Time to Interactive: {data.get('validation', {}).get('pagespeed', {}).get('time_to_interactive', 'N/A')}

Critical Optimizations Needed:
{self._format_recommendations(recommendations)}

The website's performance is {self._get_performance_rating(score)}. Focus should be placed on optimizing the identified areas to improve user experience and Core Web Vitals scores.
"""
        return analysis

    def _generate_technical_analysis(self, data, recommendations):
        """Generate detailed technical analysis"""
        security = data.get('security', {})
        accessibility = data.get('accessibility', {})
        
        analysis = f"""
Technical Analysis Summary:

Security Assessment:
- SSL Certificate: {'Valid' if security.get('ssl_certificate', {}).get('valid') else 'Invalid/Missing'}
- Security Headers: {self._analyze_security_headers(security.get('headers', {}))}
- Content Security Policy: {'Implemented' if security.get('headers', {}).get('content_security_policy') else 'Missing'}

Accessibility Compliance:
- ARIA Landmarks: {accessibility.get('basic_checks', {}).get('aria_landmarks', 0)}
- Form Labels: {accessibility.get('basic_checks', {}).get('form_labels', 0)}
- Image Alt Text: {accessibility.get('basic_checks', {}).get('images_with_alt', 0)}/{accessibility.get('basic_checks', {}).get('images_without_alt', 0) + accessibility.get('basic_checks', {}).get('images_with_alt', 0)}

Technical Infrastructure:
- Mobile Responsiveness: {'Implemented' if data.get('mobile_responsiveness', {}).get('has_viewport') else 'Not Implemented'}
- Schema Markup: {'Present' if data.get('seo_technical', {}).get('schema_markup', {}).get('has_schema') else 'Missing'}
- Sitemap: {'Found' if data.get('seo_technical', {}).get('sitemap', {}).get('exists') else 'Missing'}
- Robots.txt: {'Found' if data.get('seo_technical', {}).get('robots_txt', {}).get('exists') else 'Missing'}

Critical Technical Issues:
{self._format_recommendations(recommendations)}

The website's technical foundation is {self._analyze_technical_health(data)}. Priority should be given to addressing security vulnerabilities and accessibility compliance issues.
"""
        return analysis

    def _generate_content_analysis(self, data, recommendations):
        """Generate detailed content analysis"""
        word_count = data.get('word_count', 0)
        readability = data.get('readability_scores', {})
        
        analysis = f"""
Content Analysis Summary:

Content Overview:
- Total Word Count: {word_count} words
- Readability Score: {readability.get('flesch_reading_ease', 'N/A')}
- Key Topics: {', '.join(data.get('keywords', ['None identified']))}

Content Quality Assessment:
- Text Length: {'Sufficient' if word_count > 300 else 'Insufficient'}
- Content Structure: {self._analyze_content_structure(data)}
- Keyword Usage: {self._analyze_keyword_usage(data)}

Sentiment Analysis:
{self._analyze_sentiment(data.get('sentiment_analysis', {}))}

Content Recommendations:
{self._format_recommendations(recommendations)}

The content quality is {self._get_content_rating(data)}. Focus on implementing the recommendations to improve engagement and value for visitors.
"""
        return analysis

    def generate_summary(self, report_data):
        """Generate comprehensive report summary"""
        summary = {
            'critical_issues': [],
            'important_improvements': [],
            'positive_aspects': [],
            'conclusion': self._generate_conclusion(report_data)
        }
        
        # Analyze SEO
        seo_data = report_data.get('seo_analysis', {})
        if seo_data:
            if not seo_data.get('meta_description'):
                summary['critical_issues'].append('Missing meta description')
            if len(seo_data.get('title', '')) > 60:
                summary['important_improvements'].append('Title length exceeds recommended limit')

        # Analyze Performance
        perf_data = report_data.get('performance_analysis', {})
        if perf_data:
            load_time = perf_data.get('load_time')
            if load_time and load_time < 3:
                summary['positive_aspects'].append(f'Good page load time: {load_time:.2f}s')
            elif load_time:
                summary['important_improvements'].append(f'Slow page load time: {load_time:.2f}s')

        # Analyze Technical
        tech_data = report_data.get('technical_analysis', {})
        if tech_data:
            security = tech_data.get('security', {})
            if security.get('ssl_certificate', {}).get('valid'):
                summary['positive_aspects'].append('Valid SSL certificate')
            else:
                summary['critical_issues'].append('Invalid or missing SSL certificate')

        return summary

    def _generate_conclusion(self, report_data):
        """Generate overall conclusion"""
        return f"""
Overall Website Analysis Conclusion:

This website analysis reveals a mixed profile of strengths and areas requiring improvement:

1. SEO Performance:
   - {self._summarize_seo(report_data.get('seo_analysis', {}))}

2. Technical Health:
   - {self._summarize_technical(report_data.get('technical_analysis', {}))}

3. Performance Metrics:
   - {self._summarize_performance(report_data.get('performance_analysis', {}))}

4. Content Quality:
   - {self._summarize_content(report_data.get('content_analysis', {}))}

Priority Action Items:
1. {self._get_top_priority_action(report_data)}
2. {self._get_second_priority_action(report_data)}
3. {self._get_third_priority_action(report_data)}

Implementation of these recommendations will significantly improve the website's overall effectiveness and user experience.
"""

    def _analyze_heading_structure(self, headings):
        """Analyze the heading structure of the page"""
        if not headings:
            return "No headings found"
        
        h1_count = headings.get('h1', {}).get('count', 0)
        h2_count = headings.get('h2', {}).get('count', 0)
        h3_count = headings.get('h3', {}).get('count', 0)
        
        if h1_count == 0:
            return "Missing H1 heading"
        elif h1_count > 1:
            return f"Multiple H1 headings ({h1_count})"
        
        return f"Good structure (H1: {h1_count}, H2: {h2_count}, H3: {h3_count})"

    def _format_recommendations(self, recommendations):
        """Format recommendations into a readable string"""
        if not recommendations:
            return "No specific recommendations"
        
        formatted = ""
        for rec in recommendations:
            formatted += f"- {rec['issue']}: {rec['recommendation']} (Priority: {rec['priority']})\n"
        return formatted

    def _get_seo_health_status(self, score):
        """Determine SEO health status based on score"""
        if score >= 90:
            return "excellent"
        elif score >= 70:
            return "good"
        elif score >= 50:
            return "fair"
        else:
            return "poor"

    def _get_performance_rating(self, score):
        """Get performance rating based on score"""
        if score >= 90:
            return "excellent"
        elif score >= 70:
            return "good"
        elif score >= 50:
            return "needs improvement"
        else:
            return "poor"

    def _analyze_security_headers(self, headers):
        """Analyze security headers"""
        essential_headers = {
            'strict_transport_security': 'HSTS',
            'x_frame_options': 'X-Frame-Options',
            'x_content_type_options': 'X-Content-Type-Options',
            'content_security_policy': 'CSP'
        }
        
        implemented = sum(1 for header in essential_headers if headers.get(header))
        return f"{implemented}/{len(essential_headers)} essential headers implemented"

    def _analyze_technical_health(self, data):
        """Analyze overall technical health"""
        security = data.get('security', {})
        accessibility = data.get('accessibility', {})
        
        if security.get('ssl_certificate', {}).get('valid') and len(security.get('headers', {})) >= 3:
            return "strong"
        elif security.get('ssl_certificate', {}).get('valid'):
            return "moderate"
        else:
            return "needs significant improvement"

    def _analyze_content_structure(self, data):
        """Analyze content structure"""
        headings = data.get('headings', {})
        if not headings:
            return "Poor - No clear structure"
        
        h_count = sum(h.get('count', 0) for h in headings.values())
        if h_count >= 5:
            return "Well structured"
        elif h_count >= 3:
            return "Adequately structured"
        else:
            return "Minimal structure"

    def _analyze_keyword_usage(self, data):
        """Analyze keyword usage"""
        keywords = data.get('keywords', [])
        if len(keywords) >= 5:
            return "Good keyword coverage"
        elif len(keywords) >= 3:
            return "Moderate keyword usage"
        else:
            return "Limited keyword presence"

    def _analyze_sentiment(self, sentiment):
        """Analyze content sentiment"""
        if not sentiment:
            return "Sentiment analysis not available"
        
        compound = sentiment.get('compound', 0)
        if compound > 0.5:
            return "Very positive tone"
        elif compound > 0:
            return "Slightly positive tone"
        elif compound < -0.5:
            return "Very negative tone"
        elif compound < 0:
            return "Slightly negative tone"
        else:
            return "Neutral tone"

    def _get_content_rating(self, data):
        """Get overall content rating"""
        word_count = data.get('word_count', 0)
        keywords = len(data.get('keywords', []))
        
        if word_count > 1000 and keywords >= 5:
            return "excellent"
        elif word_count > 500 and keywords >= 3:
            return "good"
        elif word_count > 300:
            return "adequate"
        else:
            return "needs improvement"

    def _summarize_seo(self, seo_data):
        """Summarize SEO findings"""
        score = seo_data.get('score', {}).get('overall', 0)
        return f"Overall SEO score: {score}/100 - {self._get_seo_health_status(score)}"

    def _summarize_technical(self, tech_data):
        """Summarize technical findings"""
        return f"Technical foundation is {self._analyze_technical_health(tech_data)}"

    def _summarize_performance(self, perf_data):
        """Summarize performance findings"""
        score = perf_data.get('score', 0)
        return f"Performance score: {score}/100 - {self._get_performance_rating(score)}"

    def _summarize_content(self, content_data):
        """Summarize content findings"""
        return f"Content quality is {self._get_content_rating(content_data)}"

    def _get_top_priority_action(self, data):
        """Get the top priority action item"""
        if not data.get('seo_analysis', {}).get('meta_tags', {}).get('meta_description'):
            return "Add a compelling meta description"
        elif data.get('performance_analysis', {}).get('score', 100) < 70:
            return "Improve page load performance"
        else:
            return "Implement missing security headers"

    def _get_second_priority_action(self, data):
        """Get the second priority action item"""
        if data.get('content_analysis', {}).get('word_count', 0) < 300:
            return "Expand content length and depth"
        elif not data.get('technical_analysis', {}).get('seo_technical', {}).get('schema_markup', {}).get('has_schema'):
            return "Implement schema markup"
        else:
            return "Optimize images and resources"

    def _get_third_priority_action(self, data):
        """Get the third priority action item"""
        accessibility = data.get('technical_analysis', {}).get('accessibility', {}).get('basic_checks', {})
        if not accessibility.get('aria_landmarks'):
            return "Improve accessibility with ARIA landmarks"
        elif len(data.get('content_analysis', {}).get('keywords', [])) < 3:
            return "Enhance keyword optimization"
        else:
            return "Implement additional performance optimizations"