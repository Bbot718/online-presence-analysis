import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import nltk
from urllib.parse import urljoin
import trafilatura
import ssl
from pathlib import Path

class ContentCollector:
    def __init__(self):
        # Fix SSL certificate verification for NLTK downloads
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        # Download all required NLTK data
        required_packages = [
            'punkt',
            'averaged_perceptron_tagger',
            'stopwords',
            'punkt/PY3/english.pickle'
        ]

        for package in required_packages:
            try:
                nltk.download(package, quiet=True)
            except Exception as e:
                print(f"Error downloading NLTK package {package}: {str(e)}")

        # Create custom punkt_tab if needed
        punkt_tab_dir = Path(nltk.data.find('tokenizers/punkt')).parent / 'punkt_tab' / 'english'
        punkt_tab_dir.mkdir(parents=True, exist_ok=True)
        
        if not (punkt_tab_dir / 'punkt.tab').exists():
            # Create a basic punkt.tab file
            with open(punkt_tab_dir / 'punkt.tab', 'w') as f:
                f.write(".\t.\tABBR\n")

        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def collect_data(self, url):
        """Collect and analyze content from the website"""
        try:
            # Get main content using trafilatura (better at extracting main content)
            downloaded = trafilatura.fetch_url(url)
            main_content = trafilatura.extract(downloaded, include_links=True, include_images=True)
            
            # Get full HTML for additional analysis
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            content_data = {
                'main_content': main_content,
                'text_analysis': self._analyze_text(main_content),
                'readability': self._analyze_readability(main_content),
                'keyword_analysis': self._analyze_keywords(main_content),
                'structure_analysis': self._analyze_structure(soup),
                'media_analysis': self._analyze_media(soup, url),
                'sentiment_scores': self._analyze_sentiment(main_content)
            }
            
            return content_data
        except Exception as e:
            print(f"Error in content collection: {str(e)}")
            return {
                'text_content': '',
                'word_count': 0,
                'readability_scores': {},
                'sentiment_analysis': {},
                'keywords': []
            }

    def _analyze_text(self, text):
        """Analyze text content"""
        if not text:
            return {}
            
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in self.stop_words]
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
            'unique_words': len(set(words)),
            'lexical_density': len(set(words)) / len(words) if words else 0
        }

    def _analyze_readability(self, text):
        """Calculate readability metrics"""
        if not text:
            return {}
            
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        word_count = len([word for word in words if word.isalnum()])
        sentence_count = len(sentences)
        
        # Simplified Flesch Reading Ease score
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        syllable_count = self._count_syllables(text)
        avg_syllables_per_word = syllable_count / word_count if word_count > 0 else 0
        
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        return {
            'flesch_reading_ease': min(100, max(0, flesch_score)),  # Clamp between 0 and 100
            'avg_sentence_length': avg_sentence_length,
            'avg_syllables_per_word': avg_syllables_per_word,
            'complexity_level': self._get_complexity_level(flesch_score)
        }

    def _analyze_keywords(self, text):
        """Extract and analyze keywords"""
        if not text:
            return {}
            
        # Tokenize and clean words
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in self.stop_words]
        
        # Get word frequencies
        word_freq = Counter(words)
        
        # Extract bigrams
        bigrams = list(zip(words[:-1], words[1:]))
        bigram_freq = Counter([' '.join(bigram) for bigram in bigrams])
        
        # Get parts of speech
        pos_tags = pos_tag(words)
        
        return {
            'top_keywords': dict(word_freq.most_common(10)),
            'top_bigrams': dict(bigram_freq.most_common(5)),
            'keyword_density': {word: count/len(words) for word, count in word_freq.most_common(10)},
            'parts_of_speech': Counter(tag for word, tag in pos_tags)
        }

    def _analyze_structure(self, soup):
        """Analyze content structure"""
        return {
            'paragraphs': len(soup.find_all('p')),
            'lists': {
                'ul': len(soup.find_all('ul')),
                'ol': len(soup.find_all('ol'))
            },
            'tables': len(soup.find_all('table')),
            'blockquotes': len(soup.find_all('blockquote')),
            'sections': len(soup.find_all(['section', 'article', 'aside', 'nav']))
        }

    def _analyze_media(self, soup, base_url):
        """Analyze media content"""
        images = soup.find_all('img')
        videos = soup.find_all(['video', 'iframe[src*="youtube"], iframe[src*="vimeo"]'])
        
        return {
            'images': {
                'count': len(images),
                'with_alt': len([img for img in images if img.get('alt')]),
                'types': Counter(self._get_image_type(img.get('src', '')) for img in images)
            },
            'videos': {
                'count': len(videos),
                'platforms': Counter(self._get_video_platform(video.get('src', '')) for video in videos)
            }
        }

    def _analyze_sentiment(self, text):
        """Basic sentiment analysis"""
        if not text:
            return {}
            
        # This is a very basic sentiment analysis
        # In a production environment, you might want to use a proper sentiment analysis library
        positive_words = set(['good', 'great', 'awesome', 'excellent', 'happy', 'best'])
        negative_words = set(['bad', 'poor', 'terrible', 'worst', 'unhappy', 'disappointing'])
        
        words = word_tokenize(text.lower())
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        total_count = len(words)
        
        return {
            'positive_ratio': positive_count / total_count if total_count > 0 else 0,
            'negative_ratio': negative_count / total_count if total_count > 0 else 0,
            'neutral_ratio': (total_count - positive_count - negative_count) / total_count if total_count > 0 else 0
        }

    def _count_syllables(self, text):
        """Rough syllable count for English text"""
        text = text.lower()
        count = 0
        vowels = 'aeiouy'
        on_vowel = False
        
        for char in text:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
            
        return count

    def _get_complexity_level(self, flesch_score):
        """Convert Flesch score to complexity level"""
        if flesch_score >= 90:
            return "Very Easy"
        elif flesch_score >= 80:
            return "Easy"
        elif flesch_score >= 70:
            return "Fairly Easy"
        elif flesch_score >= 60:
            return "Standard"
        elif flesch_score >= 50:
            return "Fairly Difficult"
        elif flesch_score >= 30:
            return "Difficult"
        else:
            return "Very Difficult"

    def _get_image_type(self, src):
        """Get image type from src"""
        if not src:
            return 'unknown'
        if src.lower().endswith(('.jpg', '.jpeg')):
            return 'jpeg'
        elif src.lower().endswith('.png'):
            return 'png'
        elif src.lower().endswith('.gif'):
            return 'gif'
        elif src.lower().endswith('.svg'):
            return 'svg'
        return 'other'

    def _get_video_platform(self, src):
        """Get video platform from src"""
        if not src:
            return 'unknown'
        if 'youtube' in src.lower():
            return 'youtube'
        elif 'vimeo' in src.lower():
            return 'vimeo'
        return 'other'
