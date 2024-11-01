import urllib
from aiogram import Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import requests
from os import getenv

router = Router()

class WeatherForm(StatesGroup):
    start_point = State()
    end_point = State()

forecast_interval_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Прогноз на 3 дня", callback_data="3_days")],
        [InlineKeyboardButton(text="Прогноз на 4 дня", callback_data="4_days")],
        [InlineKeyboardButton(text="Прогноз на 5 дней", callback_data="5_days")]
    ]
)

location_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отправить геолокацию", request_location=True)]], resize_keyboard=True, one_time_keyboard=True)

def check_city_in_accuweather(city):
    # Если не получилось превратить в JSON, то API обработало данные, т.е. город нашло
    try:
        requests.get(f"http://localhost:5000/weather?from={city}&to={city}&days={5}").json()
        return False
    except:
        return True

@router.message(Command("weather"))
async def cmd_weather(message: Message, state: FSMContext):
    await message.answer("Введите начальную точку маршрута или отправьте свою геолокацию:", reply_markup=location_kb)
    await state.set_state(WeatherForm.start_point)

def reverse_geocode(lat, lon):
    ACCUWEATHER_API_KEY = getenv('ACCUWEATHER_API_KEY')

    url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={ACCUWEATHER_API_KEY}&q={lat},{lon}&language=ru-ru"
    response = requests.get(url).json()
    if response['Key']:
        return response['LocalizedName']
    else:
        return None

@router.message(WeatherForm.start_point)
async def process_location(message: Message, state: FSMContext):
    location = message.location
    if location:
        city_name = reverse_geocode(location.latitude, location.longitude) 
    else:
        city_name = message.text

    if city_name:
        await state.update_data(start_point=city_name)
        await message.answer(f"Вы выбрали район {city_name}. Введите конечную точку маршрута:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(WeatherForm.end_point)
    else:
        await message.answer("Не удалось определить район по геолокации. Введите название города вручную:")


@router.message(WeatherForm.start_point)
async def process_start_point(message: Message, state: FSMContext):
    if not check_city_in_accuweather(message.text):
        await message.answer("Город не найден")
        return
    
    await state.update_data(start_point=message.text)
    await message.answer(f"Вы выбрали город {message.text}. Введите конечную точку маршрута:")
    await state.set_state(WeatherForm.end_point)

@router.message(WeatherForm.end_point)
async def process_end_point(message: Message, state: FSMContext):
    if not check_city_in_accuweather(message.text):
        await message.answer("Город не найден")
        return
    await state.update_data(end_point=message.text)
    await message.answer(f"Вы выбрали город {message.text}. Выберите временной интервал прогноза:", reply_markup=forecast_interval_kb)


@router.callback_query(lambda c: c.data in ["3_days", "4_days", "5_days"])
async def process_forecast_interval(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    start_point = user_data['start_point']
    end_point = user_data['end_point']
    days = int(callback_query.data.split('_')[0])

    # Кодируем параметры URL для корректной обработки пробелов и спецсимволов
    start_point_encoded = urllib.parse.quote(start_point)
    end_point_encoded = urllib.parse.quote(end_point)

    url = f"http://localhost:5000/weather?from={start_point_encoded}&to={end_point_encoded}&days={days}"
    
    await callback_query.message.edit_text(f"Прогноз погоды на {days} дней:\n\n{url}", reply_markup=None) 
    await state.clear()
    await callback_query.answer()