import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs

from tg_bot.logger import logger
from tg_bot.config import settings

from tg_bot.keyboards.help_menu import set_main_menu
from tg_bot.handlers.user import router as user_router
from tg_bot.handlers.user_dialogs import dialog_router as user_router_dialogs

from redis.asyncio import Redis

logger.info("Starting bot")
redis = RedisStorage(
    redis=Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    ),
    key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
)

storage = MemoryStorage() #redis if settings.USE_REDIS else 
bot = Bot(token=settings.TG_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=storage)

dp.callback_query.middleware(CallbackAnswerMiddleware())
dp.startup.register(set_main_menu)


async def on_shutdown(bot):
    logger.info('Бот лег')


async def bot_main():
    try:
        dp.include_routers(
            user_router,
            user_router_dialogs
            )
        setup_dialogs(dp)
        dp.shutdown.register(on_shutdown)
        await bot.delete_webhook(True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(bot_main())