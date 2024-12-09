from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "output"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SIMILARWEB_API_KEY = os.getenv("SIMILARWEB_API_KEY")

# PDF Settings
PDF_SETTINGS = {
    'page_size': 'A4',
    'margin': 72,  # 1 inch in points
    'font_family': 'Helvetica',
    'heading_font_size': 16,
    'body_font_size': 11,
    'missing_data_color': (1, 0, 0),  # Red color in RGB
}

# AI Settings
AI_SETTINGS = {
    'model': 'gpt-4',
    'temperature': 0.7,
    'max_tokens': 500,
} 