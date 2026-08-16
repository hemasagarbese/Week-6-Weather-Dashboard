import unittest

from weather_app.weather_parser import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    format_temperature,
    get_weather_icon,
    get_wind_direction,
    parse_current_weather,
    parse_forecast,
)


class TestWeatherParser(unittest.TestCase):

    def test_celsius_to_fahrenheit(self):
        result = celsius_to_fahrenheit(0)

        self.assertEqual(result, 32)

    def test_fahrenheit_to_celsius(self):
        result = fahrenheit_to_celsius(32)

        self.assertEqual(result, 0)

    def test_format_temperature_celsius(self):
        result = format_temperature(25, "C")

        self.assertEqual(result, "25.0°C")

    def test_format_temperature_fahrenheit(self):
        result = format_temperature(0, "F")

        self.assertEqual(result, "32.0°F")

    def test_weather_icon(self):
        result = get_weather_icon("Clear")

        self.assertEqual(result, "☀️")

    def test_wind_direction(self):
        self.assertEqual(
            get_wind_direction(0),
            "N",
        )

        self.assertEqual(
            get_wind_direction(90),
            "E",
        )

        self.assertEqual(
            get_wind_direction(180),
            "S",
        )

    def test_parse_current_weather(self):

        data = {
            "name": "London",
            "main": {
                "temp": 10,
                "feels_like": 8,
                "humidity": 80,
                "pressure": 1010,
            },
            "wind": {
                "speed": 5,
                "deg": 180,
            },
            "weather": [
                {
                    "main": "Rain",
                    "description": "light rain",
                }
            ],
            "sys": {
                "country": "GB",
                "sunrise": 1000,
                "sunset": 2000,
            },
            "dt": 1500,
        }

        result = parse_current_weather(data)

        self.assertEqual(
            result["city"],
            "London",
        )

        self.assertEqual(
            result["country"],
            "GB",
        )

        self.assertEqual(
            result["temperature"],
            10,
        )

        self.assertEqual(
            result["condition"],
            "Rain",
        )

    def test_parse_forecast(self):

        data = {
            "list": [
                {
                    "dt": 1700000000,
                    "main": {
                        "temp": 15,
                        "feels_like": 14,
                        "humidity": 70,
                    },
                    "weather": [
                        {
                            "main": "Clouds",
                            "description": "few clouds",
                        }
                    ],
                }
            ]
        }

        result = parse_forecast(data)

        self.assertEqual(len(result), 1)

        self.assertEqual(
            result[0]["temperature"],
            15,
        )


if __name__ == "__main__":
    unittest.main()