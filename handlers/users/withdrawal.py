from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import vip, bot
from data import Users, Withdrawal
from keyboards import return_markup, withdrawal_markup
from states import UserWithdrawal, CryptobotWithdrawal
from utils import config


@vip.callback_query_handler(text="user-withdrawal")
async def withdrawal_handler(call: CallbackQuery):
    await call.message.edit_caption(
        caption="<b>Выберите куда вам вывести:</b>",
        reply_markup=withdrawal_markup()
    )


@vip.callback_query_handler(text='user-withdrawal-card')
async def card_handler(call: CallbackQuery):
    await UserWithdrawal.amount.set()
    await call.message.edit_caption(
        caption="<b>Введите сумму вывода:</b>"
    )


@vip.callback_query_handler(text='user-withdrawal-crypto')
async def card_handler(call: CallbackQuery):
    await CryptobotWithdrawal.amount.set()
    await call.message.edit_caption(
        caption="<b>Введите сумму вывода:</b>"
    )


@vip.message_handler(state=CryptobotWithdrawal.amount)
async def crypto_amount_handler(msg: Message, state: FSMContext):
    amount = msg.text
    user = await Users.get(user_id=msg.from_user.id)

    await bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id - 1
    )
    await bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id
    )

    try:
        if float(user.balance) >= float(amount) > 0:
            await state.update_data(amount=amount)

            await msg.answer(
                text=f"<b>Отправить заявку на вывод?\n\n"
                     f"Тип: Cryptobot\n"
                     f"Сумма: {amount} RUB\n\n"
                     f"Для подтверждения вывода введите '+'</b>"
            )


            return await CryptobotWithdrawal.next()
        else:
            return await msg.answer(
                text="<b>Сумма вывода превышает ваш баланс!</b>"
            )

    except ValueError:
        return await msg.answer(
            text="<b>Сумма должна состоять из числа</b>"
        )


@vip.message_handler(state=CryptobotWithdrawal.confirm)
async def crypto_confirm_handler(msg: Message, state: FSMContext):
    if msg.text.startswith("+"):
        data = await state.get_data()
        amount = data['amount']

        await Users.updateBalance(
            user_id=msg.from_user.id,
            amount=-float(amount)
        )
        await Withdrawal.writeWithdrawal(
            user_id=msg.from_user.id,
            wallet="Cryptobot",
            amount=amount
        )
        amount = float(amount) - (float(amount) / 100 * int(config.config("com_witch")))

        await bot.delete_message(
            chat_id=msg.from_user.id,
            message_id=msg.message_id - 1
        )
        await bot.delete_message(
            chat_id=msg.from_user.id,
            message_id=msg.message_id
        )

        await msg.answer_photo(
            photo="https://imgur.com/ohG9xyX",
            caption=f"<b>Заявка отправлена!\n\n"
                    f"Тип: Cryptobot\n"
                    f"Сумма: {amount} RUB (с учетом комиссии)\n\n"
                    f"Ожидайте уведомление об начале вывода средств</b>",
            reply_markup=return_markup()
        )
        await bot.send_message(
            chat_id=config.config("admin_group"),
            text=f'<b>♻️ Заявка на вывод!</b>\n\n'
                 f'<b>🧑🏻‍🔧 От:</b> @{msg.from_user.username} | {msg.from_user.id}\n\n'
                 f'<b>🪪 Реквизиты:</b> Cryptobt\n\n'
                 f'<b>💰 Сумма:</b> {amount} RUB (с учетом комиссии)'
        )
    else:
        await msg.answer(
            text="<b>Заявка на вывод отменена!</b>"
        )
    await state.finish()


@vip.message_handler(state=UserWithdrawal.amount)
async def with_amount_handler(msg: Message, state: FSMContext):
    amount = msg.text

    user = await Users.get(user_id=msg.from_user.id)
    try:
        if float(user.balance) >= float(amount) > 0 and float(amount) >= int(config.config("min_witch")):
            async with state.proxy() as data:
                data['amount'] = amount

            await msg.answer(
                text="<b>Введите реквизиты для вывода (qiwi\card)</b>"
            )

            await bot.delete_message(
                chat_id=msg.from_user.id,
                message_id=msg.message_id - 1
            )
            await bot.delete_message(
                chat_id=msg.from_user.id,
                message_id=msg.message_id
            )
            await UserWithdrawal.next()
        else:
            await msg.answer(
                text="<b>Сумма вывода превышает ваш баланс!</b>"
            )
            await state.finish()
    except ValueError:
        await msg.answer(
            text="<b>Вводить надо целое число или с плавающей точкой</b>"
        )
        await state.finish()


@vip.message_handler(state=UserWithdrawal.wallet)
async def with_wallet_handler(msg: Message, state: FSMContext):
    wallet = msg.text

    async with state.proxy() as data:
        data['wallet'] = wallet
        amount = data['amount']

    await bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id - 1
    )
    await bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id
    )
    await msg.answer(
        text=f"<b>Отправить заявку на вывод?\n\n"
             f"Реквизиты: {wallet}\n"
             f"Сумма: {amount} RUB (с учетом комиссии)\n\n"
             f"Для подтверждения вывода введите '+'</b>"
    )
    await UserWithdrawal.next()


@vip.message_handler(state=UserWithdrawal.confirm)
async def with_confirm_handler(msg: Message, state: FSMContext):
    if msg.text.startswith("+"):

        async with state.proxy() as data:
            wallet = data['wallet']
            amount = data['amount']

        await Users.updateBalance(
            user_id=msg.from_user.id,
            amount=-float(amount)
        )
        await Withdrawal.writeWithdrawal(
            user_id=msg.from_user.id,
            wallet=wallet,
            amount=amount
        )
        await bot.delete_message(
            chat_id=msg.from_user.id,
            message_id=msg.message_id - 1
        )
        await bot.delete_message(
            chat_id=msg.from_user.id,
            message_id=msg.message_id
        )
        amount = float(amount) - (float(amount) / 100 * int(config.config("com_witch")))
        await msg.answer_photo(
            photo="https://imgur.com/ohG9xyX",
            caption=f"<b>Заявка отправлена!\n\n"
                    f"Реквизиты: {wallet}\n"
                    f"Сумма: {amount} RUB (с учетом комиссии)\n\n"
                    f"Ожидайте уведомление об начале вывода средств</b>",
            reply_markup=return_markup()
        )
        await bot.send_message(
            chat_id=config.config("admin_group"),
            text=f'<b>♻️ Заявка на вывод!</b>\n\n'
                 f'<b>🧑🏻‍🔧 От:</b> @{msg.from_user.username} | {msg.from_user.id}\n\n'
                 f'<b>🪪 Реквизиты:</b> {wallet}\n\n'
                 f'<b>💰 Сумма:</b> {amount} RUB (с учетом комиссии)'
        )
    else:
        await msg.answer(
            text="<b>Заявка на вывод отменена!</b>"
        )
    await state.finish()
