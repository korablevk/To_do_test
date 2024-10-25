from typing import Any

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button
from tg_bot.logger import logger
from tg_bot.dialogs.states import BotMenu

from tg_bot.utils import authenticate_user


async def error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await manager.event.answer("Ошибка")

async def on_input_email(
        message: Message,
        dialog_: Any,
        dialog_manager: DialogManager,
        error_: ValueError
):
    dialog_manager.dialog_data["email"] = message.text
    await dialog_manager.next()

async def on_input_password(
        message: Message,
        dialog_: Any,
        dialog_manager: DialogManager,
        error_: ValueError
):
    dialog_manager.dialog_data["password"] = message.text
    await dialog_manager.next()


'''
FIXME при первом логине добавить telegram_id в БД
'''
async def auth_user(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    email = str(dialog_manager.dialog_data["email"])
    password = str(dialog_manager.dialog_data["password"])

    user = authenticate_user(email=email, password=password)

    logger.info(user)

    if user:
        logger.info(f"User found: {user}")
        await callback.answer("Login successful!")
        dialog_manager.dialog_data["user_id"] = user.id
        dialog_manager.dialog_data["first_name"] = user.first_name
        await dialog_manager.next()
    else:
        logger.info("User not found or incorrect password")
        await callback.answer("Неверный email или пароль.")

        