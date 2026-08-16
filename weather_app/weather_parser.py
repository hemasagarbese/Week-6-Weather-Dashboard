"""
Weather data parser and conversion utilities.
"""

from datetime import datetime
from typing import Any, Dict, List


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""

    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""

    return (fahrenheit - 32) * 5 / 9


def format_temperature(
    temperature: float,
    unit: str = "C",
) -> str:
    """Format temperature with the selected unit."""

    if unit.upper() == "F":
        value = celsius_to_fahrenheit(temperature)
        return f"{value:.1f}°F"

    return f"{temperature:.1f}°C"


def get_weather_icon(condition: str) -> str:
    """Return an emoji for a weather condition."""

    condition = condition.lower()

    icons = {
        "clear": "☀️",
        "clouds": "☁️",
        "rain": "🌧️",
        "drizzle": "🌦️",
        "thunderstorm": "⛈️",
        "snow": "❄️",
        "mist": "🌫️",
        "fog": "🌫️",
        "haze": "🌫️",
        "smoke": "🌫️",
        "dust": "🌫️",
        "sand": "🌫️",
        "ash": "🌋",
        "squall": "💨",
        "tornado": "🌪️",
    }

    return icons.get(condition, "🌤️")


def format_datetime(timestamp: int) -> str:
    """Convert Unix timestamp to readable local date/time."""

    return datetime.fromtimestamp(timestamp).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def format_time(timestamp: int) -> str:
    """Convert Unix timestamp to HH:MM."""

    return datetime.fromtimestamp(timestamp).strftime("%H:%M")


def parse_current_weather(
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """Parse current weather API response."""

    main = data.get("main", {})
    wind = data.get("wind", {})
    weather = data.get("weather", [{}])[0]
    system = data.get("sys", {})

    condition = weather.get("main", "Unknown")

    return {
        "city": data.get("name", "Unknown"),
        "country": system.get("country", ""),
        "temperature": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "pressure": main.get("pressure"),
        "wind_speed": wind.get("speed", 0),
        "wind_direction": wind.get("deg", 0),
        "visibility": data.get("visibility", 0),
        "condition": condition,
        "description": weather.get(
            "description",
            "Unknown",
        ).title(),
        "icon": get_weather_icon(condition),
        "sunrise": system.get("sunrise"),
        "sunset": system.get("sunset"),
        "updated": data.get("dt"),
    }


def parse_forecast(
    data: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Parse the 3-hour forecast response.

    Selects one forecast entry per day, approximately
    around midday where possible.
    """

    forecast_items = data.get("list", [])

    daily_data = {}

    for item in forecast_items:
        timestamp = item.get("dt")

        if not timestamp:
            continue

        date = datetime.fromtimestamp(timestamp).date()

        if date not in daily_data:
            daily_data[date] = item
            continue

        current_hour = datetime.fromtimestamp(
            daily_data[date]["dt"]
        ).hour

        new_hour = datetime.fromtimestamp(timestamp).hour

        if abs(new_hour - 12) < abs(current_hour - 12):
            daily_data[date] = item

    results = []

    for date, item in sorted(daily_data.items())[:5]:
        main = item.get("main", {})
        weather = item.get("weather", [{}])[0]

        condition = weather.get("main", "Unknown")

        results.append(
            {
                "date": date.strftime("%a %d %b"),
                "temperature": main.get("temp"),
                "feels_like": main.get("feels_like"),
                "humidity": main.get("humidity"),
                "condition": condition,
                "description": weather.get(
                    "description",
                    "Unknown",
                ).title(),
                "icon": get_weather_icon(condition),
            }
        )

    return results


def get_wind_direction(degrees: float) -> str:
    """Convert wind degrees to compass direction."""

    directions = [
        "N",
        "NE",
        "E",
        "SE",
        "S",
        "SW",
        "W",
        "NW",
    ]

    index = round(degrees / 45) % 8

    return directions[index]