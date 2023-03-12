from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

from common.common import PRICE, SALE, COEF, CARD_NUMBER, CARD_OWNER, CARD_BANK, USER_ID
from config.init import dp, bot
from data_base.scripts import add_order
from filters.handler_filter import NoUserFilter

callback_buy_subscribe = CallbackData("buy_subscribe", "count")
chanel_count_buttons = [InlineKeyboardButton(str(i), callback_data=callback_buy_subscribe.new(count=i)) for i in
                        range(1, 10)]
chanel_count = InlineKeyboardMarkup(row_width=3, resize_keyboard=True).add(*chanel_count_buttons)

callback_requisites = CallbackData("get_requisites", "step", "count", "price", "sale")

callback_pay_result = CallbackData("pay_result", "result", "count", "user_id", "price", "sale")
callback_info_channels = CallbackData("info_channels", "step", "count", "index")


class FSMFillForm(StatesGroup):
    count = State()
    index = State()
    ref = State()
    name_ref = State()
    name = State()
    n_sub = State()
    n_view = State()
    price = State()
    contact = State()
    user_for_send = State()


def calculate_price(count: int) -> int:
    res_price = PRICE * count
    res_sale = 0
    coef = COEF
    for i in range(1, count):
        res_sale += SALE / 100 * coef * PRICE
        coef *= 1.12
    return int(res_price - res_sale)


@dp.message_handler(NoUserFilter(), filters.ChatTypeFilter(types.ChatType.PRIVATE), Text("Купить подписку"))
async def buy_sub(message: types.Message):
    await bot.send_message(message.from_user.id, "Для скольки каналов вы хотите приобрести подписку?",
                           reply_markup=chanel_count)


@dp.callback_query_handler(callback_buy_subscribe.filter())
async def buy_subscribe(callback: types.CallbackQuery, callback_data: dict):
    count = int(callback_data['count'])
    price = calculate_price(count)
    sale = count * PRICE - price
    await bot.send_message(callback.message.chat.id, f"Стоимость для {count} канал{'а' if count == 1 else 'ов'} "
                                                     f"составляет {price} руб. \n"
                                                     f"{f'Скидка - {sale} руб.' if sale != 0 else ''}",
                           reply_markup=InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
                           .add(InlineKeyboardButton(text=f"Оплатить {price} руб.",
                                                     callback_data=callback_requisites.new(
                                                         step="requisites", count=count, price=price, sale=sale))))
    await callback.answer("")


@dp.callback_query_handler(callback_requisites.filter(step="requisites"))
async def accept(callback: types.CallbackQuery, callback_data: dict):
    await bot.send_message(callback.message.chat.id, f"Номер карты - {CARD_NUMBER} \n"
                                                     f"Банк получатель - {CARD_BANK} \n"
                                                     f"Владелец - {CARD_OWNER}\n\n"
                                                     f"После оплаты нажмите кнопку 'Оплатил' "
                                                     f"и в ближайшее время вам дадут доступы",
                           reply_markup=InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
                           .add(InlineKeyboardButton(text="Оплатил", callback_data=callback_requisites.new(
                               step="pay_confirm", count=callback_data['count'],
                               price=callback_data['price'], sale=callback_data['sale']))))
    await callback.answer("")


@dp.callback_query_handler(callback_requisites.filter(step="pay_confirm"))
async def pay_confirm(callback: types.CallbackQuery, callback_data: dict):
    count = int(callback_data['count'])
    price = int(callback_data['price'])
    sale = int(callback_data['sale'])
    username = callback.from_user.username

    buttons = InlineKeyboardMarkup()
    buttons.add(InlineKeyboardButton(text="Покупатель " + username, url="https://t.me/" + username))
    buttons.add(InlineKeyboardButton(text="Подтвердить",
                                     callback_data=callback_pay_result.new(result="success", count=count,
                                                                           user_id=callback.from_user.id, price=price,
                                                                           sale=sale)),
                InlineKeyboardButton(text="Отказать",
                                     callback_data=callback_pay_result.new(result="failed", count=count,
                                                                           user_id=callback.from_user.id, price=price,
                                                                           sale=sale)))

    await bot.send_message(USER_ID, f"Подтверждение оплаты для {count} канал{'а' if count == '1' else 'ов'} \n"
                                    f"Сумма = {price} руб. Cкидка = {sale} руб.",
                           reply_markup=buttons)
    await bot.send_message(callback.from_user.id, "Обработка платежа...")
    await callback.answer("")


@dp.callback_query_handler(callback_pay_result.filter(result="success"))
async def paid(callback: types.CallbackQuery, callback_data: dict):
    count = int(callback_data['count'])
    price = int(callback_data['price'])
    sale = int(callback_data['sale'])
    user_id = callback_data['user_id']

    add_order(user_id, float(price), count)
    button = InlineKeyboardMarkup(row_width=1)
    button.add(InlineKeyboardButton(text="Приступить к заполнению",
                                    callback_data=callback_info_channels.new(step="fill", count=count, index=1)))
    await bot.send_message(chat_id=int(user_id), text="Платеж подтвержден!\n"
                                                      "Давайте теперь заполним информацию по каналам.\n",
                           reply_markup=button)
    await callback.answer("")


