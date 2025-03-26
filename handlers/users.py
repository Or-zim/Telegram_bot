from aiogram import Router, types
from aiogram.filters import Command
from database import add_users

router = Router()

CHAT_ID = -4759195662 #id chat

@router.message(Command('start'))
async def start_hendler(message: types.Message):
    """хендлер для команды start"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    await add_users(user_id, username, first_name, last_name)
    
    if message.chat.id == CHAT_ID:
        text_buttun = "Играть"
    else:
        text_buttun = 'Фарм FKcoin'
    
    
    kb = [
        [
            types.KeyboardButton(text="Баланс"),
            types.KeyboardButton(text=text_buttun)
        ],
    ]
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Здавова вох"
    )
    await message.answer('Вас приветствует болванчик!', reply_markup=keyboard)




