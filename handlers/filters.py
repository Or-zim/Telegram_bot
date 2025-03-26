from aiogram.filters import Filter
from aiogram import types



class ChatFilter(Filter):
    """фильтр который проверяет на соответсвие с id чата"""
    def __init__(self, chat_id):
        self.chat_id = chat_id
    
    async def __call__(self, message: types.Message):
        return self.chat_id == message.chat.id