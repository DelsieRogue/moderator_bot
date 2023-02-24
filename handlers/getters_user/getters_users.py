from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from common.common import ROLE, get_buttons_for_role
from config.init import dp, bot
from data_base.scripts import get_users_from_db
from filters.handler_filter import SuperAdminFilter, AdminFilter, SuperAdminAndAdminFilter


@dp.message_handler(SuperAdminFilter(), filters.ChatTypeFilter(types.ChatType.PRIVATE),
                    Text("Получение списков"))
async def get_user_list_for_super_admin(message: types.Message):
    await bot.send_message(message.from_user.id, text="Команды",
                           reply_markup=super_admins_buttons)


@dp.message_handler(AdminFilter(), filters.ChatTypeFilter(types.ChatType.PRIVATE),
                    Text("Получение списков"))
async def get_user_list_for_admin(message: types.Message):
    await bot.send_message(message.from_user.id, text="Команды",
                           reply_markup=admins_buttons)


@dp.message_handler(SuperAdminFilter(), filters.ChatTypeFilter(types.ChatType.PRIVATE), Text("BOSSES"))
async def get_superadmins(message: types.Message):
    await bot.send_message(message.from_user.id, "Список боссов",
                           reply_markup=await get_inline_buttons(["SUPER_ADMIN"]))


@dp.message_handler(SuperAdminAndAdminFilter(), filters.ChatTypeFilter(types.ChatType.PRIVATE), Text("ADMINS"))
async def get_admins(message: types.Message):
    await bot.send_message(message.from_user.id, "Список админов",
                           reply_markup=await get_inline_buttons(["ADMIN"]))


@dp.message_handler(SuperAdminAndAdminFilter(), filters.ChatTypeFilter(types.ChatType.PRIVATE), Text("USERS"))
async def get_users(message: types.Message):
    await bot.send_message(message.from_user.id, "Список клиентов",
                           reply_markup=await get_inline_buttons(["USER"]))


@dp.message_handler(SuperAdminAndAdminFilter(), filters.ChatTypeFilter(types.ChatType.PRIVATE), Text("NO USERS"))
async def get_ex_users(message: types.Message):
    await bot.send_message(message.from_user.id, "Список не клиентов",
                           reply_markup=await get_inline_buttons(["NO_USER"]))


getters_users_superadmins_button_list = [
    [[ROLE.SUPER_ADMIN], KeyboardButton(text="BOSSES")],
    [[ROLE.SUPER_ADMIN, ROLE.ADMIN], KeyboardButton(text="ADMINS")],
    [[ROLE.SUPER_ADMIN, ROLE.ADMIN], KeyboardButton(text="USERS")],
    [[ROLE.SUPER_ADMIN, ROLE.ADMIN], KeyboardButton(text="NO USERS")],
    [[ROLE.SUPER_ADMIN, ROLE.ADMIN], KeyboardButton(text="Главное меню")]
]

super_admins_buttons = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)\
    .add(*get_buttons_for_role(ROLE.SUPER_ADMIN, getters_users_superadmins_button_list))


admins_buttons = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)\
    .add(*get_buttons_for_role(ROLE.ADMIN, getters_users_superadmins_button_list))


async def get_inline_buttons(roles):
    user_list = get_users_from_db(roles)
    inline_markup = InlineKeyboardMarkup(row_width=2)
    for user in user_list:
        inline_markup.add(InlineKeyboardButton(user[1] if user[1] else "FOREVER", callback_data=user[0]),
                          InlineKeyboardButton(user[0], url="https://t.me/" + user[0]))
    return inline_markup
