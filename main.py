import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent

import handlers.handlers
from config_data.config import load_config
import logging


async def main():
    config = load_config()

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )

    bot = Bot(token=config.tg_bot.bot_token)

    dp = Dispatcher()
    dp.include_router(handlers.handlers.router)
    setup_dialogs(dp)
    dp.errors.register(
        handlers.handlers.on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
