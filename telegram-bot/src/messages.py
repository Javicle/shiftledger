"""Module for sending messages to user"""

# ruff: noqa: E501, B018
# pyright: reportUnusedCallResult=false

import logging

from aiogram.types import CallbackQuery, Message

from src.ui.keyboards import main_menu
from src.utils import (
    validate_message,
    validate_user_from_message,
    validate_username_from_user,
)

logger = logging.getLogger(__name__)


async def send_welcome_text(message: Message, new_user: bool) -> None:
    """Sends a welcome message to the user."""

    mess = await validate_message(message)
    _user = await validate_user_from_message(mess)
    _username = await validate_username_from_user(_user)
    if new_user:
        text = (
            '👋 Привет! Добро пожаловать в ShiftLedger — систему учёта продаж и долгов.\n\n'
            'Здесь ты можешь быстро добавлять отчёты за смену и фиксировать поставки от начальника.'
        )
    else:
        text = f'👋 С возвращением, @{_username}!\n\n'
        'ShiftLedger готов к работе. Выбери действие ниже:'

    await mess.answer(text, reply_markup=main_menu())


async def show_main_menu(callback: CallbackQuery) -> None:
    """Shows the main menu to the user."""

    mes = await validate_message(callback.message)
    username = callback.from_user.username or callback.from_user.first_name
    text = f'👋 С возвращением, @{username}!\n\nShiftLedger готов к работе. Выбери действие ниже:'

    await mes.edit_text(text=text, reply_markup=main_menu())
    await callback.answer()
