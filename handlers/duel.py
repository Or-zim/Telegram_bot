from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers.filters import ChatFilter
from aiogram import F
import asyncio

router = Router()

CHAT_ID = -4759195662

@router.message(ChatFilter(chat_id=CHAT_ID), F.text.lower() == "играть")
async def test(message: types.Message):
    await message.reply("Вы в чате!!!!")