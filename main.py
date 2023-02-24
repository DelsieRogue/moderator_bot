from aiogram.utils import executor

from config.init import dp
from filters.handler_filter import on_startup
from handlers import main_menu
from handlers.chat_cleaning import chat_cleaning
from handlers.getters_user import getters_users

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
