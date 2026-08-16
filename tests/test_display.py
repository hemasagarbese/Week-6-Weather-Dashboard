import unittest
from io import StringIO
from unittest.mock import patch

from weather_app.weather_display import (
    display_current_weather,
    display_forecast,
)


class TestWeatherDisplay(unittest.TestCase):

    def test_current_weather_display(self):

        weather = {
            "city": "London",
            "country": "GB",
            "temperature": 10,
            "feels_like": 8,
            "humidity": 80,
            "pressure": 1010,
            "wind_speed": 5,
            "wind_direction": 180,
            "visibility": 10000,
            "condition": "Rain",
            "description": "Light Rain",
            "icon": "🌧️",
            "updated": 1700000000,
        }

        with patch(
            "sys.stdout",
            new_callable=StringIO,
        ) as output:

            display_current_weather(
                weather,
                "C",
            )

            result = output.getvalue()

        self.assertIn(
            "London",
            result,
        )

        self.assertIn(
            "10.0°C",
            result,
        )

        self.assertIn(
            "80%",
            result,
        )

    def test_forecast_display(self):

        forecast = [
            {
                "date": "Mon 25 Aug",
                "temperature": 25,
                "feels_like": 24,
                "humidity": 60,
                "description": "Clear Sky",
                "icon": "☀️",
            }
        ]

        with patch(
            "sys.stdout",
            new_callable=StringIO,
        ) as output:

            display_forecast(
                forecast,
                "C",
            )

            result = output.getvalue()

        self.assertIn(
            "Mon 25 Aug",
            result,
        )

        self.assertIn(
            "25.0°C",
            result,
        )


if __name__ == "__main__":
    unittest.main()