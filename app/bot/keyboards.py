import calendar

from datetime import datetime
from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .texts import ButtonText


@dataclass
class CallbackData:
    OPEN_CALENDAR: str = "OPEN_CALENDAR"

    BACK: str = "BACK"
    NEXT: str = "NEXT"
    LEFT: str = "LEFT"
    RIGHT: str = "RIGHT"

    DOUBLE_LEFT: str = "DOUBLE_LEFT"
    DOUBLE_RIGHT: str = "DOUBLE_RIGHT"

    DAY: str = "DAY"
    WEEK: str = "WEEK"
    MONTH: str = "MONTH"
    YEAR: str = "YEAR"


class CalendarKeyboard:
    __slots__ = ["date", "weekdays", "days_month", "month_list", "month"]

    def __init__(self, date: datetime):
        self.date = date
        self.weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        self.days_month = calendar.monthcalendar(self.date.year, self.date.month)
        self.month_list = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                           "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        self.month = {i: month for i, month in enumerate(self.month_list, start=1)}

    def _years_inline_keyboard(self) -> list[list[InlineKeyboardButton]]:
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text=ButtonText.DOUBLE_LEFT,
                    callback_data=f"{CallbackData.YEAR}:{CallbackData.DOUBLE_LEFT}"
                ),
                InlineKeyboardButton(
                    text=ButtonText.LEFT,
                    callback_data=f"{CallbackData.YEAR}:{CallbackData.LEFT}"
                ),
                InlineKeyboardButton(
                    text=f"{ButtonText.SELECTED.format(self.date.year)}",
                    callback_data=CallbackData.YEAR
                ),
                InlineKeyboardButton(
                    text=ButtonText.RIGHT,
                    callback_data=f"{CallbackData.YEAR}:{CallbackData.RIGHT}"
                ),
                InlineKeyboardButton(
                    text=ButtonText.DOUBLE_RIGHT,
                    callback_data=f"{CallbackData.YEAR}:{CallbackData.DOUBLE_RIGHT}"
                )
            ]
        ]

        return inline_keyboard

    def _months_inline_keyboard(self) -> list[list[InlineKeyboardButton]]:
        return [
            [
                InlineKeyboardButton(
                    text=ButtonText.LEFT,
                    callback_data=f"{CallbackData.MONTH}:{CallbackData.LEFT}"
                ),
                InlineKeyboardButton(
                    text=ButtonText.SELECTED.format(self.month[self.date.month]),
                    callback_data=CallbackData.MONTH
                ),
                InlineKeyboardButton(
                    text=ButtonText.RIGHT,
                    callback_data=f"{CallbackData.MONTH}:{CallbackData.RIGHT}"
                )
            ]
        ]

    def _week_inline_keyboard(self):
        return [
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"{CallbackData.WEEK}:{text}"
                ) for text in self.weekdays
            ]
        ]

    def _days_inline_keyboard(self) -> list[list[InlineKeyboardButton]]:
        return [
            [
                InlineKeyboardButton(
                    text=ButtonText.SELECTED.format(day) if day == self.date.day
                    else day if day != 0 else " ",
                    callback_data=f"{CallbackData.DAY}:{day}"
                ) for day in week
            ] for week in self.days_month
        ]

    def years_markup(self):
        markup = InlineKeyboardMarkup(row_width=1)

        markup.add(
            *[
                InlineKeyboardButton(
                    text=str(year) if year != self.date.year
                    else ButtonText.SELECTED.format(year),
                    callback_data=f"{CallbackData.YEAR}:{year}"
                ) for year in range(self.date.year - 9, self.date.year + 1)
            ]
        )
        markup.row(
            InlineKeyboardButton(
                text=ButtonText.LEFT,
                callback_data=CallbackData.LEFT
            ),
            InlineKeyboardButton(
                text=ButtonText.RIGHT,
                callback_data=CallbackData.RIGHT
            ),
        )
        markup.row(
            InlineKeyboardButton(
                text=ButtonText.BACK,
                callback_data=CallbackData.BACK
            )
        )

        return markup

    def months_markup(self):
        markup = InlineKeyboardMarkup(row_width=1)

        markup.add(
            *[
                 InlineKeyboardButton(
                     text=self.month[i] if i != self.date.month
                     else ButtonText.SELECTED.format(self.month[i]),
                     callback_data=f"{CallbackData.MONTH}:{i}"
                 ) for i in self.month.keys()
             ] + [
                 InlineKeyboardButton(
                     text=ButtonText.BACK,
                     callback_data=CallbackData.BACK
                 )
             ]
        )

        return markup

    def markup(self):
        markup = InlineKeyboardMarkup()

        markup.inline_keyboard += self._years_inline_keyboard()
        markup.inline_keyboard += self._months_inline_keyboard()
        markup.inline_keyboard += self._week_inline_keyboard()
        markup.inline_keyboard += self._days_inline_keyboard()

        markup.inline_keyboard += [
            [
                InlineKeyboardButton(
                    text=ButtonText.BACK,
                    callback_data=CallbackData.BACK
                ),
                InlineKeyboardButton(
                    text=ButtonText.NEXT,
                    callback_data=CallbackData.NEXT
                )
            ]
        ]

        return markup


def open_calendar_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ButtonText.OPEN_CALENDAR,
                    callback_data=CallbackData.OPEN_CALENDAR
                )
            ]
        ]
    )
