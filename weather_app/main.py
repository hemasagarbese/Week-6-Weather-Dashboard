"""
Main Weather Dashboard application.
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import (
    DEFAULT_UNIT,
    FAVORITES_FILE,
    UNIT_OPTIONS,
    validate_configuration,
)
from .weather_api import WeatherAPI
from .weather_display import (
    display_error,
    display_help,
    display_weather_dashboard,
)
from .weather_parser import (
    parse_current_weather,
    parse_forecast,
)


class WeatherDashboard:
    """Main application controller."""

    def __init__(self):
        self.unit = (
            "F"
            if DEFAULT_UNIT.lower() == "imperial"
            else "C"
        )

        self.api = WeatherAPI()

        self.current_city: Optional[str] = None
        self.current_data: Optional[Dict[str, Any]] = None

        self.favorites = self.load_favorites()

    def load_favorites(self) -> List[str]:
        """Load favorite cities from JSON."""

        if not FAVORITES_FILE.exists():
            return []

        try:
            with FAVORITES_FILE.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

        except (
            OSError,
            json.JSONDecodeError,
        ):
            print(
                "[WARNING] Could not load favorites."
            )

        return []

    def save_favorites(self) -> None:
        """Save favorite cities to JSON."""

        try:
            with FAVORITES_FILE.open(
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    self.favorites,
                    file,
                    indent=2,
                )

        except OSError as error:
            print(
                f"[ERROR] Could not save favorites: {error}"
            )

    def search_city(
        self,
        city: str,
        force_refresh: bool = False,
    ) -> bool:
        """Search weather for a city."""

        if not city.strip():
            display_error("City name cannot be empty.")
            return False

        units = UNIT_OPTIONS[self.unit]

        data = self.api.get_weather(
            city,
            units=units,
            force_refresh=force_refresh,
        )

        if not data:
            return False

        current_raw = data.get("current")
        forecast_raw = data.get("forecast")

        if not current_raw:
            display_error(
                "Current weather data unavailable."
            )
            return False

        current = parse_current_weather(
            current_raw
        )

        forecast = []

        if forecast_raw:
            forecast = parse_forecast(
                forecast_raw
            )

        self.current_city = current.get(
            "city",
            city,
        )

        self.current_data = {
            "current": current,
            "forecast": forecast,
        }

        display_weather_dashboard(
            current,
            forecast,
            self.unit,
        )

        return True

    def add_favorite(self, city: str) -> None:
        """Add a city to favorites."""

        city = city.strip()

        if not city:
            display_error(
                "City name cannot be empty."
            )
            return

        existing = [
            item.lower()
            for item in self.favorites
        ]

        if city.lower() in existing:
            print(
                f"\nℹ️ {city} is already a favorite."
            )
            return

        self.favorites.append(city)

        self.save_favorites()

        print(
            f"\n✅ {city} added to favorites."
        )

    def remove_favorite(self, city: str) -> None:
        """Remove a city from favorites."""

        city = city.strip()

        for favorite in self.favorites:
            if favorite.lower() == city.lower():
                self.favorites.remove(favorite)
                self.save_favorites()

                print(
                    f"\n✅ {favorite} removed from favorites."
                )
                return

        print(
            f"\nℹ️ {city} is not in favorites."
        )

    def show_favorites(self) -> None:
        """Display favorite cities."""

        print("\n" + "=" * 65)
        print(f"{'FAVORITE CITIES':^65}")
        print("=" * 65)

        if not self.favorites:
            print("\nNo favorite cities saved.")
            return

        for index, city in enumerate(
            self.favorites,
            start=1,
        ):
            print(f"{index}. {city}")

    def change_unit(self) -> None:
        """Switch between Celsius and Fahrenheit."""

        if self.unit == "C":
            self.unit = "F"
            print(
                "\n🌡️ Temperature unit changed to Fahrenheit."
            )
        else:
            self.unit = "C"
            print(
                "\n🌡️ Temperature unit changed to Celsius."
            )

        if self.current_city:
            print(
                "\nRefreshing weather with new unit..."
            )

            self.search_city(
                self.current_city,
                force_refresh=False,
            )

    def export_current_weather(self) -> None:
        """Export current weather to CSV."""

        if not self.current_data:
            display_error(
                "Search for a city first."
            )
            return

        current = self.current_data["current"]
        forecast = self.current_data["forecast"]

        export_dir = Path("data/exports")
        export_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            export_dir
            / f"weather_{timestamp}.csv"
        )

        try:
            with filename.open(
                "w",
                newline="",
                encoding="utf-8",
            ) as file:

                writer = csv.writer(file)

                writer.writerow(
                    [
                        "Date",
                        "City",
                        "Temperature",
                        "Feels Like",
                        "Condition",
                        "Humidity",
                    ]
                )

                writer.writerow(
                    [
                        current.get("updated"),
                        current.get("city"),
                        current.get("temperature"),
                        current.get("feels_like"),
                        current.get("description"),
                        current.get("humidity"),
                    ]
                )

                for item in forecast:
                    writer.writerow(
                        [
                            item.get("date"),
                            current.get("city"),
                            item.get("temperature"),
                            item.get("feels_like"),
                            item.get("description"),
                            item.get("humidity"),
                        ]
                    )

            print(
                f"\n✅ Weather exported to: {filename}"
            )

        except OSError as error:
            display_error(
                f"Could not export data: {error}"
            )

    def show_menu(self) -> None:
        """Display the main menu."""

        print("\n" + "=" * 65)
        print(
            "🌤️  WEATHER DASHBOARD".center(65)
        )
        print("=" * 65)

        print(
            """
1. Search City
2. Refresh Weather
3. Change Temperature Unit
4. Favorite Cities
5. Add Favorite City
6. Remove Favorite City
7. Export Weather to CSV
8. Help
9. Exit
"""
        )

        print("=" * 65)

    def run(self) -> None:
        """Run the interactive application."""

        print(
            "\n🌤️ Welcome to the Weather Dashboard!"
        )

        if not validate_configuration():
            print(
                "\n[WARNING] WEATHER_API_KEY is not configured."
            )
            print(
                "Add your API key to the .env file before "
                "searching for weather."
            )

        while True:
            self.show_menu()

            choice = input(
                "Enter your choice: "
            ).strip()

            if choice == "1":
                city = input(
                    "\nEnter city name: "
                ).strip()

                self.search_city(city)

            elif choice == "2":
                if self.current_city:
                    self.search_city(
                        self.current_city,
                        force_refresh=True,
                    )
                else:
                    print(
                        "\nNo city selected. "
                        "Search for a city first."
                    )

            elif choice == "3":
                self.change_unit()

            elif choice == "4":
                self.show_favorites()

            elif choice == "5":
                city = input(
                    "\nEnter city to add: "
                ).strip()

                self.add_favorite(city)

            elif choice == "6":
                city = input(
                    "\nEnter city to remove: "
                ).strip()

                self.remove_favorite(city)

            elif choice == "7":
                self.export_current_weather()

            elif choice == "8":
                display_help()

            elif choice == "9":
                print(
                    "\nThank you for using "
                    "Weather Dashboard! 🌤️"
                )
                break

            else:
                print(
                    "\n❌ Invalid choice. "
                    "Please select 1-9."
                )


def main():
    """Application entry point."""

    dashboard = WeatherDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()