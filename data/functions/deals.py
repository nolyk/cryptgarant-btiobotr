# © copyright by VoX DoX
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Union, List

from . import Users, models


class Deals(models.Deal):

    @classmethod
    async def writeNewDeal(
            cls,
            user_create: int,
            user_invite: int,
            amount: float,
            description: str
    ) -> int:
        """
        Запись новой сделки
        :param user_create: int
        :param user_invite: int
        :param amount: float
        :param description: str
        :return: int
        """
        deal = await Deals(
            buyer_id=user_create,
            seller_id=user_invite,
            amount=amount,
            description=description
        )
        await deal.save()

        return deal.id

    @classmethod
    async def getCountUserDeals(
            cls,
            user_id: int,
            status: str = "ALL"
    ) -> int:
        """
        Получаем количество сделок пользователя
        :param user_id: int
        :param status: str
        :return: int
        """
        if status == "ALL":
            buyer = await cls.filter(buyer_id=user_id).count()
            seller = await cls.filter(seller_id=user_id).count()
        else:
            buyer = await cls.filter(buyer_id=user_id, status=status).count()
            seller = await cls.filter(seller_id=user_id, status=status).count()

        count = buyer + seller

        return count

    @classmethod
    async def updateStatus(
            cls,
            dl_id: int,
            status: str) -> None:
        """
        Обновление статуса сделки
        :param dl_id: int
        :param status: str
        :return: None
        """
        deal = await cls.get(id=dl_id)
        deal.status = status
        await deal.save()

    @classmethod
    async def getDealsFromStatus(
            cls,
            status: str = "Арбитраж"
    ) -> Union[List[models.Deal], bool]:
        """
        Возвращает все арбитраж сделки
        :param status: str
        :return: Union[list, bool]
        """
        deals = await cls.filter(status=status)

        if len(deals) == 0:
            deals = False

        return deals

    @classmethod
    async def getUserDeal(
            cls,
            user_id: int,
            _type: str
    ) -> Union[List[models.Deal], bool]:
        """
        Возвращает все сделки юзера из базы данных
        :param _type: str
        :param user_id: int
        :return: Union[list, bool]
        """
        if _type == "buyer":
            deals = await cls.filter(buyer_id=user_id)
        else:
            deals = await cls.filter(seller_id=user_id)

        if len(deals) > 0:
            return deals

        return False

    @classmethod
    async def getUserDealsMarkup(cls,
                                 _type: str,
                                 user_id: int) -> Union[InlineKeyboardMarkup, bool]:
        """
        Возвращает все сделки юзера ввиде инлайн-клавы
        :param _type:
        :param user_id:
        :return: Union[InlineKeyboardMarkup, bool]
        """
        data = await cls.getUserDeal(
            _type=_type, user_id=user_id
        )
        if data:
            markup = InlineKeyboardMarkup(row_width=1)

            for i in data:
                emoji = "✅" if i.status == "Оплачена" else "♻️" if i.status != "Закрыта" else "💢"
                markup.add(
                    InlineKeyboardButton(
                        text=f'{emoji if i.status != "Арбитраж" else "👨‍⚖️"} Сделка:  #CB_{i.id} | {i.amount} ₽',
                        callback_data=f'view-deal:{i.id}')
                )

            markup.add(
                InlineKeyboardButton(
                    text="« Вернуться назад", callback_data='return-menu:default')
            )

            return markup

        return False

    @classmethod
    async def getActiveDealsMarkup(cls,
                                   page_number: int = 1) -> Union[InlineKeyboardMarkup, bool]:
        """
        Инлайн клава с кнопочками под арбитражи
        :param page_number: int
        :return: Union[InlineKeyboardMarkup, bool]
        """
        data = await cls.getDealsFromStatus(status="Оплачена")

        markup = InlineKeyboardMarkup(row_width=2)
        if data:
            size = 8
            page = []
            pages = []

            for withdrawal in data:
                page.append(withdrawal)
                if len(page) == size:
                    pages.append(page)
                    page = []

            if str(len(data) / size) not in range(16):
                pages.append(page)

            x1: int = 0
            for i in range(int(len(pages[page_number - 1]))):
                markup.add(
                    InlineKeyboardButton(
                        text=f"🤝 #CG_{pages[page_number - 1][x1].id} | {pages[page_number - 1][x1].amount} RUB",
                        callback_data=f"admin-active-deal:{pages[page_number - 1][x1].id}")
                )
                x1 += 1

            if len(pages) > 1 and 0 < len(pages[1]):
                previous_page_number = page_number + 1 if page_number == 1 else page_number - 1
                next_page_number = page_number + 1 if len(pages) > page_number else page_number
                if page_number == len(pages):
                    previous_page_number = previous_page_number
                    next_page_number = 1

                markup.add(
                    InlineKeyboardButton(
                        text='ᐊ', callback_data=f'active-deal-page:{previous_page_number}'
                    ),
                    InlineKeyboardButton(
                        text='ᐅ', callback_data=f'active-deal-page:{next_page_number}'
                    ),
                    InlineKeyboardButton(
                        text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'
                    ),
                )

            markup.add(
                InlineKeyboardButton(
                    text='🔙 Закрыть', callback_data=f'close-message')
            )

            return markup

        return False

    @classmethod
    async def getArbitrationDealsMarkup(cls,
                                        page_number: int = 1) -> Union[InlineKeyboardMarkup, bool]:
        """
        Инлайн клава с кнопочками под арбитражи
        :param page_number: int
        :return: Union[InlineKeyboardMarkup, bool]
        """
        data = await cls.getDealsFromStatus()

        markup = InlineKeyboardMarkup(row_width=2)
        if data:
            size = 8
            page = []
            pages = []

            for withdrawal in data:
                page.append(withdrawal)
                if len(page) == size:
                    pages.append(page)
                    page = []

            if str(len(data) / size) not in range(16):
                pages.append(page)

            x1: int = 0
            for i in range(int(len(pages[page_number - 1]))):
                markup.add(
                    InlineKeyboardButton(
                        text=f"👨🏻‍⚖️ #CG_{pages[page_number - 1][x1].id} | {pages[page_number - 1][x1].amount} RUB",
                        callback_data=f"admin-arb-deal:{pages[page_number - 1][x1].id}")
                )
                x1 += 1

            if len(pages) > 1 and 0 < len(pages[1]):
                previous_page_number = page_number + 1 if page_number == 1 else page_number - 1
                next_page_number = page_number + 1 if len(pages) > page_number else page_number
                if page_number == len(pages):
                    previous_page_number = previous_page_number
                    next_page_number = 1

                markup.add(
                    InlineKeyboardButton(
                        text='ᐊ', callback_data=f'arbitration-page:{previous_page_number}'
                    ),
                    InlineKeyboardButton(
                        text='ᐅ', callback_data=f'arbitration-page:{next_page_number}'
                    ),
                    InlineKeyboardButton(
                        text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'
                    ),
                )

            markup.add(
                InlineKeyboardButton(
                    text='🔙 Закрыть', callback_data=f'close-message')
            )

            return markup

        return False


