from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import BoundFilter

from common.common import ROLE
from data_base.scripts import get_role_name_by_user_id, add_user_to_table_users

clean_chat_trigger = True


def get_role_or_create_user(message: types.Message) -> ROLE:
    role = get_role_name_by_user_id(message.from_user.id)
    if not role:
        add_user_to_table_users(message.from_user.id, message.from_user.username, ROLE.NO_USER.name,
                                message.from_user.first_name, message.from_user.last_name)
        return ROLE.NO_USER
    return ROLE[role[0]]


def check_role(message: types.Message, role_list: list) -> bool:
    return get_role_or_create_user(message) in role_list


class SuperAdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        return check_role(message, [ROLE.SUPER_ADMIN])


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        return check_role(message, [ROLE.ADMIN])


class UserFilter(BoundFilter):
    async def check(self, message: types.Message):
        return check_role(message, [ROLE.USER])


class NoUserFilter(BoundFilter):
    async def check(self, message: types.Message):
        return check_role(message, [ROLE.NO_USER])


class SuperAdminAndAdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        return check_role(message, [ROLE.ADMIN, ROLE.ADMIN.SUPER_ADMIN])


class CleaningChatFilter(BoundFilter):
    async def check(self, message: types.Message):
        role = get_role_or_create_user(message)
        if clean_chat_trigger and role not in [ROLE.USER, ROLE.ADMIN, ROLE.ADMIN.SUPER_ADMIN]:
            return True
        return False


def setup(dp: Dispatcher):
    pass
    dp.filters_factory.bind(SuperAdminFilter)
    dp.filters_factory.bind(AdminFilter)


async def on_startup(dp):
    setup(dp)
