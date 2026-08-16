"""
Terminal display utilities for the Weather Dashboard.
"""

from typing import Any, Dict, List

from .weather_parser import (
    format_datetime,
    format_temperature,
    format_time,
    get_wind_direction,
)


def print_header(title: str) -> None:
    """Display a formatted section header."""

    print("\n" + "=" * 65)
    print(f"{title:^65}")
    print("=" * 65)


def display_current_weather(
    weather: Dict[str, Any],
    unit: str = "C",
) -> None:
    """Display current weather."""

    print_header("CURRENT WEATHER")

    location = weather.get("city", "Unknown")

    country = weather.get("country", "")

    print(f"\n📍 Location: {location}, {country}")

    updated = weather.get("updated")

    if updated:
        print(
            f"🕐 Updated: {format_datetime(updated)}"
        )

    print("\n" + "-" * 65)

    temperature = weather.get("temperature", 0)
    feels_like = weather.get("feels_like", 0)

    print(
        f"🌡️  Temperature : "
        f"{format_temperature(temperature, unit)}"
    )

    print(
        f"🤗 Feels Like  : "
        f"{format_temperature(feels_like, unit)}"
    )

    print(
        f"{weather.get('icon', '🌤️')} "
        f"Conditions   : {weather.get('description', 'Unknown')}"
    )

    print(
        f"💧 Humidity    : "
        f"{weather.get('humidity', 0)}%"
    )

    wind_speed = weather.get("wind_speed", 0)
    wind_direction = get_wind_direction(
        weather.get("wind_direction", 0)
    )

    if unit.upper() == "F":
        wind_unit = "mph"
    else:
        wind_unit = "m/s"

    print(
        f"💨 Wind        : "
        f"{wind_speed:.1f} {wind_unit} "
        f"from {wind_direction}"
    )

    print(
        f"🧭 Pressure    : "
        f"{weather.get('pressure', 0)} hPa"
    )

    visibility = weather.get("visibility", 0)

    if visibility:
        print(
            f"👁️  Visibility  : "
            f"{visibility / 1000:.1f} km"
        )

    sunrise = weather.get("sunrise")

    sunset = weather.get("sunset")

    if sunrise:
        print(
            f"🌅 Sunrise     : "
            f"{format_time(sunrise)}"
        )

    if sunset:
        print(
            f"🌇 Sunset      : "
            f"{format_time(sunset)}"
        )


def display_forecast(
    forecast: List[Dict[str, Any]],
    unit: str = "C",
) -> None:
    """Display 5-day forecast."""

    print_header("5-DAY WEATHER FORECAST")

    if not forecast:
        print("\nNo forecast data available.")
        return

    print()

    for item in forecast:
        temperature = format_temperature(
            item.get("temperature", 0),
            unit,
        )

        feels_like = format_temperature(
            item.get("feels_like", 0),
            unit,
        )

        print(
            f"{item.get('date', 'Unknown'):12} "
            f"{item.get('icon', '🌤️')}  "
            f"{temperature:>8}  "
            f"{item.get('description', 'Unknown'):<20} "
            f"Humidity: {item.get('humidity', 0):>3}%"
        )

        print(
            f"{'':12} Feels like: {feels_like}"
        )


def display_weather_dashboard(
    current: Dict[str, Any],
    forecast: List[Dict[str, Any]],
    unit: str = "C",
) -> None:
    """Display the complete weather dashboard."""

    print_header("🌤️ WEATHER DASHBOARD")

    display_current_weather(
        current,
        unit,
    )

    display_forecast(
        forecast,
        unit,
    )


def display_error(message: str) -> None:
    """Display an error message."""

    print(f"\n❌ Error: {message}")


def display_help() -> None:
    """Display application help."""

    print_header("HELP")

    print(
        """
Commands:

  search <city>     Search for weather in a city
  refresh           Refresh current weather
  unit              Change Celsius/Fahrenheit
  favorites         View favorite cities
  addfav <city>     Add a favorite city
  removefav <city>  Remove a favorite city
  export            Export current weather to CSV
  help              Show this help
  quit              Exit the application
        """
    )