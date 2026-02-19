from aiogram.types import Message

from src.utils import validate_message, validate_text


async def pars_message(message: Message) -> dict[str, int]:
    # message = name : count
    #           name : count

    mess = await validate_message(message=message)
    text = await validate_text(mess)

    sales_item: dict[str, int] = {}

    result = [x for x in text.split('\n') if x]
    for obj in result:
        name, count = obj.split(':')
        sales_item[name] = int(count)

    return sales_item
