import requests
import os
import pickle
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()
API_KEY = os.getenv('ACCUWEATHER_API_KEY')
CACHE_FILE = 'location_cache.pkl' 

def load_cache():
  try:
    with open(CACHE_FILE, 'rb') as f:
      return pickle.load(f)
  except FileNotFoundError:
    return {}

def save_cache(cache):
  with open(CACHE_FILE, 'wb') as f:
    pickle.dump(cache, f)

location_cache = load_cache()

@lru_cache(maxsize=None)  
def get_location_key_by_coordinates(lat, lon):
    cache_key = (lat, lon)
    if cache_key in location_cache:
      return location_cache[cache_key]

    url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
    params = {
        "apikey": API_KEY,
        "q": f"{lat},{lon}"
    }
    response = requests.get(url, params=params)
    if response.ok:
        data = response.json()
        result = data.get("Key")
        # Сохраняем результат в кэше (файл), чтобы сохранилось при перезапуске
        location_cache[cache_key] = result
        save_cache(location_cache)
        return result
    else:
        return {"error": True, "message": response.text, "code": response.status_code}

@lru_cache(maxsize=None) 
def get_location_key_by_city_name(location):
    if location in location_cache:
        return location_cache[location]

    url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
    params = {
        "apikey": API_KEY,
        "q": location,
        "language": "ru-ru"
    }
    response = requests.get(url, params=params)
    if response.ok:
        data = response.json()
        if len(data) == 0:
            return {"error": True, "message": f"Город '{location}' не найден"}
        result = data[0].get("Key")
        # Сохраняем результат в кэше (файл), чтобы сохранилось при перезапуске
        location_cache[location] = result
        save_cache(location_cache)
        return result
    else:
        return {"error": True, "message": response.text, "code": response.status_code}