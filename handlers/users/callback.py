from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.dispatcher import FSMContext

from loader import vip, bot
from data import Users, deal_create_msg, group_deal_msg, refferal_msg, inform_msg, cabinet_msg, BlackList, Deals
from keyboards import (
    deals_markup,
    garant_markup,
    accept_deal_markup,
    pay_deal_markup,
    conditions_deal_markup,
    finish_deal_markup,
    finish_seller_markup,
    arbitrator_markup,
    rating_markup,
    view_markup,
    return_markup,
    information_markup,
    partners_markup,
    cabinet_markup
)
from states import SearchUser, OpenDeal
from utils import config


@vip.callback_query_handler(text_startswith="close-message")
async def close_handler(call: CallbackQuery):
    await call.message.delete()


@vip.callback_query_handler(text_startswith="return-menu:")
async def return_handler(call: CallbackQuery):
    if call.data.split(":")[1] == "default":
        await call.message.edit_media(
            InputMediaPhoto(media=('https://telegra.ph/file/a0324f8b445c4b724dfcf.png'), caption=''),
            reply_markup=garant_markup())
    elif call.data.split(":")[1] == "cabinet":
        user = await Users.get(user_id=call.from_user.id)
        await call.message.edit_caption(
            caption=cabinet_msg.format(
                user_id=call.from_user.id,
                login=call.from_user.get_mention(),
                data=str(user.date)[:10],
                deals=await Deals.getCountUserDeals(
                    user_id=call.from_user.id,
                    status="ALL"
                ),
                success=await Deals.getCountUserDeals(
                    user_id=call.from_user.id,
                    status="Закрыта"
                ),
                canceled=await Deals.getCountUserDeals(
                    user_id=call.from_user.id,
                    status="Отменена"
                ),
                rating=user.rating,
                balance=user.balance
            ),
            reply_markup=cabinet_markup()
        )
    elif call.data.split(":")[1] == "black":
        markup = await BlackList.getMarkup()
        if markup:
            await call.message.edit_caption(
                caption="<b>🛡 Ниже можно увидеть всех скамеров из нашей базы:</b>",
                reply_markup=markup
            )
        else:
            await call.message.edit_caption(
                caption="<b>Пока нет ни одного скамера в базе...</b>",
                reply_markup=return_markup()
            )

    else:
        await call.message.delete()


@vip.callback_query_handler(text="user-information")
async def inform_handler(call: CallbackQuery):
    await call.message.edit_caption(
        caption=inform_msg,
        reply_markup=information_markup()
    )


@vip.callback_query_handler(text="partners-bot")
async def partners_bot_handler(call: CallbackQuery):
    await call.message.edit_caption(
        caption="<b>Наши партнеры:</b>",
        reply_markup=partners_markup()
    )


@vip.callback_query_handler(text="user-parners")
async def parners_handler(call: CallbackQuery):
    await call.message.edit_caption(
        caption=refferal_msg.format(
            bot_login="EWGarantBot",
            ref_code=call.from_user.id,
            ref_percent=config.config("ref_percent")
        ),
        reply_markup=return_markup()
    )


@vip.callback_query_handler(text="user-deals")
async def deals_handler(call: CallbackQuery):
    await call.message.edit_media(InputMediaPhoto(media=('https://telegra.ph/file/a0324f8b445c4b724dfcf.png'), caption=''), reply_markup=deals_markup())


@vip.callback_query_handler(text_startswith="user-deals:")
async def user_deals_handler(call: CallbackQuery):
    markup = await Deals.getUserDealsMarkup(
        _type=call.data.split(":")[1],
        user_id=call.from_user.id
    )
    face = 'Продавца' if call.data.split(':')[1] == 'seller' else 'Покупателя'
    if markup:
        await call.message.edit_caption(
            caption=f"<b>🤝 Вот все ваши сделки от лица {face}</b>",
            reply_markup=markup
        )
    else:
        await call.answer(
            text=f"У вас нет сделок от лица {face}",
            show_alert=True
        )