class Reviews(models.Review):

    @classmethod
    async def writeNewReview(cls,
                             seller: int,
                             buyer: int,
                             review: str) -> None:
        """
        Запись нового отзыва в базу данных
        :param seller: int
        :param buyer: int
        :param review: str
        :return: None
        """
        deal = await Reviews(
            buyer_id=buyer,
            seller_id=seller,
            review=review
        )
        await deal.save()

    @classmethod
    async def getUserReview(cls,
                            user_id: int) -> Union[List[models.Review], bool]:
        """
        Возвращает все арбитраж сделки
        :return: Union[list, bool]
        """
        reviews = await cls.filter(seller_id=user_id)
        if len(reviews) > 0:
            return reviews

        return False

    @classmethod
    async def getUserReviewMarkup(cls,
                                  user_id: int,
                                  page_number: int = 1) -> Union[InlineKeyboardMarkup, bool]:
        """
        Инлайн клава с кнопочками отзывов
        :param user_id: int
        :param page_number: int
        :return: Union[InlineKeyboardMarkup, bool]
        """
        data = await cls.getUserReview(
            user_id=user_id
        )

        markup = InlineKeyboardMarkup(row_width=2)
        if data:
            size = 8
            page = []
            pages = []

            for withdrawal in data:
                page.append(withdrawal)
                if len(page) == size:
                    pages.append(page)
                    page = []

            if str(len(data) / size) not in range(16):
                pages.append(page)

            x1: int = 0
            for i in range(int(len(pages[page_number - 1]))):
                user = await Users.get(user_id=pages[page_number - 1][x1].buyer_id)
                markup.add(
                    InlineKeyboardButton(
                        text=f"🔖️ #R_{pages[page_number - 1][x1].id} | От @{user.username}",
                        callback_data=f"user-review-deal:{pages[page_number - 1][x1].id}")
                )
                x1 += 1

            if len(pages) > 1 and 0 < len(pages[1]):
                previous_page_number = page_number + 1 if page_number == 1 else page_number - 1
                next_page_number = page_number + 1 if len(pages) > page_number else page_number
                if page_number == len(pages):
                    previous_page_number = previous_page_number
                    next_page_number = 1

                markup.add(
                    InlineKeyboardButton(
                        text='ᐊ', callback_data=f'review-page:{user_id}:{previous_page_number}'
                    ),
                    InlineKeyboardButton(
                        text='ᐅ', callback_data=f'review-page:{user_id}:{next_page_number}'
                    ),
                    InlineKeyboardButton(
                        text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'
                    ),
                )

            markup.add(
                InlineKeyboardButton(
                    text='🔙 Закрыть', callback_data=f'close-message')
            )

            return markup

        return False
