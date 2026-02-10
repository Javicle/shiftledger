from aiogram.types import Message

from src.utils import validate_message, validate_text


async def pars_message(message: Message) -> dict[str, Any]:
    mess = await validate_message(message=message)
    text = await validate_text(mess)

    sales_item: dict[str, int] = {}

    for lines in text:
        for name, count in lines.split(':'):
            sales_item[name] = int(count)
