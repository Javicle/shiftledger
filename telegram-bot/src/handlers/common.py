from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from src.messages import send_welcome_text
from src.ui.keyboards import main_menu
from src.utils import (
    validate_message,
    validate_user_from_message,
    validate_username_from_user,
)

common_router = Router()


@common_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Handle /start command"""
    _user = await validate_user_from_message(message)
    _username = await validate_username_from_user(_user)

    mess = await validate_message(message)
    await send_welcome_text(new_user=False, message=mess)


@common_router.message()
async def fallback(message: Message) -> None:
    """Handle other message"""
    _user = await validate_user_from_message(message)
    _username = await validate_username_from_user(_user)

    mess = await validate_message(message)
    await send_welcome_text(mess, False)
