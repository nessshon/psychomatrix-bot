from contextlib import suppress

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted
from aiogram.utils.exceptions import (MessageNotModified,
                                      MessageCantBeEdited, MessageToEditNotFound)


async def edit_message(message: Message, text: str,
                       reply_markup: InlineKeyboardMarkup | None = None,
                       disable_web_page_preview: bool = False) -> Message:
    with suppress(MessageCantBeEdited, MessageToEditNotFound, MessageNotModified):
        return await message.edit_text(
            text, reply_markup=reply_markup,
            disable_web_page_preview=disable_web_page_preview
        )


async def delete_message(message: Message) -> None:
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


async def delete_previous_message(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    with suppress(KeyError, MessageCantBeDeleted, MessageToDeleteNotFound):
        message_id = data["message_id"]

        if message_id:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=data["message_id"]
            )
