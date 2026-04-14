import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

TOKEN = "8659665258:AAFyL7OZBZqkU-D7iaE2auHyf73KdYyeeIM"
WEBAPP = "https://casino-bot-1-p7mp.onrender.com"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(msg: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="🎰 Грати",
                web_app=WebAppInfo(url=WEBAPP)
            )]
        ],
        resize_keyboard=True
    )
    await msg.answer("🎰 Відкрий гру", reply_markup=kb)

async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())