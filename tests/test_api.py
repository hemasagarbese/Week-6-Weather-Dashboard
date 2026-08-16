import unittest
from pathlib import Path
from unittest.mock import patch

from weather_app.weather_api import WeatherAPI


class TestWeatherAPI(unittest.TestCase):

    def setUp(self):
        self.api = WeatherAPI(
            api_key="test-key",
            cache_duration=600,
        )

    def test_cache_key_is_consistent(self):
        key1 = self.api._create_cache_key(
            "current",
            "London_metric",
        )

        key2 = self.api._create_cache_key(
            "current",
            "London_metric",
        )

        self.assertEqual(key1, key2)

    def test_cache_file_path(self):
        key = self.api._create_cache_key(
            "current",
            "London_metric",
        )

        path = self.api._get_cache_file(key)

        self.assertIsInstance(path, Path)

    @patch("weather_app.weather_api.requests.get")
    def test_successful_request(self, mock_get):

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "name": "London"
        }

        result = self.api._make_request(
            "weather",
            {
                "q": "London",
                "units": "metric",
            },
        )

        self.assertEqual(
            result["name"],
            "London",
        )

    @patch("weather_app.weather_api.requests.get")
    def test_city_not_found(self, mock_get):

        mock_get.return_value.status_code = 404

        result = self.api._make_request(
            "weather",
            {"q": "InvalidCity"},
        )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()