@vip.callback_query_handler(text="user-search-deal")
async def search_deal_handler(call: CallbackQuery):
    await SearchUser.username.set()
    await call.message.delete()
    await call.message.answer(
        text="<b>Введите юзернейм без @ (вот так: username) или ID пользователя</b>"
    )


@vip.callback_query_handler(text_startswith="user-open-deal:")
async def view_deal_handler(call: CallbackQuery, state: FSMContext):
    await OpenDeal.amount.set()
    async with state.proxy() as data:
        data['user_id'] = call.data.split(":")[1]

    await call.message.edit_text(
        text="<b>Введите сумму сделки:</b>"
    )


@vip.callback_query_handler(text_startswith="view-deal:")
async def view_deal_handler(call: CallbackQuery):
    deal = await Deals.get(id=call.data.split(":")[1])
    buyer = await Users.get(user_id=deal.buyer_id)
    seller = await Users.get(user_id=deal.seller_id)

    if deal.status == "Открыта":
        await call.message.edit_caption(
            caption=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status='Ожидаем подтверждения от продавца' if deal.buyer_id == call.from_user.id else "Подтвердите"
            ),
            reply_markup=None if deal.buyer_id == call.from_user.id else accept_deal_markup(deal.id)

        )
    elif deal.status == "Ожидает оплаты":
        await call.message.edit_caption(
            caption=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status="Ожидание оплаты" if deal.buyer_id == call.from_user.id else 'Ожидайте уведомления об оплате'
            ),
            reply_markup=None if deal.buyer_id != call.from_user.id else pay_deal_markup(deal.id)

        )
    elif deal.status == "Оплачена":
        await call.message.edit_caption(
            caption=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status='Ожидайте передачу услуги/товара'
                if deal.buyer_id == call.from_user.id else "Оплачена, можете передавать товар/услугу"
            ),
            reply_markup=None if deal.buyer_id == call.from_user.id else conditions_deal_markup(deal.id)

        )
    elif deal.status == "Финал":
        await call.message.edit_caption(
            caption=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status='Условия выполнены' + "\n\n‼️ Проверьте качество товара\услуги, "
                                             "а потом уже отпускайте деньги продавцу!"
                if deal.buyer_id == call.from_user.id else "Закрыта, ожидайте подтверждения от покупателя"
            ),
            reply_markup=finish_seller_markup(deal.id)
            if deal.buyer_id != call.from_user.id else finish_deal_markup(deal.id)

        )
    elif deal.status == "Арбитраж":
        await call.message.edit_caption(
            caption=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status='Арбитраж'
            ),
            reply_markup=arbitrator_markup()
        )
    else:
        await call.message.edit_caption(
            caption=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status='Закрыта'
            )
        )


@vip.callback_query_handler(text_startswith="refurse-deal:")
async def refurse_deal_handler(call: CallbackQuery):
    deal = await Deals.get(id=call.data.split(":")[1])
    await call.message.delete()

    await call.message.answer(
        text=f'<b>🌀 Сделка: #EW_{deal.id} Отменена</b>'
    )
    await bot.send_message(
        chat_id=deal.buyer_id,
        text=f'<b>🌀 Сделка: #EW_{deal.id} Отменена</b>'
    )
    await Deals.updateStatus(
        dl_id=call.data.split(":")[1],
        status="Отменена"
    )


@vip.callback_query_handler(text_startswith="refund-deal:")
async def refund_deal_handler(call: CallbackQuery):
    deal = await Deals.get(id=call.data.split(":")[1])

    if deal.status == "Оплачена":
        await Users.updateBalance(
            user_id=deal.buyer_id,
            amount=deal.amount
        )
        await Deals.updateStatus(
            dl_id=call.data.split(":")[1],
            status="Отменена"
        )

        await call.message.delete()

        await bot.send_message(
            chat_id=config.config('group_id'),
            text=f'<b>🌀 Cделка #EW_{deal.id} отменена!</b>'
        )
        await bot.send_message(
            chat_id=deal.buyer_id,
            text=f'<b>🌀 Cделка #EW_{deal.id} отменена, деньги вернулись вам на баланс!</b>'
        )
        await bot.send_message(
            chat_id=deal.seller_id,
            text=f'<b>🌀 Вы отменили сделку #EW_{deal.id}, деньги были возвращены на баланс покупателя</b>'
        )


