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
    await dialog_manager.start(BotMenu.waiting_for_email, show_mode=ShowMode.DELETE_AND_SEND, mode=StartMode.RESET_STACK)
    await message.delete()

# class LoginStates(StatesGroup):
#     waiting_for_email = State()
#     waiting_for_password = State()

# @router.message(F.text == "/login")
# async def login_start(message: Message, state: FSMContext):
#     await message.answer("Введите ваш email:")
#     await state.set_state(LoginStates.waiting_for_email)

# @router.message(LoginStates.waiting_for_email)
# async def process_email(message: Message, state: FSMContext):
#     email = message.text
#     await state.update_data(email=email)
#     await message.answer("Теперь введите ваш пароль:")
#     await state.set_state(LoginStates.waiting_for_password)

# @router.message(LoginStates.waiting_for_password)
# async def process_password(message: Message, state: FSMContext):
#     data = await state.get_data()
#     email = data.get('email')
#     password = message.text

#     user = authenticate_user(email=email, password=password)

#     if user:
#         logger.info(f"User found: {user}")
#         authenticated = True
#         await message.answer("Login successful!")
#     else:
#         logger.info("User not found or incorrect password")
#         await message.answer("Неверный email или пароль.")

#     await state.clear()  # Clear the state after login attempt