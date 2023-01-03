from aiogram import Bot


def async_sessionmaker():
    bot = Bot.get_current()
    sessionmaker = bot.get("sessionmaker")

    return sessionmaker()
