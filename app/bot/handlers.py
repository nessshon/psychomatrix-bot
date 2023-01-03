import re
import logging
import asyncio

from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils import markdown

from . import keyboards

from .states import UserState
from .texts import MessageText

from .filters import IsPrivate
from .keyboards import CallbackData

from .misc.throttling import rate_limit, waiting_previous_execution
from .misc.messages import edit_message, delete_message, delete_previous_message

from ..psychomatrix import Psychomatrix
from ..database.models import PsychomatrixSavedPage


async def open_calendar(state: FSMContext, message: Message = None, call: CallbackQuery = None):
    text = MessageText.OPEN_CALENDAR
    markup = keyboards.open_calendar_markup()

    if message:
        msg = await message.answer(text, reply_markup=markup)

        await delete_previous_message(message, state)
        await state.update_data(message_id=msg.message_id)

    else:
        await edit_message(call.message, text, reply_markup=markup)

    await UserState.OPEN_CALENDAR.set()


async def calendar(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date = data["date"] if "date" in data else datetime.now().isoformat()
    date = datetime.fromisoformat(date)

    text = MessageText.CALENDAR.format(date.strftime("%-d %B %Y г."))
    markup = keyboards.CalendarKeyboard(date).markup()

    await edit_message(call.message, text, reply_markup=markup)
    await UserState.CALENDAR.set()


async def choose_month(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date = data["date"] if "date" in data else datetime.now().isoformat()
    date = datetime.fromisoformat(date)

    text = MessageText.CHOOSE_MONTH.format(keyboards.CalendarKeyboard(date).month[date.month])
    markup = keyboards.CalendarKeyboard(date).months_markup()

    await edit_message(call.message, text, reply_markup=markup)
    await UserState.CHOOSE_MONTH.set()


async def choose_year(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date = data["date"] if "date" in data else datetime.now().isoformat()
    date = datetime.fromisoformat(date)

    text = MessageText.CHOOSE_YEAR.format(date.strftime("%Y г."))
    markup = keyboards.CalendarKeyboard(date).years_markup()

    await edit_message(call.message, text, reply_markup=markup)
    await UserState.CHOOSE_YEAR.set()


@rate_limit(0.5)
async def calculate_callback_handler(call: CallbackQuery, state: FSMContext):
    if call.data == CallbackData.OPEN_CALENDAR:
        await calendar(call, state)

    await call.answer()


@rate_limit(0.2)
@waiting_previous_execution
async def calendar_callback_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date = data["date"] if "date" in data else datetime.now().isoformat()
    date = datetime.fromisoformat(date)

    if call.data == CallbackData.BACK:
        await open_calendar(state, call=call)

    elif call.data == CallbackData.NEXT:
        await edit_message(call.message, text="⌛️")
        await state.update_data(throttling=True)

        try:
            if await PsychomatrixSavedPage.is_exists(date.strftime("%d%m%Y")):
                page = await PsychomatrixSavedPage.get(date.strftime("%d%m%Y"))
                await asyncio.sleep(1)

            else:
                psychomatrix = Psychomatrix(date)
                page = await psychomatrix.create_page()

                await PsychomatrixSavedPage.add(
                    date=date.strftime("%d%m%Y"),
                    title=page.title,
                    url=page.url
                )

            text = markdown.hlink(title=page.title, url=page.url)
            await edit_message(call.message, text)

        except Exception as err:
            logging.error(err)
            text = MessageText.ERROR
            await edit_message(call.message, text)

        finally:
            await state.update_data(throttling=False)
            await open_calendar(state, call=call)

    elif call.data.startswith(CallbackData.YEAR):
        if call.data == CallbackData.YEAR:
            await choose_year(call, state)
        else:
            _, navigation = call.data.split(":")

            if navigation == CallbackData.LEFT:
                date = date.replace(year=date.year - 1)
            if navigation == CallbackData.DOUBLE_LEFT:
                date = date.replace(year=date.year - 10)
            if navigation == CallbackData.RIGHT:
                date = date.replace(year=date.year + 1)
            if navigation == CallbackData.DOUBLE_RIGHT:
                date = date.replace(year=date.year + 10)

            await state.update_data(date=date.isoformat())
            await calendar(call, state)

    elif call.data.startswith(CallbackData.MONTH):
        if call.data == CallbackData.MONTH:
            await choose_month(call, state)
        else:
            _, navigation = call.data.split(":")

            if navigation == CallbackData.LEFT:
                if date.month == 1:
                    month = 12
                else:
                    month = date.month - 1
                date = date.replace(month=month, day=1)
            if navigation == CallbackData.RIGHT:
                if date.month == 12:
                    month = 1
                else:
                    month = date.month + 1
                date = date.replace(month=month, day=1)

            await state.update_data(date=date.isoformat())
            await calendar(call, state)

    elif call.data.startswith(CallbackData.DAY):
        _, value = call.data.split(":")
        if int(value) > 0:
            date = date.replace(day=int(value))

        await state.update_data(date=date.isoformat())
        await calendar(call, state)

    await call.answer()


@rate_limit(0.2)
async def choose_month_callback_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date = data["date"] if "date" in data else datetime.now().isoformat()
    date = datetime.fromisoformat(date)

    if call.data == CallbackData.BACK:
        await calendar(call, state)

    elif call.data.startswith(CallbackData.MONTH):
        _, value = call.data.split(":")
        date = date.replace(month=int(value), day=1)
        await state.update_data(date=date.isoformat())
        await calendar(call, state)

    await call.answer()


@rate_limit(0.2)
async def choose_year_callback_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date = data["date"] if "date" in data else datetime.now().isoformat()
    date = datetime.fromisoformat(date)

    if call.data == CallbackData.BACK:
        await calendar(call, state)

    elif call.data == CallbackData.LEFT:
        date = date.replace(year=date.year - 10)
        await state.update_data(date=date.isoformat())
        await choose_year(call, state)

    elif call.data == CallbackData.RIGHT:
        date = date.replace(year=date.year + 10)
        await state.update_data(date=date.isoformat())
        await choose_year(call, state)

    elif call.data.startswith(CallbackData.YEAR):
        _, value = call.data.split(":")
        date = date.replace(year=int(value), day=1)
        await state.update_data(date=date.isoformat())
        await calendar(call, state)

    await call.answer()


@rate_limit(1)
@waiting_previous_execution
async def text_date_message_handler(message: Message, state: FSMContext):
    def validate(value):
        return re.fullmatch(r"^\d{2}.\d{2}.\d{4}$", value)

    if message.content_type == "text" and validate(message.text):
        date = datetime.strptime(message.text, "%d.%m.%Y")

        emoji = await message.reply("⌛️")
        await state.update_data(throttling=True)
        await delete_previous_message(message, state)

        try:
            if await PsychomatrixSavedPage.is_exists(date.strftime("%d%m%Y")):
                page = await PsychomatrixSavedPage.get(date.strftime("%d%m%Y"))
                await asyncio.sleep(1)

            else:
                psychomatrix = Psychomatrix(date)
                page = await psychomatrix.create_page()

                await PsychomatrixSavedPage.add(
                    date=date.strftime("%d%m%Y"),
                    title=page.title,
                    url=page.url
                )

            text = markdown.hlink(title=page.title, url=page.url)
            await edit_message(emoji, text)

        except Exception as err:
            logging.error(err)
            text = MessageText.ERROR
            await edit_message(emoji, text)

        finally:
            await state.update_data(throttling=False)
            await open_calendar(state, message=message)
    else:
        await delete_message(message)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(
        calculate_callback_handler, IsPrivate(),
        state=UserState.OPEN_CALENDAR
    )
    dp.register_callback_query_handler(
        calendar_callback_handler, IsPrivate(),
        state=UserState.CALENDAR
    )
    dp.register_callback_query_handler(
        choose_month_callback_handler, IsPrivate(),
        state=UserState.CHOOSE_MONTH
    )
    dp.register_callback_query_handler(
        choose_year_callback_handler, IsPrivate(),
        state=UserState.CHOOSE_YEAR
    )
    dp.register_message_handler(
        text_date_message_handler, IsPrivate(),
        content_types="any",
        state="*"
    )
