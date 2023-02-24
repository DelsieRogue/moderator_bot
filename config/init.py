from aiogram import Bot, Dispatcher

from config import cnf

bot = Bot(token=cnf.TOKEN)
dp = Dispatcher(bot)
