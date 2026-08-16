# 🌤️ Weather Dashboard Application

## Week 6 - Working with External Libraries

A Python-based Weather Dashboard that retrieves real-time weather information using the OpenWeatherMap API.

## Features

- Current weather for any city
- 5-day weather forecast
- Temperature display in Celsius/Fahrenheit
- Humidity
- Wind speed and direction
- Atmospheric pressure
- Visibility
- Sunrise and sunset
- Weather condition icons
- API error handling
- Response caching
- Favorite cities
- CSV export
- Interactive CLI
- Unit testing

## Technologies

- Python
- Requests
- python-dotenv
- OpenWeatherMap API
- JSON
- CSV
- unittest

## Project Structure

```text
week6-weather-dashboard/
│
├── weather_app/
│   ├── __init__.py
│   ├── config.py
│   ├── weather_api.py
│   ├── weather_parser.py
│   ├── weather_display.py
│   └── main.py
│
├── data/
│   ├── cache/
│   ├── exports/
│   └── favorites.json
│
├── tests/
│   ├── test_api.py
│   ├── test_parser.py
│   └── test_display.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md