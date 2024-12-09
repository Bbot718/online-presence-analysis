from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "output"
CHARTS_DIR = OUTPUT_DIR / "charts"
LOGS_DIR = BASE_DIR / "logs"

# Create necessary directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# LLM Settings
LLAMA_SETTINGS = {
    'model_path': os.getenv('LLAMA_MODEL_PATH'),
    'n_threads': int(os.getenv('LLAMA_N_THREADS', 4)),
    'n_ctx': int(os.getenv('LLAMA_N_CTX', 2048))
}

# Request Settings
REQUEST_HEADERS = {
    'User-Agent': os.getenv('USER_AGENT')
}
REQUEST_DELAY = int(os.getenv('REQUEST_DELAY', 2))

# PDF Settings
PDF_SETTINGS = {
    'margin': 1 * inch,
    'page_size': A4,
    'title_font_size': 24,
    'heading_font_size': 18,
    'body_font_size': 12
} 