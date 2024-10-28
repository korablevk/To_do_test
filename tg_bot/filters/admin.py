from aiogram.filters import Filter
from aiogram import Bot, types
from tg_bot.config import settings


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in settings.ADMINS
