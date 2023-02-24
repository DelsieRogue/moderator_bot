from aiogram import types
from aiogram.dispatcher import filters

from config.init import dp
from filters.handler_filter import CleaningChatFilter


@dp.message_handler(CleaningChatFilter(), filters.ChatTypeFilter(types.ChatType.SUPERGROUP), content_types=['any'])
async def cleaning_chat(message: types.Message):
    await message.delete()
