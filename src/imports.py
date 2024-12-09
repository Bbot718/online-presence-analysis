# For data collection
import requests
from bs4 import BeautifulSoup
import dns.resolver
import whois
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pathlib import Path
import json
from urllib.parse import urlparse
import ssl
import socket
from typing import Dict, Optional, List

# For PDF generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.units import inch

# For LLM
from llama_cpp import Llama 