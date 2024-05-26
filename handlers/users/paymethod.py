from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.dispatcher import FSMContext

from loader import vip, bot
from data import Users, DepositLogs
from keyboards import payment_markup, return_markup
from states import CryptobotPay, PayokPay
from utils import Cryptobot, config, PayOk


@vip.callback_query_handler(text="user-payments")
async def payments_handler(call: CallbackQuery):
    await call.message.edit_media(
        InputMediaPhoto(
            media=('https://telegra.ph/file/81baeb7d21293bc7ea1b1.png'),
            caption="<b>Выберите способ пополнения:</b>",
        ),
        reply_markup=payment_markup()
    )



@vip.callback_query_handler(text="user-сrypto-pay")
async def crypto_handler(call: CallbackQuery):
    await CryptobotPay.amount.set()
    # async with state.proxy() as data:
    #     data["currency"] = call.data.split(":")[1]
    await call.message.edit_media(
        InputMediaPhoto(
            media=('https://telegra.ph/file/d9e386fd4c8d1cf593154.png'),
            caption="<b>Введите сумму пополнения в Рублях:</b>",
        ),
        # reply_markup=Cryptobot().getCurrencyMarkup()
    )


@vip.message_handler(state=CryptobotPay.amount)
async def cryptbot_handler(msg: Message, state: FSMContext):
    if msg.text.isdecimal():

        if float(msg.text) >= 50:
            invoice_id, invoice_url, amount = await Cryptobot().createInvoice(
                amount=float(msg.text)
            )

            await msg.answer_photo(
                photo='https://imgur.com/ohG9xyX',
                caption="<b>Для оплаты перейдите по ссылке ниже, затем нажмите '♻️ Проверить'.</b>",
                reply_markup=Cryptobot().geyCryptoPayMarkup(
                    invoice_url=invoice_url,
                    invoice_id=invoice_id,
                    amount=amount,
                )
            )
        else:
            msg.answer(
                text='Минимальная сумма пополнения 50 RUB'
            )

    else:
        await msg.answer_photo(
            photo='https://imgur.com/ohG9xyX',
            caption="<b>Нужно вводить число, а не поеботу!</b>",
            reply_markup=return_markup()
        )
    await bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id
    )
    await bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id - 1
    )
    await state.finish()


# @vip.callback_query_handler(text_startswith="crypto-pay-currency:")
# async def crypto_handler(call: CallbackQuery, state: FSMContext):
#     await CryptobotPay.amount.set()
#     async with state.proxy() as data:
#         data["currency"] = call.data.split(":")[1]
#
#     await call.message.edit_caption(
#         caption="<b>Введите сумму пополнения в долларах:</b>"
#     )


@vip.callback_query_handler(text_startswith="check-crypto-pay:")
async def check_crypto_handler(call: CallbackQuery):
    status = await Cryptobot().paidInvoice(
        invoice_id=call.data.split(":")[1].split(":")[0]
    )
    if status:
        amount = call.data.split(':')[2].split(':')[0]
        await DepositLogs.writeDepositLogs(
            user_id=call.from_user.id,
            types="CryptoBot",
            amount=amount
        )
        await bot.send_message(
            chat_id=config.config('admin_group'),
            text=f'<b>♻️ Пришло пополнение Сryptobot!</b>\n\n'
                 f'<b>🧑🏻‍🔧 От:</b> @{call.from_user.username} | {call.from_user.id}\n\n'
                 f'<b>💰 Сумма:</b> {call.data.split(":")[2]} RUB'
        )
        await call.message.edit_caption(
            caption=f"<b>♻️ Успешное пополнение баланса!\n\n"
                    f"🧑🏻‍🔧 Тип: Сryptobot\n\n"
                    f"💰 Сумма: {amount} RUB</b>",
            reply_markup=return_markup()
        )
        await Users.updateBalance(
            user_id=call.from_user.id,
            amount=amount
        )
    else:
        await call.answer(
            text="💢 Пополнение не найдено!"
        )





@vip.callback_query_handler(text="user-card-pay")
async def card_handler(call: CallbackQuery):
    await PayokPay.amount.set()
    await call.message.edit_caption(
        caption="<b>Введите сумму пополнения в рублях:</b>"
    )


@vip.callback_query_handler(text_startswith="check-card-pay:")
async def check_card_handler(call: CallbackQuery):
    status = await PayOk().checkTransaction(
        bill_id=call.data.split(":")[1].split(":")[0]
    )
    if status:
        amount = call.data.split(':')[2]
        await DepositLogs.writeDepositLogs(
            user_id=call.from_user.id,
            types="PayOk",
            amount=amount
        )
        await bot.send_message(
            chat_id=config.config('admin_group'),
            text=f'<b>♻️ Пришло пополнение PayOk!</b>\n\n'
                 f'<b>🧑🏻‍🔧 От:</b> @{call.from_user.username} | {call.from_user.id}\n\n'
                 f'<b>💰 Сумма:</b> {call.data.split(":")[2]} RUB'
        )
        await call.message.edit_caption(
            caption=f"<b>♻️ Успешное пополнение баланса!\n\n"
                    f"🧑🏻‍🔧 Тип: PayOk\n\n"
                    f"💰 Сумма: {amount} RUB</b>",
            reply_markup=return_markup()
        )
        await Users.updateBalance(
            user_id=call.from_user.id,
            amount=amount
        )
    else:
        await call.answer(
            text="💢 Пополнение не найдено!"
        )


@vip.message_handler(state=PayokPay.amount)
async def cryptbot_handler(msg: Message, state: FSMContext):

    if msg.text.isdecimal():
        invoice, pay_id = await PayOk().createInvoice(
            amount=msg.text
        )

        await msg.answer_photo(
            photo='https://imgur.com/ohG9xyX',
            caption="<b>Для оплаты перейдите по ссылке ниже, затем нажмите '♻️ Проверить'.</b>",
            reply_markup=PayOk().geyCardMarkup(
                invoice_id=pay_id,
                invoice_url=invoice,
                amount=msg.text
            )
        )
    else:
        await msg.answer_photo(
            photo='https://imgur.com/ohG9xyX',
            caption="<b>Нужно вводить число, а не поеботу!</b>",
            reply_markup=return_markup()
        )
    await bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id
    )
    await bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id - 1
    )
    await state.finish()
