# Требуется только для тестирования

def get_mock_weather_cities():
    """
    Возвращает пример данных о погоде для 5-ти городов после преобразования
    """
    return [
    [
        {
            "date": "Сегодня",
            "city": "Москва",
            "temperature": 10,
            "humidity": 50,
            "precipitation": 0,
            "wind_speed": 10,
            "cloud_cover": 20,
            "result": "Прекрасная"
        },
        {
            "date": "Завтра",
            "city": "Москва",
            "temperature": 12,
            "humidity": 55,
            "precipitation": 5,
            "wind_speed": 12,
            "cloud_cover": 30,
            "result": "Хорошая"
        },
        {
            "date": "Послезавтра",
            "city": "Москва",
            "temperature": 15,
            "humidity": 60,
            "precipitation": 0,
            "wind_speed": 8,
            "cloud_cover": 15,
            "result": "Нормальная"
        },
        {
            "date": "Через 3 дня",
            "city": "Москва",
            "temperature": 13,
            "humidity": 65,
            "precipitation": 10,
            "wind_speed": 15,
            "cloud_cover": 40,
            "result": "Плохая"
        },
        {
            "date": "Через 4 дня",
            "city": "Москва",
            "temperature": 11,
            "humidity": 70,
            "precipitation": 0,
            "wind_speed": 10,
            "cloud_cover": 25,
            "result": "Отвратительная"
        }
    ],
    [
        {
            "date": "Сегодня",
            "city": "Санкт-Петербург",
            "temperature": 8,
            "humidity": 70,
            "precipitation": 20,
            "wind_speed": 15,
            "cloud_cover": 60,
            "result": "Прекрасная"
        },
        {
            "date": "Завтра",
            "city": "Санкт-Петербург",
            "temperature": 9,
            "humidity": 75,
            "precipitation": 10,
            "wind_speed": 12,
            "cloud_cover": 50,
            "result": "Хорошая"
        },
        {
            "date": "Послезавтра",
            "city": "Санкт-Петербург",
            "temperature": 10,
            "humidity": 80,
            "precipitation": 5,
            "wind_speed": 10,
            "cloud_cover": 40,
            "result": "Нормальная"
        },
        {
            "date": "Через 3 дня",
            "city": "Санкт-Петербург",
            "temperature": 11,
            "humidity": 85,
            "precipitation": 0,
            "wind_speed": 8,
            "cloud_cover": 30,
            "result": "Плохая"
        },
        {
            "date": "Через 4 дня",
            "city": "Санкт-Петербург",
            "temperature": 12,
            "humidity": 90,
            "precipitation": 15,
            "wind_speed": 10,
            "cloud_cover": 50, 
            "result": "Отвратительная"
        }
    ],
    [
        {
            "date": "Сегодня",
            "city": "Новосибирск",
            "temperature": -5,
            "humidity": 30,
            "precipitation": 0,
            "wind_speed": 5,
            "cloud_cover": 10,
            "result": "Прекрасная"
        },
        {
            "date": "Завтра",
            "city": "Новосибирск",
            "temperature": -3,
            "humidity": 35,
            "precipitation": 2,
            "wind_speed": 7,
            "cloud_cover": 15,
            "result": "Хорошая"
        },
        {
            "date": "Послезавтра",
            "city": "Новосибирск",
            "temperature": -1,
            "humidity": 40,
            "precipitation": 0,
            "wind_speed": 10,
            "cloud_cover": 20,
            "result": "Нормальная"
        },
        {
            "date": "Через 3 дня",
            "city": "Новосибирск",
            "temperature": 0,
            "humidity": 45,
            "precipitation": 5,
            "wind_speed": 12,
            "cloud_cover": 25,
            "result": "Плохая"
        },
        {
            "date": "Через 4 дня",
            "city": "Новосибирск",
            "temperature": 2,
            "humidity": 50,
            "precipitation": 0,
            "wind_speed": 8,
            "cloud_cover": 15,
            "result": "Отвратительная"
        }
    ]
]