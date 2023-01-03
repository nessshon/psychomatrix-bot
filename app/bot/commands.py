import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils import markdown
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, Message

from . import keyboards

from .states import UserState
from .texts import MessageText

from .filters import IsPrivate

from .misc.throttling import rate_limit
from .misc.messages import delete_previous_message, delete_message, edit_message

from ..database.models.users import User


@rate_limit(2.2)
async def command_start(message: Message, state: FSMContext):
    emoji = await message.answer("👋")

    await delete_previous_message(message, state)
    await delete_message(message)
    await asyncio.sleep(2)

    user_link = markdown.hlink(
        title=message.from_user.first_name,
        url=message.from_user.url
    )
    text = MessageText.START.format(user_link)
    text += MessageText.OPEN_CALENDAR
    markup = keyboards.open_calendar_markup()

    await edit_message(emoji, text.format(user_link), reply_markup=markup)
    async with state.proxy() as data:
        data.clear()

    await state.update_data(message_id=emoji.message_id)
    await UserState.OPEN_CALENDAR.set()

    if not await User.is_exists(message.from_user.id):
        await User.add(
            id=message.from_user.id,
            name=message.from_user.first_name
        )


async def setup(bot: Bot):
    commands = {
        "en": [
            BotCommand("start", "Restart"),
        ],
        "ru": [
            BotCommand("start", "Перезапустить"),
        ]
    }

    await bot.set_my_commands(
        commands=commands["ru"],
        scope=BotCommandScopeAllPrivateChats(),
        language_code="ru"
    )
    await bot.set_my_commands(
        commands=commands["en"],
        scope=BotCommandScopeAllPrivateChats(),
    )


def register(dp: Dispatcher):
    dp.register_message_handler(
        command_start, CommandStart(), IsPrivate(), state="*"
    )
