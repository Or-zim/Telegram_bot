from aiogram import Router, types
from aiogram.filters import Command
from database import add_users

router = Router()


@router.message(Command('start'))
async def start_hendler(message: types.Message):
    """хендлер для команды start"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    await add_users(user_id, username, first_name, last_name)
    await message.reply('Вас приветствует болванчик!')



