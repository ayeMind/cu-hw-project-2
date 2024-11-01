from flask import render_template, request, redirect, url_for, Blueprint, session
from utils import get_location_key_by_city_name, get_weather, process_weather_data, get_mock_weather_cities

index_bp = Blueprint('index_bp', __name__, url_prefix='/')

@index_bp.route("/", methods=["GET", "POST"])
def index():
    error = request.args.get('error')
    return render_template("form.html", error=error)

@index_bp.route("/weather", methods=["GET", "POST"])
def weather():
    # city_from = request.form.get("city-from")
    # city_to = request.form.get("city-to")
    # cities_intermediate = request.form.getlist("city-intermediate")

    # if not city_from or not city_to:
    #     return redirect(url_for('index', error="Ошибка ввода города. Попробуйте еще раз."))

    # weather_cities = []
    # cities = [city_from] + cities_intermediate + [city_to]
    
    # for city in cities:
    #     location_data = get_location_key_by_city_name(city)
        
    #     if location_data.get("error"):
    #         index_bp.logger.error(location_data.get("message"))
    #         return redirect(url_for('index', error=location_data.get("message")))
        
    #     location_key = location_data.get("key")
    #     weather_data = get_weather(location_key)
        
    #     if isinstance(weather_data, dict) and weather_data.get("error"):
    #         return redirect(url_for('index', error="Не удалось получить данные о погоде. Попробуйте позже."))
        
    #     process_weather_data(weather_data, city)
    #     weather_cities.append(weather_data)
    
    weather_cities = get_mock_weather_cities()  
    number_of_days = int(request.form.get("amount"))
    weather_cities = [city_data[0:number_of_days] for city_data in weather_cities]
            
    session["weather_cities"] = weather_cities
        
    return render_template("weather.html", weather=weather_cities)