@dp.callback_query_handler(callback_info_channels.filter(step="fill"))
async def start(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    if not await state.get_data():
        count = int(callback_data['count'])
        index = int(callback_data['index'])
        await state.update_data(count=count)
        await state.update_data(index=index)

    data = await state.get_data()
    await bot.send_message(chat_id=callback.from_user.id, text=f"Введите ссылку для {data['index']}-го канала",
                           reply_markup=ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                           .add(KeyboardButton(text="Заполнить канал заново")))
    await FSMFillForm.ref.set()
    await callback.answer("")


async def check_ref(message: types.Message, state: FSMContext) -> bool:
    text = message.text
    if text.startswith('https://t.me/'):
        await state.update_data(name_ref='TG')
    elif text.startswith('https://vk.com/'):
        await state.update_data(name_ref='VK')
    elif text.startswith('https://www.instagram.com/'):
        await state.update_data(name_ref='INST')
    else:
        await bot.send_message(message.from_user.id, "Некорректная ссылка. Напомним, что принимаются ссылки TG, VK, INST.")
        return False
    return True


@dp.message_handler(state=FSMFillForm.ref)
async def set_ref(message: types.Message, state: FSMContext):
    if not await check_ref(message, state):
        await bot.send_message(message.from_user.id, "Введите ссылку еще раз")
        return
    await state.update_data(ref=message.text)
    await bot.send_message(chat_id=message.from_user.id, text="Введите название канала.")
    await FSMFillForm.name.set()


@dp.message_handler(state=FSMFillForm.name)
async def set_name(message: types.Message, state: FSMContext):
    if len(message.text) > 60:
        await bot.send_message(message.from_user.id, "Максимальная длина названия 60 символов. Введите название еще раз.")
        return
    await state.update_data(name=message.text)
    await bot.send_message(chat_id=message.from_user.id, text="Введите количество подписчиков")
    await FSMFillForm.n_sub.set()


@dp.message_handler(state=FSMFillForm.n_sub)
async def set_n_sub(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) > 9999999:
        await bot.send_message(message.from_user.id, "Найдены буквы, либо же число слишком большое. Введите еще раз.")
        return
    await state.update_data(n_sub=message.text)
    await bot.send_message(chat_id=message.from_user.id, text="Введите среднее количество просмотров на пост")
    await FSMFillForm.n_view.set()


@dp.message_handler(state=FSMFillForm.n_view)
async def set_n_view(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) > 9999999:
        await bot.send_message(message.from_user.id, "Найдены буквы, либо же число слишком большое. Введите еще раз.")
        return
    await state.update_data(n_view=message.text)
    await bot.send_message(chat_id=message.from_user.id, text="Введите минимальную стоимость рекламы")
    await FSMFillForm.price.set()


@dp.message_handler(state=FSMFillForm.price)
async def set_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) > 1000000:
        await bot.send_message(message.from_user.id, "Найдены буквы, либо же число слишком большое. Введите еще раз.")
        return
    await state.update_data(price=message.text)
    await bot.send_message(chat_id=message.from_user.id, text="Введите контакты к кому обраться по поводу покупки рекламы на канале")
    await FSMFillForm.contact.set()


async def get_result_post(data: dict) -> str:
    return f"<b>{data['name_ref']}: <a href='{data['ref']}'>{data['name']}</a>\n" \
           f"👥 Подписчики: {data['n_sub']}+\n" \
           f"👀 Просмотры: {data['n_view']}+\n" \
           f"💵 Цена: от {data['price']}₽\n" \
           f"📩 Для связи: {data['contact']}\n\n" \
           f"Выкладывают рекламу: {data['user_for_send']}</b>"


@dp.message_handler(state=FSMFillForm.contact)
async def set_contact(message: types.Message, state: FSMContext):
    if not message.text.startswith('@') and len(message.text) > 1:
        await bot.send_message(message.from_user.id, "Контакты должны начинаться с '@'. Например @ivan. Введите еще раз.")
        return
    await state.update_data(contact=message.text)
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите пользователей, которые будут выкладывать сообщения в чат. Максимум 3 человека. Например: @ivan @lena @vova")
    await FSMFillForm.user_for_send.set()


@dp.message_handler(state=FSMFillForm.user_for_send)
async def set_user_for_send(message: types.Message, state: FSMContext):
    usernames = message.text.strip().split(" ")
    res_check: bool = len(usernames) <= 3 and not list(filter(lambda a: not a.startswith('@') or len(a) < 2, usernames))
    if not res_check:
        await bot.send_message(message.from_user.id, "Ошибка при заполнение проверьте внимательно.")
        return
    await state.update_data(user_for_send=message.text)
    data = await state.get_data()
    count = data['count']
    index = data['index']

    button = InlineKeyboardMarkup(row_width=2)
    res_post = await get_result_post(data)
    await bot.send_message(chat_id=message.from_user.id, text=res_post, parse_mode='HTML', disable_web_page_preview=True)

    button.add(InlineKeyboardButton(text=f"Да", callback_data=callback_info_channels.new(step="confirm", count=count, index=index + 1)))
    button.add(InlineKeyboardButton(text=f"Нет, заполнить заново", callback_data=callback_info_channels.new(step="fill", count=count, index=index)))
    await bot.send_message(chat_id=message.from_user.id, text=f"Данные заполнены правильно?", reply_markup=button)
    await state.reset_state()


@dp.callback_query_handler(callback_info_channels.filter(step="confirm"))
async def start(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    count = data['count']
    index = data['index']

    if index < count:
        await state.update_data(index=index + 1)
        button = InlineKeyboardMarkup(row_width=1)
        button.add(InlineKeyboardButton(text=f"Нет, заполнить заново", callback_data=callback_info_channels.new(step="fill", count=count, index=index + 1)))
        await state.reset_state()

    await state.finish()

# https://t.me/tvoi_wildberries
# Твой Wildberries
# 13000
# 7000
# 400
# @TimkaGA
