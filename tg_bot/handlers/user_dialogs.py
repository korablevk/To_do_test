from aiogram import Router, F, types
from django.contrib.auth.hashers import check_password
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from tg_bot.config import settings
from tg_bot.logger import logger
from tg_bot.utils import authenticate_user
from tg_bot.dialogs.dialogs import bot_menu_dialogs
from tg_bot.dialogs.states import BotMenu

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

dialog_router = Router()
dialog_router.include_routers(bot_menu_dialogs)


@dialog_router.message(Command('tasks'))
async def begin(message: Message, dialog_manager: DialogManager):
    telegram_id = message.from_user.id
    await dialog_manager.start(BotMenu.waiting_for_email, show_mode=ShowMode.DELETE_AND_SEND, mode=StartMode.RESET_STACK)
    dialog_manager.dialog_data["telegram_id"] = telegram_id
    await message.delete()
