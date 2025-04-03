from aiogram import Router, types, F
from aiogram.filters import Command
from database import get_all_users_ad
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from time import sleep
import os
from dotenv import load_dotenv
load_dotenv()
ADMIN_ID = os.environ.get("ADMIN_ID")

router = Router()


class BroadState(StatesGroup):
    """состояние текста рассылки"""
    text = State()

@router.message(Command('broadcast'), F.from_user.id == ADMIN_ID)
async def broadcast_fun(message: types.Message, state: FSMContext):
    """ хендлер на рассылку соо"""
    
    await message.reply('Отправте текст рассылки')
    await state.set_state(BroadState.text)
    

@router.message(BroadState.text, F.from_user.id == ADMIN_ID)
async def process_broad(message: types.Message, bot, state: FSMContext):
    """Обработчик текста рассылки"""
    text = message.text
    users_ids = await get_all_users_ad()
    success_count = 0
    fail_count = 0
    for user_id in users_ids:
        try:
            await bot.send_message(user_id[0], text)
            await sleep(0.3)
            success_count += 1 
        except Exception as e:
            fail_count += 1
            
    await message.reply(f"Рассылка завершена.\nУспешно отправлено: {success_count}\nНе удалось отправить: {fail_count}")
    await state.clear()



@router.message(Command('us_count'), F.from_user.id == ADMIN_ID)
async def user_count(message: types.Message):
    us_count = await get_all_users_ad()
    await message.reply(f"Количество пользователей равно: {str(len(us_count))}")

@router.message(Command("chatid"))
async def chat_id_handler(message: types.Message):
    """Отправляет ID чата."""
    chat_id = message.chat.id
    await message.answer(f"ID этого чата: {chat_id}")

