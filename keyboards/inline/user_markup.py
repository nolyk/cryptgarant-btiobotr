from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import config


def garant_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='🤝 Провести сделку 🛡', callback_data='user-search-deal'),
			],
			[
				InlineKeyboardButton(text='📑 Мои сделки', callback_data='user-deals'),
				InlineKeyboardButton(text='📇 Профиль', callback_data='user-profile'),
			],
			[
				InlineKeyboardButton(text='🔗 Рефералка ', callback_data='user-parners'),
				InlineKeyboardButton(text='🚫 Black List', callback_data='user-blacklist'),
			],
			[
				InlineKeyboardButton(text='📖 Информация ℹ️', callback_data='user-information'),
			],
		]
	)

	return markup


def blacklist_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='🚫Внести скамера', callback_data='blacklist-write'),
			],
			[
				InlineKeyboardButton(text='🔎 Проверить', callback_data='blacklist-checker'),
				InlineKeyboardButton(text='📋 Список скамеров', callback_data='blacklist-list'),
			],
			[
				InlineKeyboardButton(
					text="« Вернуться назад", callback_data='return-menu:default')
			],
		]
	)

	return markup


def return_black_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text="« Вернуться назад", callback_data='return-menu:black')
			],
		]
	)

	return markup


def information_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[

			[
				InlineKeyboardButton(
					text="« Вернуться назад", callback_data='return-menu:default')
			],
		]
	)

	return markup


def partners_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text='📣 End Soft', url='https://t.me/End_Soft'),
				InlineKeyboardButton(
					text='🕹 Форум', url='https://endway.su'),
			],
			[
				InlineKeyboardButton(
					text='🌡 EW Житуха | Общение', url='https://t.me/+PfUvAksMqb05NDdi'),
				InlineKeyboardButton(
					text='🧪 End Way Chat', url='https://t.me/End_Groups'),
			],
			[
				InlineKeyboardButton(
					text="« Вернуться назад", callback_data='return-menu:default')
			],
		]
	)

	return markup


def cabinet_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='➕Пополнить', callback_data='user-payments'),
				InlineKeyboardButton(text='⚡️Вывести', callback_data='user-withdrawal'),
			],
			[
				InlineKeyboardButton(
					text="« Вернуться назад", callback_data='return-menu:default')
			],
		]
	)

	return markup


def withdrawal_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='🤖 CryptoBot', callback_data='user-withdrawal-crypto')
			],
			# [
			# 	InlineKeyboardButton(text='💳 Карта/Qiwi/Yoomoney', callback_data='user-withdrawal-card'),
			# ],
			[
				InlineKeyboardButton(
					text="« Вернуться назад", callback_data='return-menu:cabinet')
			],
		]
	)

	return markup


def payment_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='🤖 CryptoBot', callback_data='user-сrypto-pay'),
				InlineKeyboardButton(text='💳 PayOK', callback_data='user-card-pay')
			],
			[
				InlineKeyboardButton(text='« Вернуться назад', callback_data='return-menu:cabinet'),
			]
		]
	)

	return markup


def return_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text="« Вернуться назад", callback_data='return-menu:default')
			],
		]
	)

	return markup


def deals_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(
					text='📈 Как покупатель', callback_data='user-deals:buyer'),
				InlineKeyboardButton(
					text='📉 Как продавец', callback_data='user-deals:seller'),
			],
			[
				InlineKeyboardButton(
					text="« Вернуться назад", callback_data='return-menu:default')
			]
		]
	)

	return markup


def accept_deal_markup(deal_id: int):
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='✅ Согласиться на сделку', callback_data=f'accept-deal:{deal_id}'),
			],
			[
				InlineKeyboardButton(text='❌ Отказаться от сделки', callback_data=f'refurse-deal:{deal_id}'),
			]
		]
	)

	return markup


def pay_deal_markup(deal_id: int):
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='✅ Оплатить сделку', callback_data=f'pay-deal:{deal_id}'),
			],
			[
				InlineKeyboardButton(text='❌ Отменить сделку', callback_data=f'refurse-deal:{deal_id}'),
			]
		]
	)

	return markup


def conditions_deal_markup(deal_id: int):
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='✅ Условия выполнены', callback_data=f'conditions-deal:{deal_id}'),
			],
			[
				InlineKeyboardButton(text='♻️ Возврат средств', callback_data=f'refund-deal:{deal_id}'),
			]
		]
	)

	return markup


def finish_deal_markup(deal_id: int):
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='💸 Отправить деньги продавцу', callback_data=f'finish-deal-sell:{deal_id}'),
			],
			[
				InlineKeyboardButton(text='🧑‍⚖️ Открыть арбитраж', callback_data=f'arbitration-deal:{deal_id}'),
			]
		]
	)

	return markup


def finish_seller_markup(deal_id: int):
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='🧑‍⚖️ Открыть арбитраж', callback_data=f'arbitration-deal:{deal_id}'),
			]
		]
	)

	return markup


def arbitrator_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='🧑‍⚖️ Написать Арбитру', url=config.config("arbitr_link")),
			]
		]
	)

	return markup


def rating_markup(user_id: int):
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='👍', callback_data=f'user-rating-plus:{user_id}'),
				InlineKeyboardButton(text='👎', callback_data=f'user-rating-minus:{user_id}'),
			]
		]
	)

	return markup


def open_deal_markup(user_id: int):
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='🌀 Открыть сделку', callback_data=f'user-open-deal:{user_id}'),
			],
			[
				InlineKeyboardButton(text='🔖 Посмотреть отзывы', callback_data=f'user-reviews:{user_id}'),
			]
		]
	)

	return markup


def info_deal_markup(user_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='🔖 Посмотреть отзывы', callback_data=f'user-reviews:{user_id}'),
			]
		]
	)

	return markup


def view_markup(user_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text='💈 Написать отзыв', callback_data=f'deal-add-views:{user_id}'),
			],
			[
				InlineKeyboardButton(text='❌ Отказаться', callback_data=f'close-message'),
			]
		]
	)

	return markup
