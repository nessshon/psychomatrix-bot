from dataclasses import dataclass

from aiogram.utils.markdown import hide_link


@dataclass
class MessageText:
    START: str = (
        "<b>Привет, {}!</b>\n\n"
        "Этот бот поможет рассчитать Квадрат Пифагора \"Психоматрицу\" по дате рождения.\n\n"
        "<b>Квадрат Пифагора еще называют Картой судьбы или Психоматрицей.</b>\n"
        "Это уникальный метод, который использовался еще египетскими жрецами. "
        "Пифагор доработал метод, так что теперь по дате рождения вы можете узнать все о человека."
        f"{hide_link('https://telegra.ph//file/d50e9257450847fd405b7.jpg')}\n\n"
    )
    OPEN_CALENDAR: str = (
        f"{hide_link('https://telegra.ph//file/05c8b5f7a094a9cbc1744.jpg')}"
        "<b>Чтобы рассчитать квадрат Пифагора</b>:\n\n"
        "• Отправьте дату рождения в формате <code>16.04.1998</code>\n"
        "• Откройте календарь и выберите дату рождения."
    )
    CALENDAR: str = (
        "<b>Выберите дату:</b>\n\n"
        "• Указана дата {}"
    )
    CHOOSE_MONTH: str = (
        "<b>Выберите месяц:</b>\n\n"
        "• Указан месяц {}"
    )
    CHOOSE_YEAR: str = (
        "<b>Выберите год:</b>\n\n"
        "• Указан год {}"
    )
    ERROR: str = (
        "<b>Неизвестная ошибка!</b>\n\n"
        "• Попробуйте повторить позже."
    )


@dataclass
class ButtonText:
    OPEN_CALENDAR: str = "Открыть календарь"
    SELECTED: str = "· {} ·"

    BACK: str = "‹ Назад"
    NEXT: str = "Далее ›"
    LEFT: str = "‹"
    RIGHT: str = "›"

    DOUBLE_LEFT: str = "«"
    DOUBLE_RIGHT: str = "»"
