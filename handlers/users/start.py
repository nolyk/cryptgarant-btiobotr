from aiogram.types import Message, CallbackQuery

from data import (
    Users,
    ChannelSub,
    start_msg, DepositLogs
)
from filters import IsPrivate
from keyboards import default_markup
from loader import bot, vip
from utils import config


@vip.message_handler(IsPrivate(), commands=['start'])
async def start_handler(msg: Message):
    status, who_invite = await Users().joinFromBot(
        user_id=msg.from_user.id,
        username=msg.from_user.username.lower(),
        who_invite=msg.text[7:]
    )
    if status:
        await bot.send_message(
            chat_id=config.config("admin_group"),
            text=f"<b>Новый пользователь: {msg.from_user.get_mention()} | {msg.from_user.id}</b>\n"
        )
        if who_invite:
            await bot.send_message(
                chat_id=msg.text[7:],
                text=f'<b>У вас новый реферал: {msg.from_user.get_mention()}</b>'
            )

    subscriber = await ChannelSub.checkSubsChannels(
        bot=bot,
        user_id=msg.from_user.id
    )
    if not subscriber:
        markup = await ChannelSub.getChannelMarkup(who=msg.text[7:])
        if markup:
            await msg.answer(
                text='<b>Чтобы пользоваться ботом, подпишись на наши каналы:</b>',
                reply_markup=markup
            )

    else:
        await msg.answer(
            text=start_msg,
            reply_markup=default_markup(),
            disable_web_page_preview=True
        )


@vip.callback_query_handler(text_startswith='check-subscribes-channels:')
async def channels_handler(call: CallbackQuery):
    subscriber = await ChannelSub.checkSubsChannels(
        bot=bot,
        user_id=call.from_user.id
    )

    if subscriber:
        await call.message.delete()

        status, who_invite = await Users().joinFromBot(
            user_id=call.from_user.id,
            username=call.from_user.username,
            who_invite=call.data.split(":")[1]
        )
        if status:
            await bot.send_message(
                chat_id=config.config("admin_group"),
                text=f"<b>Новый пользователь: {call.from_user.get_mention()} | {call.from_user.id}</b>\n"

            )
            await call.message.answer(
                text=start_msg,
                reply_markup=default_markup(),
                disable_web_page_preview=True
            )

            if who_invite:
                await bot.send_message(
                    chat_id=call.data.split(":")[1],
                    text=f'<b>У вас новый реферал: {call.from_user.get_mention()}</b>'
                )

        else:
            await call.message.answer(
                text="<b>Успешная подписка на каналы!</b>",
                reply_markup=default_markup()
            )
    else:
        await call.message.answer(
            text='Вы подписаны не на все каналы, подпишитесь!',
        )
