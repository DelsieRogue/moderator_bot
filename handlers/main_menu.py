from enum import Enum

from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from common.common import get_buttons_for_role, ROLE
from config.init import dp, bot
from filters.handler_filter import SuperAdminFilter, AdminFilter, UserFilter, NoUserFilter


# ---------------------------------SUPER ADMIN-----------------------------------------

@dp.message_handler(SuperAdminFilter(), filters.ChatTypeFilter(types.ChatType.PRIVATE),
                    text=['/start', 'Главное меню'])
async def start_for_super_admin(message: types.Message):
    await bot.send_message(message.from_user.id, text="Главное меню",
                           reply_markup=super_admins_buttons)


# ---------------------------------ADMIN-----------------------------------------

@dp.message_handler(AdminFilter(), filters.ChatTypeFilter(types.ChatType.PRIVATE),
                    text=['/start', 'Главное меню', 'Обновить роль'])
async def start_for_admin(message: types.Message):
    await bot.send_message(message.from_user.id, text="Главное меню",
                           reply_markup=admins_buttons)


# ---------------------------------USER-----------------------------------------

@dp.message_handler(UserFilter(), filters.ChatTypeFilter(types.ChatType.PRIVATE),
                    text=['/start', 'Главное меню', 'Обновить роль'])
async def start_for_user(message: types.Message):
    await bot.send_message(message.from_user.id, text="Главное меню",
                           reply_markup=user_buttons)


# ---------------------------------NO_USER-----------------------------------------

@dp.message_handler(NoUserFilter(), filters.ChatTypeFilter(types.ChatType.PRIVATE),
                    text=['/start', 'Главное меню', 'Обновить роль'])
async def start_for_no_user(message: types.Message):
    await bot.send_message(message.from_user.id, text="Главное меню",
                           reply_markup=no_user_buttons)

# --------------------------------------------------------------------------------

main_menu_admins_button_list = [
    [[ROLE.SUPER_ADMIN], KeyboardButton(text="Ждут одобрения")],
    [[ROLE.ADMIN, ROLE.SUPER_ADMIN], KeyboardButton(text="Получение списков")],
    [[ROLE.ADMIN, ROLE.SUPER_ADMIN], KeyboardButton(text="Действия")],
    [[ROLE.SUPER_ADMIN], KeyboardButton(text="Вкл/Выкл чистки")],
    [[ROLE.ADMIN, ROLE.SUPER_ADMIN], KeyboardButton(text="История заказов")],
    [[ROLE.SUPER_ADMIN], KeyboardButton(text="Анализ финансов")],
    [[ROLE.USER, ROLE.NO_USER], KeyboardButton(text="Прайслист и условия")],
    [[ROLE.USER], KeyboardButton(text="Продлить подписку")],
    [[ROLE.USER], KeyboardButton(text="Дата окончания текущей подписки")],
    [[ROLE.NO_USER], KeyboardButton(text="Купить подписку")],
    [[ROLE.NO_USER], KeyboardButton(text="Активировать подписку")],
    [[ROLE.NO_USER.ADMIN, ROLE.USER, ROLE.NO_USER], KeyboardButton(text="Обновить роль")]
]

super_admins_buttons = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) \
    .add(*get_buttons_for_role(ROLE.SUPER_ADMIN, main_menu_admins_button_list))

admins_buttons = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) \
    .add(*get_buttons_for_role(ROLE.ADMIN, main_menu_admins_button_list))

user_buttons = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) \
    .add(*get_buttons_for_role(ROLE.USER, main_menu_admins_button_list))

no_user_buttons = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) \
    .add(*get_buttons_for_role(ROLE.NO_USER, main_menu_admins_button_list))

