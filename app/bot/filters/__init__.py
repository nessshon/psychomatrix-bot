from aiogram import Dispatcher

from .is_private import IsPrivate


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
