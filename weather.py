import datetime
import os
from typing import Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()  # Load .env file

# Initialize FastMCP server
mcp = FastMCP("weather")

OPENWEATHER_API_BASE = "https://api.openweathermap.org/data/2.5"
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
USER_AGENT = "weather-app/1.0"


async def _make_openweather_request(url: str) -> dict[str, Any] | None:
    """Make a request to the OpenWeather API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def _format_timestamp(
    timestamp: int, timezone_offset: int, date_format_string: str
) -> str:
    """Converts a UTC timestamp to a local time string using the provided format string."""
    utc_dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    local_dt = utc_dt.astimezone(
        datetime.timezone(datetime.timedelta(seconds=timezone_offset))
    )
    return local_dt.strftime(date_format_string)


def _format_weather(data: dict, city: str) -> str | None:
    """Format weather data into a readable string."""
    try:
        # Basic weather information
        weather_description = data["weather"][0]["description"]
        weather_icon = data["weather"][0]["icon"]

        # Temperature and comfort data
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        sea_level = data["main"]["sea_level"]
        ground_level = data["main"]["grnd_level"]

        # Wind information
        wind_speed = data["wind"]["speed"]
        wind_direction = data["wind"]["deg"]
        wind_gust = data["wind"].get("gust", "N/A")

        # Convert wind direction from degrees to cardinal direction
        directions = [
            "N",
            "NNE",
            "NE",
            "ENE",
            "E",
            "ESE",
            "SE",
            "SSE",
            "S",
            "SSW",
            "SW",
            "WSW",
            "W",
            "WNW",
            "NW",
            "NNW",
        ]
        cardinal_direction = directions[round(wind_direction / 22.5) % 16]

        # Additional information
        visibility = data.get("visibility", "N/A")
        if visibility != "N/A":
            visibility = f"{visibility / 1000} km"

        rain_data = data.get("rain", {}).get("1h", "No precipitation")
        if rain_data != "No precipitation":
            rain_data = f"{rain_data} mm/h"

        snow_data = data.get("snow", {}).get("1h", "No snow")
        if snow_data != "No snow":
            snow_data = f"{snow_data} mm/h"

        cloud_coverage = data.get("clouds", {}).get("all", "N/A")

        # Location and time information
        country = data["sys"]["country"]
        sunrise_timestamp = data["sys"]["sunrise"]
        sunset_timestamp = data["sys"]["sunset"]
        timezone_offset = data.get("timezone", 0)  # Timezone offset in seconds

        # Convert timestamps to readable time format using helper function
        sunrise_time = _format_timestamp(sunrise_timestamp, timezone_offset, "%H:%M:%S")
        sunset_time = _format_timestamp(sunset_timestamp, timezone_offset, "%H:%M:%S")

        # Get local time from the timestamp in data using helper function
        local_time = _format_timestamp(data["dt"], timezone_offset, "%Y-%m-%d %H:%M:%S")

        # Format the weather report with additional information
        weather_report = f"""
            Current Weather for {data["name"]}, {country} (as of {local_time})
            Temperature: {temp:.1f}°C (Feels like: {feels_like:.1f}°C)
            Temp Range: {temp_min:.1f}°C - {temp_max:.1f}°C
            Conditions: {weather_description.title()} (Icon: {weather_icon})
            Humidity: {humidity}%
            Visibility: {visibility}
            Precipitation (1h): {rain_data}
            Snow (1h): {snow_data}
            Cloud Coverage: {cloud_coverage}%
            Wind: {wind_speed} m/s, Direction: {cardinal_direction} ({wind_direction}°)
            Wind Gusts: {wind_gust} m/s
            Atmospheric pressure: {pressure} hPa
            Sunrise: {sunrise_time}
            Sunset: {sunset_time}
            Sea level: {sea_level} hPa
            Ground level: {ground_level} hPa
            """
        return weather_report

    except KeyError as e:
        print(f"Error formatting weather data: {e}")
        return None


@mcp.tool()
async def get_forecast(city: str) -> str:
    """Get current weather for a city.

    Args:
        city: Name of the city (e.g. London, New York, etc.)
    """
    # Make a request to the OpenWeather API
    url = f"{OPENWEATHER_API_BASE}/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

    # Get weather data
    data = await _make_openweather_request(url)
    if not data:
        return f"Unable to fetch weather data for {city}. The city may not exist or there might be an API issue."

    # Format the weather data
    weather_report = _format_weather(data, city)

    if weather_report:
        return weather_report
    else:
        return f"Unable to parse weather data for {city}. The city may not exist or there might be an API issue."


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
