import aiogram
import aiosqlite
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from database import create_tables
from handlers import admin, users, farm_coins, balance, duel
from handlers.filters import ChatFilter

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token="7855524669:AAF5rFikKaFwfvhT0Q3_6fOm7WLiP1Y571Q")
    dp = Dispatcher()
    dp.include_router(users.router)
    dp.include_router(admin.router)
    dp.include_router(farm_coins.router)
    dp.include_router(balance.router)
    dp.include_router(duel.router)
    await create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
