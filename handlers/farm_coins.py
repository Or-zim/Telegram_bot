from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from database import add_user_coins, get_user_coin

router = Router()

last_click = {}
CLICK_COOLDOWN = 1


@router.message(Command("farmcoin"))
async def farm_coins(message: types.Message):
    user_id = message.from_user.id

    builder = InlineKeyboardBuilder()
    builder.button(text='Фармим FKcoin', callback_data="click_button")

    await message.reply("Опять ты в дерьме, вонючка", reply_markup=builder.as_markup())

@router.callback_query(lambda c: c.data == "click_button")
async def click_button_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    now = asyncio.get_event_loop().time()
    
    if user_id in last_click and now - last_click[user_id] < CLICK_COOLDOWN:
        await callback.answer()
        return
    
    await add_user_coins(user_id, 1)
    last_click[user_id] = now
    
    await callback.answer("Сюда + 1FK")
     
    builder = InlineKeyboardBuilder()
    builder.button(text='Фармим FKcoin', callback_data="click_button")
    await callback.message.edit_text(text="так дело не пойдет, свего + 1FK", reply_markup=builder.as_markup())