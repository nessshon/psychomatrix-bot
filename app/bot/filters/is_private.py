from aiogram.types import ChatType, Message, CallbackQuery
from aiogram.dispatcher.filters import BoundFilter


class IsPrivate(BoundFilter):

    async def check(self, update: Message | CallbackQuery) -> bool:
        chat = update.chat if update.__class__ == Message else update.message.chat
        return ChatType.PRIVATE == chat.type
