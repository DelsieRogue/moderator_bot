from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from common.common import PRICE, SALE, COEF, CARD_NUMBER, CARD_OWNER, CARD_BANK
from config.init import dp, bot
from filters.handler_filter import NoUserFilter

chanel_count_buttons = [
    InlineKeyboardButton(text="1", callback_data="buy_subscribe_1"),
    InlineKeyboardButton(text="2", callback_data="buy_subscribe_2"),
    InlineKeyboardButton(text="3", callback_data="buy_subscribe_3"),
    InlineKeyboardButton(text="4", callback_data="buy_subscribe_4"),
    InlineKeyboardButton(text="5", callback_data="buy_subscribe_5"),
    InlineKeyboardButton(text="6", callback_data="buy_subscribe_6"),
    InlineKeyboardButton(text="7", callback_data="buy_subscribe_7"),
    InlineKeyboardButton(text="8", callback_data="buy_subscribe_8"),
    InlineKeyboardButton(text="9", callback_data="buy_subscribe_9")
]

chanel_count = InlineKeyboardMarkup(row_width=3, resize_keyboard=True).add(*chanel_count_buttons)


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


@dp.callback_query_handler(lambda c: c.data.startswith('buy_subscribe_'))
async def buy_subscribe(callback: types.CallbackQuery):
    count = int(callback.data.replace("buy_subscribe_", ""))
    price = calculate_price(count)
    sale = count * PRICE - price
    await bot.send_message(callback.message.chat.id, f"Стоимость для {count} канал{'а' if count == 1 else 'ов'} "
                                                     f"составляет {price} руб. \n"
                                                     f"{f'Скидка - {sale} руб.' if sale != 0 else ''}",
                           reply_markup=InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
                           .add(InlineKeyboardButton(text=f"Оплатить {price} руб.", callback_data=f"accept_{count}")))
    await callback.answer("")


@dp.callback_query_handler(lambda c: c.data.startswith('accept_'))
async def accept(callback: types.CallbackQuery):
    count = int(callback.data.replace("accept_", ""))
    await bot.send_message(callback.message.chat.id, f"Номер карты - {CARD_NUMBER} \n"
                                                     f"Банк получатель - {CARD_BANK} \n"
                                                     f"Владелец - {CARD_OWNER}\n\n"
                                                     f"После оплаты нажмите кнопку 'Оплатил' "
                                                     f"и в ближайшее время вам дадут доступы",
                           reply_markup=InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
                           .add(InlineKeyboardButton(text="Оплатил", callback_data=f"paid_{count}")))
    await callback.answer("")


@dp.callback_query_handler(lambda c: c.data.startswith('paid_'))
async def paid(callback: types.CallbackQuery):
    count = int(callback.data.replace("paid_", ""))
    # дописать отправление админу
    await bot.send_message(callback.message.chat.id, "Отправлено на проверку")
    await callback.answer("")