@vip.callback_query_handler(text_startswith="accept-deal:")
async def accept_deal_handler(call: CallbackQuery):
    deal = await Deals.get(id=call.data.split(":")[1])
    if deal.status == 'Открыта':
        buyer = await Users.get(user_id=deal.buyer_id)
        seller = await Users.get(user_id=deal.seller_id)

        await Deals.updateStatus(
            dl_id=call.data.split(":")[1],
            status="Ожидает оплаты"
        )

        await bot.send_message(
            chat_id=deal.buyer_id,
            text=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status='Ожидание оплаты'
            ),
            reply_markup=pay_deal_markup(deal.id))
        await bot.send_message(
            chat_id=deal.seller_id,
            text=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status='Ожидайте уведомления об оплате'
            )
        )
        await call.message.delete()


@vip.callback_query_handler(text_startswith="pay-deal:")
async def pay_deal_handler(call: CallbackQuery):
    deal = await Deals.get(id=call.data.split(":")[1])
    print(deal.status)

    if deal.status == 'Ожидает оплаты':
        buyer = await Users.get(user_id=deal.buyer_id)
        seller = await Users.get(user_id=deal.seller_id)

        balance = buyer.balance
        if float(balance) >= float(deal.amount):
            await Users.updateBalance(
                user_id=deal.buyer_id,
                amount=-float(deal.amount)
            )
            await Deals.updateStatus(
                dl_id=call.data.split(":")[1],
                status="Оплачена"
            )

            await bot.send_message(
                chat_id=config.config('group_id'),
                text=group_deal_msg.format(
                    id_deal=deal.id,
                    seller=seller.username,
                    buyer=buyer.username,
                    amount=deal.amount,
                    info='Новая сделка'
                )
            )
            await bot.send_message(
                chat_id=deal.buyer_id,
                text=deal_create_msg.format(
                    id_deal=deal.id,
                    seller=seller.username,
                    buyer=buyer.username,
                    amount=deal.amount,
                    info=deal.description,
                    status='Ожидайте передачу услуги/товара')
            )
            await bot.send_message(
                chat_id=deal.seller_id,
                text=deal_create_msg.format(
                    id_deal=deal.id,
                    seller=seller.username,
                    buyer=buyer.username,
                    amount=deal.amount,
                    info=deal.description,
                    status='Оплачена, можете передавать товар/услугу'
                ),
                reply_markup=conditions_deal_markup(deal.id))

            await bot.send_message(
                chat_id=config.config('admin_group'),
                text=f"<b>🌀 Сделка:</b> #EW_{deal.id}\n\n"
                     f"<b>💈 Продавец:</b> @{seller.username} | "
                     f"<b>Покупатель:</b> @{buyer.username}\n"
                     f"<b>💳 Сумма:</b> <code>{deal.amount}</code> RUB\n"
                     f"<b>📝 Условия:</b>\n <code>{deal.description}</code>\n"
                     f"<b>🧿 Статус:</b> Новая сделка"
            )

            await call.message.delete()
        else:
            await call.message.answer(
                text='Недостаточно средств! Пополните баланс!'
            )


@vip.callback_query_handler(text_startswith="conditions-deal:")
async def conditions_deal_handler(call: CallbackQuery):
    deal = await Deals.get(id=call.data.split(":")[1])
    if deal.status == 'Оплачена':
        buyer = await Users.get(user_id=deal.buyer_id)
        seller = await Users.get(user_id=deal.seller_id)

        await Deals.updateStatus(
            dl_id=call.data.split(":")[1],
            status="Финал"
        )

        await bot.send_message(
            chat_id=deal.buyer_id,
            text=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status='Условия выполнены' + "\n\n‼️ Проверьте качество товара\услуги, "
                                             "а потом уже отпускайте деньги продавцу!"
            ),
            reply_markup=finish_deal_markup(deal.id)
        )
        await bot.send_message(
            chat_id=deal.seller_id,
            text=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status='Закрыта, ожидайте подтверждения от покупателя'
            ),
            reply_markup=finish_seller_markup(deal.id)
        )
        await call.message.delete()


