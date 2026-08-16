"""
Weather API client.

Handles:
- Current weather
- 5-day forecast
- API errors
- Response caching
"""

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from .config import API_KEY, BASE_URL, CACHE_DIR, CACHE_DURATION


class WeatherAPI:
    """Handles communication with the OpenWeatherMap API."""

    def __init__(
        self,
        api_key: str = API_KEY,
        base_url: str = BASE_URL,
        cache_duration: int = CACHE_DURATION,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.cache_duration = cache_duration

        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _create_cache_key(self, prefix: str, query: str) -> str:
        """Create a safe cache filename."""

        raw_key = f"{prefix}_{query.lower().strip()}"

        return hashlib.md5(
            raw_key.encode("utf-8")
        ).hexdigest()

    def _get_cache_file(self, cache_key: str) -> Path:
        """Return cache file path."""

        return CACHE_DIR / f"{cache_key}.json"

    def _get_cached_data(
        self,
        cache_key: str,
    ) -> Optional[Dict[str, Any]]:
        """Return cached data if it is still valid."""

        cache_file = self._get_cache_file(cache_key)

        if not cache_file.exists():
            return None

        try:
            modified_time = cache_file.stat().st_mtime
            age = time.time() - modified_time

            if age > self.cache_duration:
                return None

            with cache_file.open("r", encoding="utf-8") as file:
                return json.load(file)

        except (OSError, json.JSONDecodeError):
            return None

    def _save_to_cache(
        self,
        cache_key: str,
        data: Dict[str, Any],
    ) -> None:
        """Save API response to cache."""

        cache_file = self._get_cache_file(cache_key)

        try:
            with cache_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=2)

        except OSError:
            # Cache failure should not stop the application.
            pass

    def _make_request(
        self,
        endpoint: str,
        params: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """Make an HTTP request and handle common API errors."""

        if not self.api_key:
            print("\n[ERROR] Weather API key is not configured.")
            print("Please add WEATHER_API_KEY to your .env file.")
            return None

        request_params = dict(params)
        request_params["appid"] = self.api_key

        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=request_params,
                timeout=10,
            )

            if response.status_code == 200:
                return response.json()

            if response.status_code == 401:
                print("\n[ERROR] Invalid API key.")
                return None

            if response.status_code == 404:
                print("\n[ERROR] City not found.")
                return None

            if response.status_code == 429:
                print("\n[ERROR] API rate limit exceeded.")
                return None

            print(
                f"\n[ERROR] API request failed "
                f"with status {response.status_code}."
            )

        except requests.exceptions.Timeout:
            print("\n[ERROR] Request timed out.")

        except requests.exceptions.ConnectionError:
            print("\n[ERROR] Network connection error.")

        except requests.exceptions.RequestException as error:
            print(f"\n[ERROR] Request failed: {error}")

        return None

    def get_current_weather(
        self,
        city: str,
        country_code: Optional[str] = None,
        units: str = "metric",
        force_refresh: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """Get current weather for a city."""

        city = city.strip()

        query = city

        if country_code:
            query = f"{city},{country_code.strip()}"

        cache_key = self._create_cache_key(
            "current",
            f"{query}_{units}",
        )

        if not force_refresh:
            cached = self._get_cached_data(cache_key)

            if cached:
                return cached

        params = {
            "q": query,
            "units": units,
        }

        data = self._make_request("weather", params)

        if data:
            self._save_to_cache(cache_key, data)

        return data

    def get_forecast(
        self,
        city: str,
        country_code: Optional[str] = None,
        units: str = "metric",
        force_refresh: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """Get 5-day / 3-hour forecast for a city."""

        city = city.strip()

        query = city

        if country_code:
            query = f"{city},{country_code.strip()}"

        cache_key = self._create_cache_key(
            "forecast",
            f"{query}_{units}",
        )

        if not force_refresh:
            cached = self._get_cached_data(cache_key)

            if cached:
                return cached

        params = {
            "q": query,
            "units": units,
        }

        data = self._make_request("forecast", params)

        if data:
            self._save_to_cache(cache_key, data)

        return data

    def get_weather(
        self,
        city: str,
        units: str = "metric",
        force_refresh: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """
        Get both current weather and forecast.

        Returns:
            Dictionary containing current and forecast data.
        """

        current = self.get_current_weather(
            city,
            units=units,
            force_refresh=force_refresh,
        )

        if not current:
            return None

        forecast = self.get_forecast(
            city,
            units=units,
            force_refresh=force_refresh,
        )

        return {
            "current": current,
            "forecast": forecast,
        }