from aiogram import Dispatcher


async def on_startup(dp: Dispatcher):
    from .bot import filters
    filters.setup(dp)

    from .bot import middlewares
    middlewares.setup(dp)

    from .bot import commands
    commands.register(dp)
    await commands.setup(dp.bot)

    from .bot import handlers
    handlers.register(dp)

    from .database import manage
    engine, sessionmaker = manage.loader()
    dp.bot["sessionmaker"] = sessionmaker
    await manage.run(engine)


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()

    session = await dp.bot.get_session()
    await session.close()
