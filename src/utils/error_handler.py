import logging
from pathlib import Path
from datetime import datetime

class ErrorHandler:
    def __init__(self):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        log_file = self.log_dir / f"website_analyzer_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def log_error(self, error: Exception, section: str, url: str):
        """Log errors with context"""
        self.logger.error(f"Error in {section} for {url}: {str(error)}")
        return f"Error in {section}: {str(error)}"

    def log_warning(self, message: str, section: str, url: str):
        """Log warnings with context"""
        self.logger.warning(f"Warning in {section} for {url}: {message}")