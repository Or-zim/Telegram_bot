from aiogram import Router, types
import json
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers.filters import ChatFilter
from aiogram.fsm.context import FSMContext
from aiogram import F
import asyncio
import re
from database import add_user_coins, del_user_coins, get_username
import random
from aiogram.fsm.state import State, StatesGroup
from database import get_user_coin, get_username
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

CHAT_ID = -4759195662


def coin_flip() -> str:
    """Случайным образом возвращает "орел" или "решка"."""
    return random.choice(["орел", "решка"])






def create_side_keyboard():
    """создает клавиатуру для выбора стороны"""
    button = [
        [KeyboardButton(text='Орел')],
        [KeyboardButton(text='Решка')]
    ]
    return ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True, one_time_keyboard=True)

@router.message(ChatFilter(chat_id=CHAT_ID), Command('play'))
async def duel_func(message: types.Message):
    try:
        match = re.match(r'/play\s+(\w+)\s+(\d+)', message.text, re.IGNORECASE)

        if not match:
            await message.reply("Неверный формат команды. Используйте: /play [орел, решка] [сумма]")
            return
        
        user_id = message.from_user.id #id того кто создает дуэль
        ui = user_id # копия 
        balance = await get_user_coin(user_id) # баланс создателя дуэли
        username = await get_username(user_id)# тег создателя дуэли
        a1 = match.group(1)# присваивает орел или решка из соо 
        a2 = int(match.group(2))# присваивает ставку
        list_side = ['орел', 'решка']
        
        if a1.lower() not in ['орел', 'решка']:
            await message.reply("Орел или решка напиши идиот!")
            return
        
        if a2 <= 0:
            await message.reply("Ты че совсем тупой?")
            return
        
        if a2 > balance[0]:
            await message.reply("У тя денег столько нету лох")
            return
        
        if a1.lower() == list_side[0]:
            opponent_side = list_side[1]
        else:
            opponent_side = list_side[0]
        
        callback_data = {'a1': a1, 'a2': a2, 'id': ui}# образуется словарь который передасться в play_callback размер которого не привышает 64 байта
        callback_data_json = json.dumps(callback_data)
        builder = InlineKeyboardBuilder()
        builder.button(text=f"Принять дуэль от игрока {username[0]}, за {opponent_side} на сумму {a2}", callback_data=callback_data_json)
        await message.reply(f"Дуэль", reply_markup=builder.as_markup())

    except (ValueError, IndexError):
        await message.reply("Неверный формат команды. Используйте: /play [орел, решка] [сумма]")

@router.callback_query()
async def play_callback(callback: types.CallbackQuery):
    """после нажатия на кнопку принятия дуэли срабатывает этот хендлер
    все фуункции из бд передают словарь со значением"""
    try:
        callback_data = json.loads(callback.data)# загружаем словарь с переданными данными из duel_func
        arg1 = callback_data['a1']# орел или решка
        arg2 = callback_data['a2']# ставка
        opponent_id = callback.from_user.id #нажавший на кнопку 
        user_id = callback_data['id'] # id кто создал дуэль
        username = await get_username(user_id) # тег того кто создал дуэль
        oppo_name = await get_username(opponent_id)# тег того кто принял дуэль
        balance_oppo = await get_user_coin(opponent_id)#баланс того кто принял дуэль 
        
        if balance_oppo[0] >= arg2:
            win_pos = coin_flip()
            if win_pos == arg1.lower():
                try:
                    await add_user_coins(user_id, arg2)
                    await del_user_coins(opponent_id, arg2)
                    await callback.answer(f"победа игрока {username[0]}", show_alert=True)
                    await callback.message.edit_text(f"1Игрок {username[0]} выйграл. Результат {win_pos}")
                except Exception as e:
                    print(f"Ошибка при обновлении баланса: {e}")

            if win_pos != arg1.lower():
                try:
                    await add_user_coins(opponent_id, arg2)
                    await del_user_coins(user_id, arg2)
                    await callback.answer(f"победа игрока {oppo_name[0]}", show_alert=True)
                    await callback.message.edit_text(f"2Игрок {oppo_name[0]} выйграл. Результат {win_pos}")
                except Exception as e:
                    print(f"Ошибка при обновлении баланса: {e}")
                    
        else:
            await callback.answer("у тя нету столько денег на ставку", show_alert=True)

    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


