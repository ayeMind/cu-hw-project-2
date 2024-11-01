import requests
import os
from dotenv import load_dotenv
from datetime import date
from .model import classify_weather

load_dotenv()
API_KEY = os.getenv('ACCUWEATHER_API_KEY')

def parse_five_days_weather(weather_data):
    """
    Принимает прогноз погоды из API и возвращает список из словарей с погодой на 5 дней.
    Возвращает среднее значение между минимумом и максимумом для каждого параметра.
    """
    if not weather_data:
        return None

    result_list = []
    for day in weather_data["DailyForecasts"]:
        result = {
            "date": format_date(day),
            "temperature": calculate_mean(day["Temperature"]),
            "humidity": day["Day"]["RelativeHumidity"]["Average"],
            "precipitation": calculate_precipitation(day),
            "wind_speed": day["Day"]["Wind"]["Speed"]["Value"],
            "cloud_cover": day["Day"].get("CloudCover")
        }
        result_list.append(result)

    return result_list

def calculate_mean(param):
    """Возвращает среднее значение между минимумом и максимумом."""
    return (param["Minimum"]["Value"] + param["Maximum"]["Value"]) / 2

def calculate_precipitation(day):
    """Возвращает общее количество осадков в миллиметрах."""
    snow = day["Day"].get("Snow", {}).get("Value", 0) * 10  # Конвертация см в мм
    rain = day["Day"].get("Rain", {}).get("Value", 0)
    ice = day["Day"].get("Ice", {}).get("Value", 0)
    return snow + rain + ice

def format_date(day):
    """Форматирует дату для отображения."""
    current_date = date.today()
    param_date = date.fromisoformat(day["Date"][:10])
    delta_days = abs((current_date - param_date).days)
    
    if delta_days == 0:
        return "Сегодня"
    elif delta_days == 1:
        return "Завтра"
    elif delta_days == 2:
        return "Послезавтра"
    elif delta_days in [3, 4]:
        return f"Через {delta_days} дня"
    else:
        return f"Через {delta_days} дней"

def get_weather(location_key):
    """
    Получает прогноз погоды на 5 дней по местоположению из API.
    """
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}"
    params = {"apikey": API_KEY, "details": "true", "metric": "true"}
    
    response = requests.get(url, params=params)
    
    if response.ok:
        weather_data = response.json()
        return parse_five_days_weather(weather_data)
    
    return {"error": True, "message": response.text, "code": response.status_code}

def process_weather_data(weather_data, city: str):
    """
    Добавляет название города и результат модели к данным о погоде
    """
    for weather_day in weather_data:
        result_of_model = classify_weather(weather_day)
        
        if not result_of_model:
            raise ValueError("Не удалось определить погоду. Попробуйте еще раз.")
        
        weather_day["result_of_model"] = result_of_model
        weather_day["city"] = city