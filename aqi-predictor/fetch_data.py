import requests
import time
import pandas as pd
from datetime import datetime

# Latitude and Longitude for Delhi
lat = 28.7041
lon = 77.1025

# OpenWeatherMap API details
API_KEY = "c5716c8c430e90677358439fab343227"
BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution/history"

# Google Maps API details (for traffic and geographical data)
API_KEY_GOOGLEMAPS = "AIzaSyDrJzjYe-EZ5OX__KB8ZTLw8lkuLhERoi4"  # Replace with your actual API key
import googlemaps

gmaps = googlemaps.Client(key=API_KEY_GOOGLEMAPS)

# Define the time range (last 5 days for example)
end_time = int(time.time())  # Current time in Unix timestamp
start_time = end_time - (30 * 24 * 60 * 60)  # 5 days ago

# Fetch data from OpenWeatherMap
params = {
    "lat": lat,
    "lon": lon,
    "start": start_time,
    "end": end_time,
    "appid": API_KEY
}

response = requests.get(BASE_URL, params=params)


# Function to fetch air quality data from OpenWeatherMap
def fetch_air_quality():
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        pollutants = data.get("list", [])
        if pollutants:
            # Extracting components of the pollutants
            components = pollutants[0]["components"]
            aqi = pollutants[0]["main"]["aqi"]
            return components, aqi
        else:
            return None, None
    else:
        print(f"Failed to fetch air quality data. HTTP Status code: {response.status_code}")
        return None, None


# Function to fetch weather data
def fetch_weather():
    weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(weather_url)
    if response.status_code == 200:
        data = response.json()
        current_weather = data.get("current", {})
        weather_data = {
            "temperature": current_weather.get("temp", None),
            "humidity": current_weather.get("humidity", None),
            "wind_speed": current_weather.get("wind_speed", None),
            "precipitation": current_weather.get("rain", {}).get('1h', 0)  # Optional rain data
        }
        return weather_data
    else:
        print(f"Failed to fetch weather data. Status code: {response.status_code}")
        print(response.text)
        return {
            "temperature": None,
            "humidity": None,
            "wind_speed": None,
            "precipitation": None
        }



# Function to fetch traffic data
def fetch_traffic_data():
    # Example: Get traffic data for a route in Delhi (just as an example)
    # directions_result = gmaps.directions("Connaught Place, New Delhi", "Indira Gandhi Airport, Delhi",
    #                                      departure_time="now")
    # if directions_result:
    #     traffic_info = directions_result[0]['legs'][0]['duration_in_traffic']['text']
    #     return traffic_info
    # else:
    #     return None
    return "Traffic data not available"


# Function to fetch geographical data (industrial zones, etc.)
def fetch_geographical_data():
    # OpenWeatherMap Current Weather API endpoint
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"

    response = requests.get(url)

    # Check if the response status code is 200 (successful)
    if response.status_code == 200:
        try:
            data = response.json()
            # Example: extract latitude and longitude from the response
            latitude = data['coord']['lat']
            longitude = data['coord']['lon']
            return latitude, longitude
        except Exception as e:
            print(f"Error parsing JSON response: {e}")
            return None, None
    else:
        print(f"Failed to fetch geographical data. Status code: {response.status_code}")
        print(response.text)  # Print raw response to debug
        return None, None



# Function to fetch festive and seasonal data (Diwali, crop burning)
def fetch_festive_data():
    # Example: Input known dates for Diwali, crop burning, and seasonal patterns
    festive_data = {
        "diwali_date": "2024-11-12",  # Example date for Diwali
        "crop_burning_season": ["2024-10-15", "2024-11-15"],  # Approximate crop burning period
        "season": "Winter"
    }
    return festive_data


# Fetch data from all sources
def fetch_all_data():
    # Fetching air quality data
    pollutants, aqi = fetch_air_quality()

    # Fetching weather data
    weather_data = fetch_weather()

    # Fetching traffic data
    traffic_data = fetch_traffic_data()

    # Fetching geographical data
    latitude, longitude = fetch_geographical_data()

    # Fetching festive and seasonal data
    festive_data = fetch_festive_data()

    # Combine all data into a dictionary
    all_data = {
        "timestamp": datetime.now(),
        "aqi": aqi,
        "pm2_5": pollutants.get("pm2_5", None) if pollutants else None,
        "pm10": pollutants.get("pm10", None) if pollutants else None,
        "co": pollutants.get("co", None) if pollutants else None,
        "no2": pollutants.get("no2", None) if pollutants else None,
        "so2": pollutants.get("so2", None) if pollutants else None,
        "o3": pollutants.get("o3", None) if pollutants else None,
        "nh3": pollutants.get("nh3", None) if pollutants else None,
        "temperature": weather_data["temperature"],
        "humidity": weather_data["humidity"],
        "wind_speed": weather_data["wind_speed"],
        "precipitation": weather_data["precipitation"],
        "traffic_density": traffic_data,
        "industrial_latitude": latitude,
        "industrial_longitude": longitude,
        "diwali_date": festive_data["diwali_date"],
        "crop_burning_period": festive_data["crop_burning_season"],
        "season": festive_data["season"]
    }

    return all_data


# Save data to CSV
def save_to_csv(data, filename="delhi_aqi_data.csv"):
    df = pd.DataFrame([data])
    df.to_csv(filename, mode='a', header=False, index=False)
    print("Data saved to", filename)


# Main execution
if __name__ == "__main__":
    data = fetch_all_data()
    save_to_csv(data)
