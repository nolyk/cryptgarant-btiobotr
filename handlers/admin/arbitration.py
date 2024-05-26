from aiogram.types import Message, CallbackQuery

from loader import vip, bot
from filters import IsPrivate, IsAdmin
from keyboards import admin_button, adm_arb_markup
from data import Deals, Users, adm_deal_msg


@vip.message_handler(IsPrivate(), IsAdmin(), text=admin_button[3])
async def arbitration_handler(msg: Message):
    markup = await Deals.getArbitrationDealsMarkup()
    if markup:
        await msg.answer(
            text="<b>Держи все активные арбитражи:</b>",
            reply_markup=markup
        )
    else:
        await msg.answer(
            text="<b>Бро, пока нет активных арбитражей!</b>"
        )


@vip.callback_query_handler(text_startswith="arbitration-page:")
async def page_handler(call: CallbackQuery):
    markup = await Deals.getArbitrationDealsMarkup(
        page_number=int(call.data.split(":")[1])
    )
    await call.message.edit_reply_markup(
        reply_markup=markup
    )


@vip.callback_query_handler(text_startswith='admin-arb-deal:')
async def get_arb_handler(call: CallbackQuery):
    deal = await Deals.get(id=call.data.split(":")[1])
    seller = await Users.get(user_id=deal.seller_id)
    buyer = await Users.get(user_id=deal.buyer_id)

    await call.message.edit_text(
        text=adm_deal_msg.format(
            id_deal=deal.id,
            seller=seller.username,
            buyer=buyer.username,
            amount=deal.amount,
            info=deal.description
        ),
        reply_markup=adm_arb_markup(deal.id)
    )


@vip.callback_query_handler(text_startswith='favor-buyer:')
async def favor_handler(call: CallbackQuery):
    deal = await Deals.get(id=call.data.split(":")[1])
    await deal.updateStatus(
        dl_id=call.data.split(":")[1],
        status="Закрыта"
    )
    await Users.updateBalance(
        user_id=deal.buyer_id,
        amount=deal.amount
    )
    await Users.updateCountDeals(
        user_id=deal.buyer_id, count=1
    )
    await Users.updateCountDeals(
        user_id=deal.seller_id, count=1
    )

    await call.message.edit_text(
        text=f'<b>🌀 Cделка #CG_{deal.id} успешно закрыта в пользу покупателя</b>'
    )
    await bot.send_message(
        chat_id=deal.buyer_id,
        text=f"<b>🌀 Cделка #CG_{deal.id} закрыта в вашу пользу</b>"
    )
    await bot.send_message(
        chat_id=deal.seller_id,
        text=f"<b>🌀 Cделка #CG_{deal.id} закрыта в пользу покупателя</b>"
    )


@vip.callback_query_handler(text_startswith='favor-seller:')
async def favor_handler(call: CallbackQuery):
    deal = await Deals.get(id=call.data.split(":")[1])
    await Deals.updateStatus(
        dl_id=call.data.split(":")[1],
        status="Закрыта"
     )
    await Users().updateBalance(
        user_id=deal.seller_id,
        amount=deal.amount
    )
    await Users.updateCountDeals(
        user_id=deal.buyer_id, count=1
    )
    await Users.updateCountDeals(
        user_id=deal.seller_id, count=1
    )

    await call.message.edit_text(
        text=f'<b>🌀 Cделка #CG_{deal.id} успешно закрыта в пользу продавца</b>'
    )

    await bot.send_message(
        chat_id=deal.buyer_id,
        text=f"<b>🌀 Cделка #CG_{deal.id} закрыта в пользу продавца!</b>"
    )
    await bot.send_message(
        chat_id=deal.seller_id,
        text=f"<b>🌀 Cделка #CG_{deal.buyer_id} закрыта в вашу пользу</b>"
    )
