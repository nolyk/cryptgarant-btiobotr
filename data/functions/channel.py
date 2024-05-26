# © copyright by VoX DoX
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Union, Tuple, List

from . import models


class ChannelSub(models.Channels):
    status = [
        'administrator', 'creator', 'member'
    ]

    @classmethod
    async def writeNewChannel(cls,
                              channel_id: str,
                              name: str,
                              link: str) -> bool:
        """
        Запись нового канала в базу данных
        :param channel_id: str
        :param name: str
        :param link: str
        :return: bool
        """
        await ChannelSub(
            channel_id=channel_id,
            channel_name=name,
            link=link
        ).save()

        return True

    @classmethod
    async def deleteChannel(cls,
                            channel_id: str) -> None:
        """
        Удаление канала из базы данных
        :param channel_id: str
        :return: None
        """
        channel = await cls.get(channel_id=channel_id)
        await channel.delete()

    @classmethod
    async def getChannels(cls) -> Union[List[models.Channels], bool]:
        """
        Возвращает все каналы из базы данных
        :return: Union[list, bool]
        """
        channels = await ChannelSub.all()
        if len(channels) == 0:
            return False

        return channels

    @classmethod
    async def getChannelMarkup(cls, who: int) -> Union[InlineKeyboardMarkup, bool]:
        channels = await cls.getChannels()
        if channels:
            markup = InlineKeyboardMarkup(row_width=1)

            x1 = 0
            for i in range(len(channels)):
                try:
                    markup.add(
                        InlineKeyboardButton(
                            text=channels[x1].channel_name, url=channels[x1].link)
                    )
                    x1 += 1
                except IndexError:
                    break
            markup.add(
                InlineKeyboardButton(
                    text='✅Я вступил', callback_data=f'check-subscribes-channels:{who}')
            )

            return markup

        return False

    @classmethod
    async def checkSubsChannels(cls,
                                bot,
                                user_id: int) -> bool:
        channels = await cls.getChannels()
        if channels:

            not_sub = []
            for channel in channels:
                subscribers = await bot.get_chat_member(
                    chat_id=channel.channel_id,
                    user_id=user_id
                )
                if subscribers.status not in cls.status:
                    not_sub.append(channel.channel_id)

            status = False
            if len(not_sub) == 0:
                status = True
        else:
            status = True

        return status

    @classmethod
    async def getAdminChannelMarkup(cls) -> Tuple[InlineKeyboardMarkup, bool]:
        channels = await cls.getChannels()
        markup = InlineKeyboardMarkup(row_width=1)

        status = False
        if channels:

            x1 = 0
            for i in range(len(channels)):
                try:
                    markup.add(
                        InlineKeyboardButton(
                            text=channels[x1].channel_name,
                            callback_data=f'admin-channel-info:{channels[x1].channel_id}')
                    )
                    x1 += 1
                except IndexError:
                    break

            status = True

        markup.add(
            InlineKeyboardButton(
                text='Добавить канал', callback_data=f'append-new-channel')
            )

        return markup, status
