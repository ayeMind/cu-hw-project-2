from aiogram import Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

def for_start_keyboard():
    kb = [
        [
            KeyboardButton(text="/weather"),
            KeyboardButton(text="/help"),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите команду")
    return keyboard
router = Router() 

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(html.quote(message.from_user.full_name))}!\n\n"
        f"Это бот для получения прогноза погоды перед путешествием.\n"
        f"Погода будет отображаться в виде интерактивного графика и таблицы в браузере.\n\n"
        f"Возможные команды:\n"
        f"{html.bold('/weather')} - получить прогноз погоды\n"
        f"{html.bold('/help')} - посмотреть все команды\n"
        )
    await message.answer(
        "Выберите команду: ",
        reply_markup=for_start_keyboard()
    )
    
@router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(
        "Возможные команды:\n"
        f"{html.bold('/weather')} - получить прогноз погоды\n"
        f"{html.bold('/help')} - посмотреть все команды\n"
    )