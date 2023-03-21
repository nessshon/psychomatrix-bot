from aiogram.types import ChatType, Message
from aiogram.dispatcher.filters import BoundFilter


class IsGroup(BoundFilter):

    async def check(self, message: Message) -> bool:
        groups_types = [ChatType.GROUP, ChatType.SUPERGROUP]
        groups_allowed = [-1001918777590]

        return message.chat.type in groups_types and message.chat.id in groups_allowed
