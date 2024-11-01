from flask import render_template, request, redirect, url_for, Blueprint, session, jsonify
from utils import get_location_key_by_city_name, get_weather, process_weather_data, get_mock_weather_cities

USE_REAL_WEATHER = False

index_bp = Blueprint('index_bp', __name__, url_prefix='/')

@index_bp.route("/", methods=["GET", "POST"])
def index():
    error = request.args.get('error')
    return render_template("form.html", error=error)

@index_bp.route("/weather", methods=["GET", "POST"])
def weather():
    number_of_days = int(request.args.get("days") or request.form.get("amount") or 5)

    if USE_REAL_WEATHER == True:
        weather_cities = get_mock_weather_cities()
        weather_cities = [city_data[0:number_of_days] for city_data in weather_cities]
        session["weather_cities"] = weather_cities
        return render_template("weather.html", weather=weather_cities)

    if request.args.get("from"): # Запрос от Telegram бота
        city_from = request.args.get("from")
        city_to = request.args.get("to")
        cities = [city_from, city_to]
    else: # Запрос от веб-формы
        city_from = request.form.get("city-from")
        city_to = request.form.get("city-to")
        cities_intermediate = request.form.getlist("city-intermediate")
        cities = [city_from] + cities_intermediate + [city_to]

    if not city_from or not city_to:
        if request.args.get("from"):
            return jsonify({'error': "Ошибка ввода города. Попробуйте еще раз."}), 400
        else:
            return redirect(url_for('index', error="Ошибка ввода города. Попробуйте еще раз."))

    weather_cities = []
    for city in cities:
        location_data = get_location_key_by_city_name(city)

        if location_data.get("error"):
            if request.args.get("from"):
                return jsonify({'error': location_data.get("message")}), 400
            else:
                index_bp.logger.error(location_data.get("message"))
                return redirect(url_for('index', error=location_data.get("message")))

        location_key = location_data.get("key")
        weather_data = get_weather(location_key)

        if isinstance(weather_data, dict) and weather_data.get("error"):
            if request.args.get("from"):
                return jsonify({'error': "Не удалось получить данные о погоде. Попробуйте позже."}), 500
            else:
                return redirect(url_for('index', error="Не удалось получить данные о погоде. Попробуйте позже."))

        process_weather_data(weather_data, city)
        weather_cities.append(weather_data)

    weather_cities = [city_data[0:number_of_days] for city_data in weather_cities]
    session["weather_cities"] = weather_cities

    return render_template("weather.html", weather=weather_cities)