import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import Command

API_TOKEN = "ТУТ_ТВІЙ_ТОКЕН"
WEBAPP_URL = "https://тут-буде-render-url"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎮 Грати", web_app=WebAppInfo(url=WEBAPP_URL))]
        ],
        resize_keyboard=True
    )

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer("🎰 Казино", reply_markup=get_keyboard())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())