@vip.callback_query_handler(text_startswith="finish-deal-sell:")
async def finish_deal_handler(call: CallbackQuery):
    deal = await Deals.get(id=call.data.split(":")[1])
    if deal.status == 'Финал':
        buyer = await Users.get(user_id=deal.buyer_id)
        seller = await Users.get(user_id=deal.seller_id)

        await Deals.updateStatus(
            dl_id=call.data.split(":")[1],
            status="Закрыта"
        )
        await Users.updateBalance(
            user_id=deal.seller_id,
            amount=deal.amount
        )
        await Users.updateCountDeals(
            user_id=deal.seller_id,
            count=1
        )
        await Users.updateCountDeals(
            user_id=deal.buyer_id,
            count=1
        )

        await bot.send_message(
            chat_id=config.config('group_id'),
            text=group_deal_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info='Завершена успешно'
            )
        )
        await bot.send_message(
            chat_id=deal.buyer_id,
            text=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status='Завершена успешно'
            )
        )
        await bot.send_message(
            chat_id=deal.seller_id,
            text=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status=f'Завершена успешно и вы получили {deal.amount} RUB'
            )
        )
        await bot.send_message(
            chat_id=deal.buyer_id,
            text=f'<b>Хотите оставить отзыв об работе @{seller.username}?</b>',
            reply_markup=view_markup(deal.seller_id)
        )
        await bot.send_message(
            chat_id=deal.buyer_id,
            text=f'<b>Оцените работу @{seller.username}</b>',
            reply_markup=rating_markup(deal.seller_id)
        )
        await bot.send_message(
            chat_id=deal.seller_id,
            text=f'<b>Оцените работу @{buyer.username}</b>',
            reply_markup=rating_markup(deal.buyer_id))

        await call.message.delete()


@vip.callback_query_handler(text_startswith="user-rating-")
async def rating_handler(call: CallbackQuery):
    status = call.data.split("-")[2].split(":")[0]
    user = await Users.get(user_id=call.data.split(":")[1])
    updater = await Users.get(user_id=call.from_user.id)
    await Users.updateRate(
        user_id=call.data.split(":")[1],
        rate=1 if status == "plus" else -1
    )
    await call.message.edit_text(
        text=f"<b>Успешно оставлен рейтинг: {1 if status == 'plus' else -1} для @{user.username}</b>"
    )
    await bot.send_message(
        chat_id=call.data.split(":")[1],
        text=f"<b>@{updater.username} {'повысил' if status == 'plus' else 'понизил'} ваш рейтинг!</b>"
    )


@vip.callback_query_handler(text_startswith="arbitration-deal:")
async def arbitration_deal_handler(call: CallbackQuery):
    deal = await Deals.get(id=call.data.split(":")[1])
    if deal.status == 'Финал':
        buyer = await Users.get(user_id=deal.buyer_id)
        seller = await Users.get(user_id=deal.seller_id)
        await Deals.updateStatus(
            dl_id=call.data.split(":")[1],
            status="Арбитраж"
        )

        await bot.send_message(
            chat_id=config.config('group_id'),
            text=group_deal_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount, info='Арбитраж'
            )
        )
        await bot.send_message(
            chat_id=deal.buyer_id,
            text=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status='Арбитраж'
            ),
            reply_markup=arbitrator_markup()
        )
        await bot.send_message(
            chat_id=deal.seller_id,
            text=deal_create_msg.format(
                id_deal=deal.id,
                seller=seller.username,
                buyer=buyer.username,
                amount=deal.amount,
                info=deal.description,
                status='Арбитраж'
            ),
            reply_markup=arbitrator_markup())

        await call.message.delete()
