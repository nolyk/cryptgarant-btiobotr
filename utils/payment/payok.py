from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiopayok import Payok
from aiohttp import ClientSession
from random import randint
from typing import Tuple
import ssl
import certifi

from utils import config


class PayOk:
    def __init__(self):
        self._PAY_ID_ = config.config("payok_id")
        self._API_KEY_ = config.config("payok_api")
        self._SHOP_ID_ = 12110
        self._SECRET_KEY_: str = "1f871de722c231b8f8bd79f481bf1426"
        self._PAYOK_ = Payok(
            api_id=self._PAY_ID_,
            api_key=self._API_KEY_,
            secret_key=self._SECRET_KEY_,
            shop=self._SHOP_ID_
        )
        self._DESC: str = "Пополнение @CryptoGarantsBot"
        self._CURRENCY = "RUB"

    async def createInvoice(self,
                            amount: float) -> Tuple[str, int]:
        """
        Получение инвойса на оплату
        :param amount: float
        :return:
        """
        pay_id: int = randint(111111, 999999)
        payok = await self._PAYOK_.create_pay(
            payment=pay_id,
            amount=amount,
            currency=self._CURRENCY,
            desc=self._DESC
        )

        return payok, pay_id

    async def checkTransaction(self,
                               bill_id: int):
        """
        Проверка транзы на оплату
        :param bill_id: int
        :return:
        """
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with ClientSession() as session:
            request_params = {
                'API_ID': self._PAY_ID_,
                'API_KEY': self._API_KEY_,
                'shop': self._SHOP_ID_
            }
            async with session.post(url='https://payok.io/api/transaction',
                                    data=request_params, ssl_context=ssl_context) as response:
                resp = await response.json(content_type=None)
                x1 = 1
                for index in list(resp):
                    if index != "status":
                        print(resp[index])

                        # if resp[f"{index}"]['payment_id'] == bill_id:
                        #     print(index)
                        #     if int(resp[f"{index}"]['transaction_status']) == 1:
                        #         return True
            return False

    @staticmethod
    def geyCardMarkup(invoice_url: str,
                      invoice_id: int,
                      amount: float) -> InlineKeyboardMarkup:
        """
        Инлайн-клава на оплату и проверку пополнения
        :param invoice_url: str
        :param invoice_id: int
        :param amount: float
        :return: InlineKeyboardMarkup
        """
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='Оплатить', url=invoice_url
                    ),
                    InlineKeyboardButton(
                        text='♻️ Проверить', callback_data=f'check-card-pay:{invoice_id}:{amount}'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='« Вернуться назад', callback_data='return-menu:cabinet'
                    )
                ]
            ]
        )
        return markup
