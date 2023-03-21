from aiogram.types import ChatType, Message
from aiogram.dispatcher.filters import BoundFilter


class IsGroup(BoundFilter):

    async def check(self, message: Message) -> bool:
        return message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
