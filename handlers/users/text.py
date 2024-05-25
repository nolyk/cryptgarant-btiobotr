from aiogram.types import Message, CallbackQuery, InputMediaPhoto


from loader import vip
from data import cabinet_msg, Users, Deals
from filters import IsPrivate, IsBan
from keyboards import (
    default_button,
    cabinet_markup,
    garant_markup
)


@vip.message_handler(IsPrivate(), IsBan(), text=default_button[0])
async def default_handler(msg: Message):
    user = await Users().get(user_id=msg.from_user.id)
    if user.username != msg.from_user.username:
        await Users().updateUsername(
            user_id=msg.from_user.id,
            username=msg.from_user.username
        )
    await msg.answer_photo(
        photo='https://telegra.ph/file/c02319db76b95f2eab4de.png',
        reply_markup=garant_markup()
    )


@vip.message_handler(IsPrivate(), IsBan(), text=default_button[1])
async def profile_handler(msg: Message):
    user = await Users().get(user_id=msg.from_user.id)
    if user.username != msg.from_user.username:
        await Users().updateUsername(
            user_id=msg.from_user.id,
            username=msg.from_user.username
        )
    await msg.answer_photo(
        photo='https://telegra.ph/file/ba585ea63559091e3ac24.png',
        caption=cabinet_msg.format(
            user_id=msg.from_user.id,
            login=msg.from_user.get_mention(),
            data=str(user.date)[:10],
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
            rating=user.rating,
            balance=user.balance
        ),
        reply_markup=cabinet_markup()
    )

@vip.callback_query_handler(text="user-profile")
async def profile_handler_call(call: CallbackQuery):
    user = await Users().get(user_id=call.from_user.id)
    if user.username != call.from_user.username:
        await Users().updateUsername(
            user_id=call.from_user.id,
            username=call.from_user.username
        )
    await call.message.edit_media(
        InputMediaPhoto(
            media=('https://telegra.ph/file/ba585ea63559091e3ac24.png'),
            caption=cabinet_msg.format(
                user_id=call.from_user.id,
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
            )),
        reply_markup=cabinet_markup()
    )

