# Проект 2. Веб-сервис по предсказанию неблагоприятных погодных условий для путешественников

### Настройка API ключа

1. Зарегистрируйтесь на [AccuWeather API](https://developer.accuweather.com/) и получите API ключ.
2. Создайте файл `.env` в корне проекта (или переименуйте файл `.env.example`).
3. Добавьте в файл `.env` следующую строку:

```
ACCUWEATHER_API_KEY=ваш_ключ
```

### Небольшой дисклеймер

В форме нужно вводить названия городов именно на русском языке, так как API одновременно может работать только с одним языком.

(AccuWeather слишком жадные, 3 запроса для получения погоды в одном городе это перебор, так что оставил только русский)

### Локальный запуск

1. Создайте виртуальное окружение `python3 -m venv .venv`
2. Войдите в окружение `source .venv/bin/activate` (Linux) или `.\venv\Scripts\activate.bat` (Windows)
3. Установите зависимости `pip install -r requirements.txt`
4. Запустите проект `python3 weather-app/app.py`
5. Откройте в браузере `http://localhost:5000`

### Модель

Оценка производится на основе следующих параметров:

* **Температура** 
* **Влажность** 
* **Скорость ветра** 
* **Количество осадков** 
* **Облачность** 
* **Атмосферное давление** 

И может возвращать следующие значения:

* **Прекрасная погода** 
* **Хорошая погода** 
* **Нормальная погода**
* **Плохая погода**
* **Отвратительная погода** 

Более подробно ознакомиться с моделью можно в файле `utils/model.py`.
