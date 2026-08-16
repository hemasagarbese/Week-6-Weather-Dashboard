# 🌤️ Week 6 – Weather Dashboard Application

A Python-based command-line Weather Dashboard developed as part of **The Developers Arena Python Internship – Week 6**.

The application uses an external weather API to retrieve real-time weather information and provides features such as city search, 5-day forecasts, temperature conversion, favorite cities, caching, and CSV export.

---

## 📌 Project Overview

The Weather Dashboard demonstrates practical usage of:

* Python external libraries
* HTTP API requests
* JSON data processing
* Environment variables
* API error handling
* Response caching
* Date and time formatting
* CSV file handling
* Modular Python programming

---

## ✨ Features

* 🌍 Search weather for cities worldwide
* 🌡️ Display temperature in Celsius and Fahrenheit
* 🤗 Show feels-like temperature
* ☁️ Display weather conditions
* 💧 Show humidity
* 💨 Show wind speed and direction
* 🧭 Display atmospheric pressure
* 👁️ Display visibility
* 🌅 Show sunrise and sunset
* 📅 Display a 5-day weather forecast
* ⭐ Add favorite cities
* 📋 View favorite cities
* ❌ Remove favorite cities
* 🔄 Refresh weather information
* 💾 Cache API responses
* 📊 Export weather information to CSV
* ❓ Built-in help system
* ⚠️ Handle invalid cities and API errors

---

## 🛠️ Technologies Used

| Technology         | Purpose                         |
| ------------------ | ------------------------------- |
| Python             | Application development         |
| Requests           | HTTP API requests               |
| python-dotenv      | Environment variable management |
| JSON               | Weather data processing         |
| CSV                | Weather data export             |
| OpenWeatherMap API | Weather information             |
| pathlib            | File and directory management   |
| datetime           | Date and time formatting        |

---

## 📁 Project Structure

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
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/hemasagarbese/Week-6-Weather-Dashboard.git
```

### 2. Open the Project

```bash
cd Week-6-Weather-Dashboard
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

**Windows PowerShell:**

```powershell
venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Configuration

Create a `.env` file in the project root:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

Do not upload your actual API key to GitHub.

The `.env` file should be included in `.gitignore.

---

## ▶️ Running the Application

Run the application using:

```bash
python -m weather_app.main
```

You should see:

```text
🌤️ Welcome to the Weather Dashboard!

=================================================================
                      🌤️ WEATHER DASHBOARD
=================================================================

1. Search City
2. Refresh Weather
3. Change Temperature Unit
4. Favorite Cities
5. Add Favorite City
6. Remove Favorite City
7. Export Weather to CSV
8. Help
9. Exit
```

---

## 🌍 Searching for Weather

Select:

```text
Enter your choice: 1
```

Then enter a city:

```text
Enter city name: Vizianagaram
```

The application displays:

```text
📍 Location: Vizianagaram, IN

🌡️ Temperature : 31.4°C
🤗 Feels Like  : 36.3°C
☁️ Conditions  : Overcast Clouds
💧 Humidity    : 62%
💨 Wind        : 3.9 m/s from W
🧭 Pressure    : 1003 hPa
👁️ Visibility  : 10.0 km
🌅 Sunrise     : 05:38
🌇 Sunset      : 18:22
```

---

## 📅 5-Day Forecast

The dashboard provides a forecast for the next five days.

Example:

```text
=================================================================
                     5-DAY WEATHER FORECAST
=================================================================

Sun 16 Aug   ☁️   30.7°C  Overcast Clouds      Humidity: 63%
             Feels like: 35.0°C

Mon 17 Aug   ☁️   29.5°C  Overcast Clouds      Humidity: 60%
             Feels like: 32.0°C

Tue 18 Aug   ☁️   34.9°C  Overcast Clouds      Humidity: 41%
             Feels like: 37.3°C

Wed 19 Aug   ☁️   36.1°C  Scattered Clouds     Humidity: 38%
             Feels like: 38.7°C

Thu 20 Aug   ☁️   34.6°C  Overcast Clouds      Humidity: 44%
             Feels like: 37.6°C
```

---

## 🌡️ Temperature Conversion

The application supports:

* Celsius
* Fahrenheit

Select:

```text
3. Change Temperature Unit
```

Example:

```text
🌡️ Temperature unit changed to Fahrenheit.
```

The weather information is then displayed using Fahrenheit.

---

## ⭐ Favorite Cities

Cities can be saved for quick access.

Example:

```text
Enter your choice: 5

Enter city to add: Vizianagaram, IN

✅ Vizianagaram, IN added to favorites.
```

Favorite cities can be viewed using:

```text
4. Favorite Cities
```

Example:

```text
=================================================================
                         FAVORITE CITIES
=================================================================

1. Vizianagaram, IN
2. Vizag, IN
3. Kakinada, IN
```

---

## 🔄 Refresh Weather

After searching for a city, select:

```text
2. Refresh Weather
```

The application retrieves the latest available weather information.

---

## 💾 API Response Caching

The application stores API responses in:

```text
data/cache/
```

Caching helps reduce unnecessary API requests and improves application performance.

---

## 📊 Export Weather Data

Weather information can be exported to CSV.

Select:

```text
7. Export Weather to CSV
```

If no city has been searched, the application displays:

```text
❌ Error: Search for a city first.
```

After searching for a city, the weather data can be exported successfully.

---

## ⚠️ Error Handling

The application handles common problems such as:

* Invalid city names
* Network errors
* API errors
* Missing API key
* Invalid menu selections
* Exporting before searching for a city

Example:

```text
[ERROR] City not found.
```

For an invalid menu option:

```text
❌ Invalid choice. Please select 1-9.
```

---

## ❓ Help System

The application includes a built-in help menu.

Example:

```text
=================================================================
                              HELP
=================================================================

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
```

---

## 🧪 Testing

Run the project tests using:

```bash
python -m unittest discover -s tests -v
```

The tests cover important parts of the application, including:

* API functionality
* Weather data parsing
* Weather display

---

## 🔐 Security

The API key is stored using an environment variable instead of being directly written in the source code.

Example:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

The `.env` file should never be committed to GitHub.

---

## 📸 Screenshots

The project includes screenshots demonstrating:

1. Home Screen
2. Search Weather
3. Refresh Weather
4. Temperature Unit Conversion
5. Favorite Cities
6. Add Favorite City
7. Export CSV
8. Help
9. Exit

---

## 🎯 Learning Outcomes

Through this project, I learned:

1. How to work with external Python libraries.
2. How to make HTTP API requests.
3. How to process JSON responses.
4. How to use environment variables.
5. How to handle API errors.
6. How to implement API caching.
7. How to work with CSV files.
8. How to organize a Python project into modules.
9. How to create an interactive command-line application.
10. How to test Python application components.

---

## 👨‍💻 Developer

**Bese Hema Sagar**

**B.Tech – Information Technology**

**JNTU-GV College of Engineering, Vizianagaram**

**The Developers Arena – Python Internship**

**Week 6 Project**

---

## 📄 License

This project was developed for educational and internship purposes.
