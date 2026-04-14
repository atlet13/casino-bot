import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8659665258:AAFyL7OZBZqkU-D7iaE2auHyf73KdYyeeIM"
WEBAPP = "https://casino-bot-1-p7mp.onrender.com"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(commands=["start"])
async def start(msg: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎰 Грати", web_app=WebAppInfo(url=WEBAPP))]
        ],
        resize_keyboard=True
    )
    await msg.answer("🎰 Відкрий гру", reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())