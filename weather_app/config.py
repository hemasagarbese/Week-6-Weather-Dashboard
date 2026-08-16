"""
Application configuration and environment management.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
EXPORT_DIR = DATA_DIR / "exports"

# Create required directories
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# Environment file
load_dotenv(BASE_DIR / ".env")

# API configuration
API_KEY = os.getenv("WEATHER_API_KEY", "")
BASE_URL = os.getenv(
    "WEATHER_API_BASE_URL",
    "https://api.openweathermap.org/data/2.5",
)

# Application settings
CACHE_DURATION = int(os.getenv("CACHE_DURATION", "600"))
DEFAULT_UNIT = os.getenv("DEFAULT_UNIT", "metric")

# Favorites
FAVORITES_FILE = DATA_DIR / "favorites.json"

# Supported units
UNIT_OPTIONS = {
    "C": "metric",
    "F": "imperial",
}


def validate_configuration():
    """Validate required application configuration."""

    if not API_KEY:
        return False

    return True