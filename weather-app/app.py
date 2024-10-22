from flask import Flask, render_template, request
from utils.weather import get_weather
from utils.location import get_location_key_by_city_name
from utils.model import classify_weather
import logging

app = Flask(__name__)

class DualHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        print(self.format(record))

handler = DualHandler()
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO) 

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    error = request.args.get('error')
    return render_template("form.html", error=error)

@app.route("/weather", methods=["GET", "POST"])
def weather():
    city_from = request.form.get("city-from")
    city_to = request.form.get("city-to")

    if not city_from or not city_to:
        return redirect(url_for('index', error="Ошибка ввода города. Попробуйте еще раз."))

    weather_cities = []
    for city in [city_from, city_to]:
        location_key = get_location_key_by_city_name(city)
        if isinstance(location_key, dict) and location_key.get("error", False):
            app.logger.error(location_key.get("message"))
            return redirect(url_for('index', error=location_key.get("message")))

        weather_data = get_weather(location_key)
        if isinstance(weather_data, dict) and weather_data.get("error", False):
            return redirect(url_for('index', error="Не удалось получить данные о погоде. Попробуйте позже."))

        result_of_model = classify_weather(weather_data)
        if not result_of_model:
            return redirect(url_for('index', error=result_of_model))

        weather_data["result"] = result_of_model
        weather_data["city"] = city
        weather_cities.append(weather_data)

    weather_dict = {
        "weather_from": weather_cities[0],
        "weather_to": weather_cities[1],
    }

    return render_template("weather.html", weather=weather_dict)

if __name__ == "__main__":
    app.run(debug=True)