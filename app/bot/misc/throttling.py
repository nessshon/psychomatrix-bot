from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler


def waiting_previous_execution(func, *args, **kwargs):
    async def decorator(message: Message, state: FSMContext):
        user_data = await state.get_data()

        if 'throttling' in user_data and user_data['throttling']:
            raise CancelHandler()

        return await func(message, state, *args, **kwargs)

    return decorator


def rate_limit(limit: float, key=None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)

        return func

    return decorator
