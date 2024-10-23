import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('ACCUWEATHER_API_KEY')

def parse_weather_data(weather_data):
    """
    Принимает прогноз погоды из API и возвращает словарь с основными параметрами погоды
    (температура, влажность, ветер, осадки, облачность, атмосферное давление)
    """
    if not weather_data:
        return None
    
    weather_data = weather_data[0]
    
    temperature = float(weather_data["Temperature"]["Metric"]["Value"]) # в градусах цельсия
    humidity = int(weather_data["RelativeHumidity"]) # в процентах
    wind_speed = float(weather_data["Wind"]["Speed"]["Metric"]["Value"]) # в км/ч
    precipitation = float(weather_data["PrecipitationSummary"]["Precipitation"]["Metric"]["Value"]) # в миллиметрах
    cloud_cover = int(weather_data["CloudCover"]) # в процентах
    pressure = int(weather_data["Pressure"]["Metric"]["Value"]) # в миллибарах
    
    return {
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "precipitation": precipitation,
        "cloud_cover": cloud_cover,
        "pressure": pressure
    }
    
def get_weather(location_key):
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
    params = {"apikey": API_KEY, "details": "true"}
    response = requests.get(url, params=params)
    if response.ok:
        weather_data = response.json()
        return parse_weather_data(weather_data)
    else:
        return {"error": True, "message": response.text, "code": response.status_code}


