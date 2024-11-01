from os import getenv
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


TOKEN = getenv("TG_BOT_TOKEN")

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}!\n\n"
        f"Это бот для получения прогноза погоды перед путешествием.\n"
        f"Погода будет отображаться в виде интерактивного графика и таблицы в браузере.\n\n"
        f"Возможные команды:\n"
        f"{html.bold('/weather')} - получить прогноз погоды\n"
        f"{html.bold('/help')} - вы сейчас здесь\n"
        )
    
@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(
        f"Возможные команды:\n\n"
        f"{html.bold('/weather')} - получить прогноз погоды\n"
        f"{html.bold('/help')} - вы сейчас здесь\n"
    )
    
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())