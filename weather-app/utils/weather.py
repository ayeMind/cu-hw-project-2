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
    возращая среднее между минимумом и максимумом для каждого параметра (если дается именно так)
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
        
        def get_precipation(name):
            if name == "Snow":
                return day["Day"]["Snow"]["Value"] * 10 # Дается в API в см, пока все остальное - в мм
            return day["Day"][name]["Value"]
        
        temperature = get_mean(day["Temperature"])
        relative_humidity = day["Day"]["RelativeHumidity"]["Average"]
        precipation_mm = get_precipation("Snow") + get_precipation("Rain") + get_precipation("Ice")
        wind_speed = day["Day"]["Wind"]["Speed"]["Value"]
        cloud_cover = day["Day"].get("CloudCover")
                
        result = {
            "delta_days": get_delta_days_text(get_delta_days(day)),
            "temperature": temperature,
            "humidity": relative_humidity,
            "precipitation": precipation_mm,
            "wind_speed": wind_speed,
            "cloud_cover": cloud_cover
        }
        
        result_list.append(result)
        
    return result_list
            
def get_weather(location_key):
    """
    Получет прогноз погоды на 5 дней по местоположению из API
    """
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}"
    params = {"apikey": API_KEY, "details": "true", "metric": "true"}
    response = requests.get(url, params=params)
    if response.ok:
        weather_data = response.json()
        return parse_five_days_weather(weather_data)
    else:
        return {"error": True, "message": response.text, "code": response.status_code}

