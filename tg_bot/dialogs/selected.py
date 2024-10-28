import re
from typing import Any, Optional

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button
import pytz
from tg_bot.logger import logger
from tg_bot.dialogs.states import BotMenu
from tg_bot.services.dao.user import UsersDAO
from tg_bot.services.dao.tasks import TasksDAO
from tg_bot.services.dao.comments import CommentsDAO
from datetime import datetime

from tg_bot.utils import authenticate_user, generate_custom_pk

async def is_valid_date(message: Message) -> bool:
    try:
        date_str = message.text

        datetime.strptime(date_str, "%Y-%m-%d %H:%M")

        if datetime.strptime(date_str, "%Y-%m-%d %H:%M") <= datetime.now():
            return False 

        return True
    except ValueError:
        return False


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


async def auth_user(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    email = str(dialog_manager.dialog_data["email"])
    password = str(dialog_manager.dialog_data["password"])

    telegram_id = dialog_manager.dialog_data.get("telegram_id")

    user = authenticate_user(email=email, password=password)

    logger.info(user)

    if user:
        await callback.answer("Login successful!")
        dialog_manager.dialog_data["user_id"] = user.id
        dialog_manager.dialog_data["first_name"] = user.first_name

        if UsersDAO.user_has_telegram_id(user.id):
            await dialog_manager.next()
        else:
            UsersDAO.update_telegram_id(telegram_id=telegram_id, user_id=user.id)
            logger.info(f"Updated telegram_id for user {user.id}: {telegram_id}")
            await dialog_manager.next()

    else:
        logger.info("User not found or incorrect password")
        await callback.answer("Неверный email или пароль.")

        
async def on_chosen_task(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    ctx = dialog_manager.current_context()
    ctx.dialog_data['task_id'] = item_id
    await dialog_manager.switch_to(BotMenu.comment)


async def on_chosen_category(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    ctx = dialog_manager.current_context()
    ctx.dialog_data['category_id'] = item_id
    await dialog_manager.switch_to(BotMenu.confirm_task)


async def add_task(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(BotMenu.add_name_task)


async def send_task_to_database(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    try:
        name = dialog_manager.find("name_input").get_value()
        description = dialog_manager.find("description_input").get_value()
        due_date_str = dialog_manager.find("due_to_input").get_value()
        category_id = dialog_manager.dialog_data["category_id"]

        if not name or not description or not due_date_str:
            raise ValueError("Все поля должны быть заполнены.")

        due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")

        TasksDAO.add(
            id=generate_custom_pk(),
            name=name,
            description=description,
            due_date=due_date,
            completed=False,
            category_id=category_id,
            created_date=datetime.now(),
            user_id=int(dialog_manager.dialog_data["user_id"]),
        )
        await callback.answer("Задача добавлена в базу данных.")
        await dialog_manager.switch_to(BotMenu.main)

    except Exception as e:
        logger.error(e)
        await callback.answer(f"Ошибка: \n{str(e)}")


async def add_comment(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(BotMenu.add_text_comment)


async def send_comment_to_database(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    try:

        comment = dialog_manager.find("comment_input").get_value()
        task_id = dialog_manager.dialog_data["task_id"]

        CommentsDAO.add(
            task_id=task_id,  
            user_id=int(dialog_manager.dialog_data["user_id"]),                   
            comment_text=comment, 
            created_at=datetime.now() 
        )
        await callback.answer("Комментарий добавлен в базу данных.")
        await dialog_manager.switch_to(BotMenu.main)

    except Exception as e:
        logger.error(e)
        await callback.answer(f"Ошибка: \n{str(e)}")


async def back_main(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(BotMenu.main)