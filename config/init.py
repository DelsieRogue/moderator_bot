from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import cnf

storage = MemoryStorage()
bot = Bot(token=cnf.TOKEN)
dp = Dispatcher(bot, storage=storage)
