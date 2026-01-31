"""utils.py - module with auxiliary tools"""

from logging import getLogger

from aiogram.types import InaccessibleMessage, Message, User
from aiogram.types.maybe_inaccessible_message_union import (
    MaybeInaccessibleMessageUnion,
)
from exc import FakeUser, MessageNotFound, UserNotFound

logger = getLogger(__name__)


async def validate_message(
    message: MaybeInaccessibleMessageUnion | None,
) -> Message:
    """Validate user from message"""
    if isinstance(message, InaccessibleMessage):
        logger.debug('InaccessibleMessage: chat_id=%s', message.chat.id)
        raise FakeUser(
            f'Message with chat id: {message.chat.id} is InaccessibleMessage'
        )
    elif message is None:
        logger.debug('Message is None')
        raise MessageNotFound('Message is None')
    else:
        logger.debug('Message is accessible: chat_id=%s', message.chat.id)
        return message


async def validate_user_from_message(message: Message) -> User:
    user = message.from_user

    if not user:
        logger.debug('Message has no user: chat_id=%s', message.chat.id)
        raise UserNotFound(
            f'Chat with id: {message.chat.id} dont have any user'
        )
    return user


async def validate_username_from_user(user: User) -> str:
    username = user.username
    if not username:
        logger.debug('User has no username: user_id=%s', user.id)
        raise FakeUser(f'User with id {user.id} not have username')

    return username
