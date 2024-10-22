def classify_weather(weather_data):
    if not weather_data:
        return None
    
    temperature = weather_data["temperature"] # в градусах цельсия
    humidity = weather_data["humidity"] # в процентах
    wind_speed = weather_data["wind_speed"] # в км/ч
    precipitation = weather_data["precipitation"] # в миллиметрах
    cloud_cover = weather_data["cloud_cover"] # в процентах
    pressure = weather_data["pressure"] # в миллибарах
    
    score = 0 # Оценка погоды, чем меньше, тем лучше

    # Влияние температуры
    if temperature > 25:
        score += (temperature - 25) * 2 # Для жары каждый градус играет более важную роль, чем для холода
    elif temperature < 15:
        score += (15 - temperature) // 2
        
    # Влияние влажности
    humidity_score = 0
    if temperature <= 0: # При низкой температуре предпочтительная влажность 30-40
        if humidity < 30:
            humidity_score += (30 - humidity) // 4
        elif humidity > 40:
            humidity_score += (humidity - 40) // 4
    
    elif temperature > 20: # При высокой температуре предпочтительная влажность 50-60
        if humidity < 50:
            humidity_score += (50 - humidity) // 4
        elif humidity > 60:
            humidity_score += (humidity - 60) // 4
            
    else: # Что-то между
        if humidity < 40:
            humidity_score += (40 - humidity) // 4
        elif humidity > 50:
            humidity_score += (humidity - 50) // 4
    
    if humidity_score > score: # больше очков, чем за температуру
        score += max(score, humidity_score // 2)
    else:
        score += humidity_score
        
            
    # Влияние скорости ветра
    if wind_speed >= 20: # Начиная с умеренного ветра по шкале Бофорта
        score += (wind_speed - 20) // 3
    elif wind_speed > 10: 
        score += 1
    
    # Влияние осадков
    if precipitation >= 5:
        score += 5 + (precipitation - 5) // 2
    elif precipitation > 0.2: 
        score += 2
        
    # Влияние облачности
    if cloud_cover > 50:
        score += (cloud_cover - 50) // 10 
   
    # Влияние атмосферного давления
    if abs(pressure - 1013) > 15: 
        score += (abs(pressure - 1013) - 15) * 2 
    
    # print("SCORE", score)
            
    # Результат
    if score < 5:
        return "Прекрасная погода"
    elif score < 10:
        return "Хорошая погода"
    elif score < 15:
        return "Нормальная погода"
    elif score < 20:
        return "Плохая погода"
    else:
        return "Отвратительная погода"

# Примеры для проверки работы модели
# import json
# with open('tests.json', 'r') as f:
#     tests = json.load(f)
#     for test in tests:
#         print(test, classify_weather(test))