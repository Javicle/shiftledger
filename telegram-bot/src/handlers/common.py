from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from src.messages import send_welcome_text
from src.utils import (
    validate_message,
    validate_username_from_user,
)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Handle /start command"""
    _user = await validate_user_from_message(message)
    _username = await validate_username_from_user(_user)

    logger.info(
        "command_start: user_id=%s, username='%s'",
        _user.id,
        _username,
    )

    await validate_message(message)
    user_in_db = await exists_user_database(_user.id)

    await send_welcome_text(message=message, new_user=not user_in_db)

    try:
        await add_user(telegram_id=_user.id, username=_username)
    except UserAlreadyExistsError:
        logger.debug('User already exists: user_id=%s', _user.id)
    except DatabaseError as exc:
        logger.error(
            'Database error while adding user: %s', exc, exc_info=True
        )
        await message.answer(i18n.message('error_generic'))
