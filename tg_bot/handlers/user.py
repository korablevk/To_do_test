from aiogram import Router, F, types
from django.contrib.auth.hashers import check_password
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from tg_bot.config import settings
from tg_bot.logger import logger
from tg_bot.utils import authenticate_user

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import bcrypt  

authenticated = False

router = Router()

if settings.BOT_LANGUAGE == 'en':
    from tg_bot.lexicon.en import GREETING_TEXT
elif settings.BOT_LANGUAGE == 'ru':
    from tg_bot.lexicon.ru import GREETING_TEXT
else:
    raise ValueError(f"Unsupported language: {settings.BOT_LANGUAGE}")

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.delete()
    await message.answer(GREETING_TEXT['greeting'])


