import requests


# Milak, Rampur, Uttar Pradesh
LATITUDE = 28.6129
LONGITUDE = 79.1681

LOCATION = "Milak, Rampur, Uttar Pradesh"

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "precipitation,"
            "weather_code,"
            "cloud_cover,"
            "wind_speed_10m"
        ),

        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "timezone": "Asia/Kolkata",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        current = data["current"]

        return {
            "temperature": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"],
            "precipitation": current["precipitation"],
            "weather_code": current["weather_code"],
            "cloud_cover": current["cloud_cover"],
            "wind_speed": current["wind_speed_10m"],
        }

    except requests.RequestException as e:
        print("Weather API Error:", e)
        return None

    except Exception as e:
        print("Weather Error:", e)
        return None

def weather_description(code):
     weather_codes = {
        0: "clear sky",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "foggy",
        48: "depositing rime fog",
        51: "light drizzle",
        53: "moderate drizzle",
        55: "dense drizzle",
        61: "slight rain",
        63: "moderate rain",
        65: "heavy rain",
        71: "slight snow",
        73: "moderate snow",
        75: "heavy snow",
        80: "slight rain showers",
        81: "moderate rain showers",
        82: "violent rain showers",
        95: "thunderstorm",
        96: "thunderstorm with slight hail",
        99: "thunderstorm with heavy hail",
    }
     
     return weather_codes.get(code, "unknown weather")

def get_weather_text():
    weather = get_weather()

    if weather is None:
        return "Sorry sir, I couldn't get the current weather."

    description = weather_description(weather["weather_code"])

    return (
        f"In {LOCATION}, the temperature is "
        f"{weather['temperature']} degrees Celsius, "
        f"feels like {weather['feels_like']} degrees, "
        f"with {description}. "
        f"Humidity is {weather['humidity']} percent "
        f"and wind speed is {weather['wind_speed']} kilometers per hour."
    )