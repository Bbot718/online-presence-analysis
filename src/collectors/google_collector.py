from google.oauth2.credentials import Credentials
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, DateRange, Metric, Dimension
)
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
from pathlib import Path
from datetime import datetime, timedelta

class GoogleCollector:
    def __init__(self):
        # Load credentials from service account file
        credentials_path = Path("credentials/google-credentials.json")
        if not credentials_path.exists():
            raise FileNotFoundError(
                "Google credentials file not found. Please place your service account "
                "credentials in credentials/google-credentials.json"
            )
        
        self.credentials = service_account.Credentials.from_service_account_file(
            str(credentials_path),
            scopes=[
                'https://www.googleapis.com/auth/analytics.readonly',
                'https://www.googleapis.com/auth/webmasters.readonly',
                'https://www.googleapis.com/auth/business.manage'
            ]
        )
        
        # Initialize API clients
        self.analytics_client = BetaAnalyticsDataClient(credentials=self.credentials)
        self.search_console_service = build('searchconsole', 'v1', credentials=self.credentials)
        self.my_business_service = build('mybusiness', 'v4', credentials=self.credentials)

    def collect_data(self, url, property_id):
        """Collect all Google data for the website"""
        try:
            return {
                'analytics': self._get_analytics_data(property_id),
                'search_console': self._get_search_console_data(url),
                'reviews': self._get_business_reviews()
            }
        except Exception as e:
            print(f"Error collecting Google data: {str(e)}")
            return None

    def _get_analytics_data(self, property_id):
        """Collect Google Analytics data"""
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(
                start_date="30daysAgo",
                end_date="today"
            )],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="sessions"),
                Metric(name="bounceRate"),
                Metric(name="averageSessionDuration"),
                Metric(name="screenPageViews")
            ],
            dimensions=[Dimension(name="date")]
        )

        response = self.analytics_client.run_report(request)
        
        # Process the response
        analytics_data = {
            'user_metrics': self._process_analytics_metrics(response),
            'engagement_metrics': self._process_engagement_metrics(response)
        }
        
        return analytics_data

    def _get_search_console_data(self, url):
        """Collect Search Console data"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        request = {
            'startDate': start_date.isoformat(),
            'endDate': end_date.isoformat(),
            'dimensions': ['query', 'page'],
            'rowLimit': 25
        }
        
        response = self.search_console_service.searchanalytics().query(
            siteUrl=url,
            body=request
        ).execute()
        
        return {
            'search_metrics': self._process_search_metrics(response),
            'top_queries': self._process_top_queries(response)
        }

    def _get_business_reviews(self):
        """Collect Google Business Profile reviews"""
        # First get the account
        accounts = self.my_business_service.accounts().list().execute()
        if not accounts or 'accounts' not in accounts:
            return {}
            
        account = accounts['accounts'][0]
        account_name = account['name']
        
        # Then get the location
        locations = self.my_business_service.accounts().locations().list(
            parent=account_name
        ).execute()
        
        if not locations or 'locations' not in locations:
            return {}
            
        location = locations['locations'][0]
        location_name = location['name']
        
        # Finally get the reviews
        reviews = self.my_business_service.accounts().locations().reviews().list(
            parent=location_name
        ).execute()
        
        return self._process_reviews(reviews)

    def _process_analytics_metrics(self, response):
        """Process Analytics metrics"""
        metrics = {}
        for row in response.rows:
            date = row.dimension_values[0].value
            metrics[date] = {
                'active_users': int(row.metric_values[0].value),
                'sessions': int(row.metric_values[1].value),
                'bounce_rate': float(row.metric_values[2].value),
                'avg_session_duration': float(row.metric_values[3].value),
                'page_views': int(row.metric_values[4].value)
            }
        return metrics

    def _process_engagement_metrics(self, response):
        """Process engagement metrics"""
        total_users = sum(int(row.metric_values[0].value) for row in response.rows)
        total_sessions = sum(int(row.metric_values[1].value) for row in response.rows)
        avg_bounce_rate = sum(float(row.metric_values[2].value) for row in response.rows) / len(response.rows)
        
        return {
            'total_users': total_users,
            'total_sessions': total_sessions,
            'avg_bounce_rate': avg_bounce_rate,
            'users_trend': [int(row.metric_values[0].value) for row in response.rows]
        }

    def _process_search_metrics(self, response):
        """Process Search Console metrics"""
        if not response.get('rows'):
            return {}
            
        total_clicks = sum(row['clicks'] for row in response['rows'])
        total_impressions = sum(row['impressions'] for row in response['rows'])
        avg_position = sum(row['position'] for row in response['rows']) / len(response['rows'])
        
        return {
            'total_clicks': total_clicks,
            'total_impressions': total_impressions,
            'avg_position': avg_position,
            'ctr': total_clicks / total_impressions if total_impressions > 0 else 0
        }

    def _process_top_queries(self, response):
        """Process top search queries"""
        if not response.get('rows'):
            return {}
            
        queries = {}
        for row in response['rows']:
            queries[row['keys'][0]] = {
                'clicks': row['clicks'],
                'impressions': row['impressions'],
                'ctr': row['ctr'],
                'position': row['position']
            }
        return queries

    def _process_reviews(self, reviews):
        """Process Google Business reviews"""
        if not reviews.get('reviews'):
            return {}
            
        processed_reviews = {
            'average_rating': 0,
            'total_reviews': len(reviews['reviews']),
            'rating_distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            'recent_reviews': []
        }
        
        total_rating = 0
        for review in reviews['reviews']:
            rating = review['starRating']
            total_rating += rating
            processed_reviews['rating_distribution'][rating] += 1
            
            if len(processed_reviews['recent_reviews']) < 5:
                processed_reviews['recent_reviews'].append({
                    'rating': rating,
                    'comment': review.get('comment', ''),
                    'time': review['createTime']
                })
        
        processed_reviews['average_rating'] = total_rating / len(reviews['reviews'])
        return processed_reviews 