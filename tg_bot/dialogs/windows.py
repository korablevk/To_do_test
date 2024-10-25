from dataclasses import dataclass
from typing import Dict, Any
from aiogram import F

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, Window, ChatEvent
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.common import ManagedScroll, Whenable
from aiogram_dialog.widgets.kbd import Radio, Column, Next, Back, StubScroll, NumberedPager, Button, ManagedRadio, Cancel
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Jinja

from tg_bot.config import settings

from tg_bot.dialogs.getters import get_data_for_login, get_user_id, get_user_tasks

from tg_bot.dialogs.states import BotMenu
from tg_bot.services.dao.user import UsersDAO
from tg_bot.dialogs.selected import error, auth_user, on_input_email, on_input_password

email_window = Window(
    Const("Введите ваш email:"),
    TextInput(id="email_input", filter=F.text, on_error=error, on_success=on_input_email),
    Cancel(Const("Отмена")),
    state=BotMenu.waiting_for_email,
)

password_window = Window(
    Const("Теперь введите ваш пароль:"),
    TextInput(id="password_input", filter=F.text, on_error=error, on_success=on_input_password),
    Cancel(Const("Отмена")),
    Back(Const("Назад")),
    state=BotMenu.waiting_for_password,
)

verify_login_data_window = Window(
    Jinja(
        "<b>Ваш email</b>: {{email}}, \n"
        "<b>Ваш пароль</b> {{password}} \n"
    ),
    Button(Const("Логин"), id="go", on_click=auth_user),
    Cancel(Const("Отмена")),
    Back(Const("Назад")),
    state=BotMenu.verify_login_data,
    getter=get_data_for_login
)

main_window = Window(
    Jinja(
        "<b>Здавствуйте</b>: {{first_name}}, \n"
    ),
    getter=get_user_tasks,
    state=BotMenu.main,
)