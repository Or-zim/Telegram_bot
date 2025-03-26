from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from aiogram import F
from database import get_user_coin 
router = Router()


@router.message(F.text.lower() == "баланс")
async def get_balance(message: types.Message):
    user_id = message.from_user.id
    balance = await get_user_coin(user_id)
    try:
        await message.reply(f"Твой баланс: {balance[0]}")
    except:
        await message.reply("Я сломался(")