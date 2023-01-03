from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    OPEN_CALENDAR = State()
    CALENDAR = State()
    CHOOSE_MONTH = State()
    CHOOSE_YEAR = State()
