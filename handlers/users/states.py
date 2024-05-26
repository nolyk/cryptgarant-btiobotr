from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import bot, vip
from data import (
    Users,
    info_user,
    search_user_msg,
    Deals,
    deal_create_msg,
)
from keyboards import open_deal_markup, info_deal_markup, accept_deal_markup
from states import SearchUser, OpenDeal
from utils import config


@vip.message_handler(state=SearchUser.username)
async def search_username(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        await msg.answer(
            text='<b>🔍 Ведем поиск...</b>'
        )
        await state.finish()
        status = await Users().checkFromBase(
            user_id=msg.text
        )
        print(status)
        if status:
            user = await Users.get(user_id=msg.text)
            if msg.from_user.id != msg.text and user.username != msg.from_user.username:
                await msg.answer(
                    text=search_user_msg.format(
                        username=user.username,
                        user_id=user.user_id,
                        deals=await Deals.getCountUserDeals(
                            user_id=user.user_id,
                            status="ALL"
                        ),
                        success=await Deals.getCountUserDeals(
                            user_id=user.user_id,
                            status="Закрыта"
                        ),
                        canceled=await Deals.getCountUserDeals(
                            user_id=user.user_id,
                            status="Отменена"
                        ),
                        rating=user.rating),
                    reply_markup=open_deal_markup(user.user_id)
                )
            else:
                await msg.answer(
                    text=info_user.format(
                        username=user.username,
                        deals=await Deals.getCountUserDeals(
                            user_id=msg.from_user.id,
                            status="ALL"
                        ),
                        success=await Deals.getCountUserDeals(
                            user_id=msg.from_user.id,
                            status="Закрыта"
                        ),
                        canceled=await Deals.getCountUserDeals(
                            user_id=msg.from_user.id,
                            status="Отменена"
                        ),
                        rating=user.rating
                    ),
                    reply_markup=info_deal_markup(msg.from_user.id)
                )
        else:
            await msg.answer(
                text='<b>Мы не нашли такого пользователя</b>'
            )
    else:
        username = msg.text
        await msg.answer(
            text='<b>🔍 Ведем поиск...</b>'
        )
        await state.finish()
        status = await Users.checkingUsername(username)
        print(username)
        print(status)
        if status:
            user = await Users.get(username=username)
            if user.username != msg.from_user.username and user.user_id != msg.from_user.id:
                await msg.answer(
                    text=search_user_msg.format(
                        username=user.username,
                        user_id=user.user_id,
                        deals=await Deals.getCountUserDeals(
                            user_id=user.user_id,
                            status="ALL"
                        ),
                        success=await Deals.getCountUserDeals(
                            user_id=user.user_id,
                            status="Закрыта"
                        ),
                        canceled=await Deals.getCountUserDeals(
                            user_id=user.user_id,
                            status="Отменена"
                        ),
                        rating=user.rating),
                    reply_markup=open_deal_markup(user.user_id)
                )
            else:
                await msg.answer(
                    text=info_user.format(
                        username=user.username,
                        deals=await Deals.getCountUserDeals(
                            user_id=msg.from_user.id,
                            status="ALL"
                        ),
                        success=await Deals.getCountUserDeals(
                            user_id=msg.from_user.id,
                            status="Закрыта"
                        ),
                        canceled=await Deals.getCountUserDeals(
                            user_id=msg.from_user.id,
                            status="Отменена"
                        ),
                        rating=user.rating
                    ),
                    reply_markup=info_deal_markup(msg.from_user.id)
                )
        else:
            await msg.answer(
                text='<b>Мы не нашли такого пользователя</b>'
            )


@vip.message_handler(state=OpenDeal.amount)
async def open_deal(msg: Message, state: FSMContext):
    if msg.text.isdecimal():
        if int(msg.text) >= int(config.config('min_sum_deal')):
            async with state.proxy() as data:
                data['amount'] = msg.text

            await msg.answer(
                text='<b>Введите описание к сделке</b>'
            )
            await OpenDeal.next()
        else:
            await state.finish()
            await msg.answer(
                text=f'<b>Минимальная сумма сделки</b> {config.config("min_sum_deal")} RUB'
            )
    else:
        await state.finish()
        await msg.answer(
            text='<b>Вводить нужно только цифры!</b>'
        )


@vip.message_handler(state=OpenDeal.info)
async def open_deal(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['user_id']
        amount = data['amount']
    await state.finish()
    seller = await Users.get(user_id=user_id)
    buyer = await Users.get(user_id=msg.from_user.id)

    if float(amount) <= float(buyer.balance) and float(buyer.balance) >= int(config.config("min_sum_deal")):

        deal_id = await Deals.writeNewDeal(
            user_create=msg.from_user.id,
            user_invite=user_id,
            amount=amount,
            description=msg.text
        )
        await state.finish()

        await msg.answer(
            text=deal_create_msg.format(
                id_deal=deal_id,
                seller=seller.username,
                buyer=buyer.username,
                amount=amount,
                info=msg.text,
                status='Ожидает подтверждения'
            )
        )
        await bot.send_message(
            chat_id=user_id,
            text=deal_create_msg.format(
                id_deal=deal_id,
                seller=seller.username,
                buyer=buyer.username,
                amount=amount,
                info=msg.text,
                status='Ожидает подтверждения'
            ),
            reply_markup=accept_deal_markup(deal_id))
    else:
        await msg.answer(
            text="<b>Недостаточно баланса для совершения сделки!</b>"
        )
