from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_keyboard: list[list[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(
            text='Создать отчет', callback_data='create_report'
        ),
        InlineKeyboardButton(
            text='Создать поставку', callback_data='create_supply'
        ),
        InlineKeyboardButton(
            text='История Отчетов', callback_data='history_peports'
        ),
        InlineKeyboardButton(
            text='История поставок', callback_data='histry_supplyes'
        ),
    ]
]


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
