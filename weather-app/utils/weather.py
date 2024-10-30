import requests
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()
API_KEY = os.getenv('ACCUWEATHER_API_KEY')
    
def parse_five_days_weather(weather_data):
    """
    Принимает прогноз погоды из API и возвращает список из словарей с погодой на 5 дней
    (температура, относительная влажность, вероятность осадков, скорость ветра, реальное ощущение температуры, облачность)
    возращая среднее между минимумом и максимумом для каждого параметра
    """
    if not weather_data:
        return None
    
    def get_mean(param):
        return (param["Minimum"]["Value"] + param["Maximum"]["Value"]) / 2
    
    def get_delta_days(param):
        current_date = date.today()
        date_string = param["Date"][:10]
        param_date = date.fromisoformat(date_string)
        delta_days = (current_date - param_date).days
        return abs(delta_days)
    
    def get_delta_days_text(delta_days):
        if delta_days == 0:
            return "Сегодня"
        elif delta_days == 1:
            return "Завтра"
        elif delta_days == 2:
            return "Послезавтра"
        elif delta_days == 3 or delta_days == 4:
            return f"Через {delta_days} дня"
        else:
            return f"Через {delta_days} дней"
    
    result_list = []
    for day in weather_data["DailyForecasts"]:
        temperature = get_mean(day["Temperature"])
        real_temperature = get_mean(day["RealFeelTemperature"])
        relative_humidity = day["Day"]["RelativeHumidity"]["Average"]
        precipation_probability = day["Day"].get("PrecipitationProbability")
        wind_speed = day["Day"]["Wind"]["Speed"]["Value"]
        cloud_cover = day["Day"].get("CloudCover")
        
        result = {
            "delta_days": get_delta_days_text(get_delta_days(day)),
            "temperature": temperature,
            "real_temperature": real_temperature,
            "humidity": relative_humidity,
            "precipitation": precipation_probability,
            "wind_speed": wind_speed,
            "cloud_cover": cloud_cover
        }
        
        result_list.append(result)
        
    return result_list
            
def get_five_days_weather(location_key):
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}"
    params = {"apikey": API_KEY, "details": "true", "metric": "true"}
    response = requests.get(url, params=params)
    if response.ok:
        weather_data = response.json()
        return parse_five_days_weather(weather_data)
    else:
        return {"error": True, "message": response.text, "code": response.status_code}

