# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\productivity\weather.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(location: str):
    """
    Gets the current weather for a specified location using OpenWeatherMap.
    Args:
        location (str): The city name to get the weather for (e.g., "Chennai").
    """
    print(f"🛠️ TOOL: Running get_weather(location='{location}')...")
    if not API_KEY:
        return "OpenWeatherMap API key is not configured."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    try:
        params = {
            'q': location,
            'appid': API_KEY,
            'units': 'metric'  # Request temperature in Celsius
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        
        city = data.get('name')
        temp_c = data.get('main', {}).get('temp')
        condition = data.get('weather', [{}])[0].get('description')
        
        if not city or temp_c is None or not condition:
            return "Sorry, I couldn't get complete weather data for that location."
            
        return f"The current weather in {city} is {temp_c}°C with {condition}."
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Sorry, I couldn't find the city '{location}'. Please check the spelling."
        else:
            print(f"❌ Weather API HTTP Error: {e}")
            return "Sorry, there was an error communicating with the weather service."
    except requests.exceptions.RequestException as e:
        print(f"❌ Weather API Request Error: {e}")
        return "Sorry, I couldn't retrieve the weather information at this time."