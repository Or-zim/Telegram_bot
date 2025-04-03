from aiogram import Router, types
from aiogram.filters import Command
from database import add_users

router = Router()
import os
from dotenv import load_dotenv
load_dotenv()
CHAT_ID = os.environ.get("GROUP_ID") #id chat group




@router.message(Command('start'))
async def start_hendler(message: types.Message):
    """хендлер для команды start"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    await add_users(user_id, username, first_name, last_name)
    
    if message.chat.id == CHAT_ID:
            kb = [
        [
            types.KeyboardButton(text="Баланс")
            
        ]
        ]
            text_new_user = "Вас приветсвуте игровой бот Болванчик, это простой симулятор игры в 'Орел или Решка', здесь нету никакой подкрутки) и победа реально зависит от вашей удачи. Начать игру очень просто, для этого пропиши команду /play 'орел/решка' 'сумма ставки', и ожидай когда найдется тот, кто также желает испыть свою удачу! Чтобы отменить дуэль нужно сыграть самому с собой."

    else:
            kb = [
        [
            types.KeyboardButton(text="Баланс"),
            types.KeyboardButton(text='Фарм FKcoin')
        ]
        ]
            text_new_user = f"""
            Вас приветсвуте игровой бот Болванчик, это простой симулятор игры в 'Орел или Решка', здесь нету никакой подкрутки) и победа реально зависит от вашей удачи. Чтобы заработать первые Freak coins нужно очень много кликать по кнопке в чате, если тебя это не устраиват, то ты можешь сыграть в общем чате и удвоить свой баланс! Вот ссылка на чат https://t.me/+XR4tWuBczghhY2Ey"""

    

    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Здавова вох"
    )
    await message.answer(text=text_new_user, reply_markup=keyboard)




