from typing import Tuple, Union
from loguru import logger

from . import models


class Users(models.User):

    @classmethod
    async def checkingUsername(
            cls,
            username: str
    ) -> Union[list, bool]:
        """
        Проверяем есть ли такой юзернейм в базе
        :param username: str
        :return: list or bool
        """
        user = await cls.exists(username=username)
        return user

    @classmethod
    async def updateUsername(
            cls,
            user_id: int,
            username: str
    ) -> None:
        """
        Обновляем юзернейм пользователя
        :param user_id: int, user id
        :param username: str
        :return:
        """
        user = await cls.get(user_id=user_id)
        user.username = username
        await user.save()

    @classmethod
    async def updateBanStatus(
            cls,
            user_id: int,
            status: bool
    ) -> None:
        """
        Обновление статуса бана
        :param user_id: int
        :param status: False or True
        :return: None
        """
        user = await cls.get(user_id=user_id)
        user.ban = status
        await user.save()

    @classmethod
    async def updateStatus(
            cls,
            status: str
    ) -> None:
        """
        Обновляем статус пользователя
        :param status: str, default Active
        :return: None
        """
        user = await cls.get(user_id=cls.user_id)
        user.status = status
        await user.save()

    @classmethod
    async def updateBalance(
            cls,
            user_id: int,
            amount: Union[float, int]
    ) -> None:
        """
        Обновление баланса пользователя
        :param user_id: int
        :param amount: float
        :return: None
        """
        print(f"Пополнение баланса на {amount}")
        user = await cls.get(user_id=user_id)
        user.balance += float(amount)
        await user.save()

    @classmethod
    async def updateBalanceNull(
            cls,
            user_id: int,
            amount: Union[float, int]
    ) -> None:
        """
        Обновление баланса на нужное значение
        :param user_id: int
        :param amount: float or int
        :return: None
        """
        user = await cls.get(user_id=user_id)
        user.balance = amount
        await user.save()

    @classmethod
    async def updateRate(
            cls,
            user_id: int,
            rate: int = 1
    ) -> None:
        """
        Обновление рейтинга пользователя
        :param user_id: int
        :param rate: int
        :return: None
        """
        user = await cls.get(user_id=user_id)
        user.rating += rate
        await user.save()

    @classmethod
    async def updateCountDeals(
            cls,
            user_id: int,
            count: int = 1
    ) -> None:
        """
        Обновление количества сделок пользователя
        :param user_id: int
        :param count: int, default 1
        :return: None
        """
        user = await cls.get(user_id=user_id)
        user.deals += count
        await user.save()

    @classmethod
    async def checkFromBase(
            cls,
            user_id: int
    ):
        user = await cls.exists(user_id=user_id)
        return user

    @classmethod
    async def joinFromBot(
            cls,
            user_id: int,
            username: str,
            who_invite: str) -> Tuple[bool, int]:
        """
        Проверка и запись пользователя в
        базу данных
        :param user_id: int
        :param username: str
        :param who_invite: str
        :return: Tuple[bool, int]
        """
        invite, status = False, False
        if who_invite != "":
            who = await cls.exists(user_id=who_invite)
            invite = True if who else False

        select = await cls.checkFromBase(
            user_id=user_id
        )
        if not select:
            logger.info(
                f"Запись нового пользователя: {user_id} | {username} " + ""
                if not invite else f"| Пригласил: {who_invite}")
            status = True
            await Users(
                user_id=user_id,
                username=username,
                who_invite=who_invite if invite else 0

            ).save()

        return status, invite
