from .error_handler import ErrorHandler
from ..config.settings import REQUEST_HEADERS, REQUEST_DELAY
import time
import requests

class BaseCollector:
    def __init__(self):
        self.error_handler = ErrorHandler()
        self.headers = REQUEST_HEADERS
        self.delay = REQUEST_DELAY

    def make_request(self, url: str, method: str = 'GET', **kwargs) -> requests.Response:
        """Make HTTP request with error handling and rate limiting"""
        try:
            time.sleep(self.delay)  # Rate limiting
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response
        except Exception as e:
            self.error_handler.log_error(e, "HTTP Request", url)
            raise 