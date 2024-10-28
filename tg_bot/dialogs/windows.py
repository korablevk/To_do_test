from dataclasses import dataclass
from typing import Dict, Any
from aiogram import F
from operator import itemgetter

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, Window, ChatEvent
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.common import ManagedScroll, Whenable, sync_scroll

from aiogram_dialog.widgets.kbd import (
    Radio, Column, Next, Back, 
    StubScroll, NumberedPager, Button, 
    ManagedRadio, Cancel, ScrollingGroup, Multiselect
)

from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Jinja, List

from tg_bot.config import settings

from tg_bot.dialogs.getters import (get_data_for_login, get_data_for_task, 
                                    get_user_id, get_user_tasks, get_comments, 
                                    get_categories, get_data_for_comment)

from tg_bot.dialogs.states import BotMenu
from tg_bot.services.dao.user import UsersDAO
from tg_bot.dialogs.selected import (error, auth_user, is_valid_date, on_input_email, 
                                     on_input_password, on_chosen_task, add_task, back_main,
                                     send_task_to_database, on_chosen_category, add_comment, send_comment_to_database)


ID_STUB_SCROLL = "stub_scroll"
ID_SYNC_SCROLL = "sync_scroll"
ID_SYNC_CATEGORY = "sync_scroll2"
ID_RADIO = "radio"
ID_RADIO_CATEGORY = "radio2"
ID_LIST_SCROLL = "list_scroll"
ID_LIST_CATEGORY = "list_scroll2"


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
        "<b>Здравствуйте</b>: {{first_name}}, \n"
        "Ваши задачи: \n"
    ),
    List(
        Format("{pos}. {item[0]} - {item[2]} (Сделать до: {item[3]})"),
        items="tasks",
        id=ID_LIST_SCROLL,
        page_size=5,
    ),
    Button(
        Const("Добавить задачу"),
        id="add",
        on_click=add_task,
    ),
    ScrollingGroup(
        Radio(
            checked_text=Format("Комментарии: 🔘 {item[0]}"),
            unchecked_text=Format("Комментарии: ⚪️ {item[0]}"),
            items="tasks",
            item_id_getter=itemgetter(1),
            id=ID_RADIO,
            on_click=on_chosen_task
        ),
        width=1,
        height=5,
        id=ID_SYNC_SCROLL,
        on_page_changed=sync_scroll(ID_LIST_SCROLL),
    ),
    state=BotMenu.main,
    getter=get_user_tasks, 
    preview_data=get_user_tasks, 
)

comment_window = Window(
    Jinja(
        "<b>Комментарии для задачи</b>:",
    ),
    Button(
        Const("Добавить комментарий"),
        id="add",
        on_click=add_comment,
    ),
    List(
        Format("{pos}. {item[0]}"),
        items="comments",
        id="comment_list",
        page_size=10,
    ),
    Back(Const("Назад")),
    state=BotMenu.comment,
    getter=get_comments,
    preview_data=get_comments,
)

add_task_window = Window(
    Const("Напишите название для задачи"),
    TextInput(id="name_input", filter=F.text, on_error=error, on_success=Next()),
    Cancel(Const("Отмена")),
    Button(
        Const("Назад"),
        id="back_main",
        on_click=back_main,
    ),
    state=BotMenu.add_name_task,
)

add_description_window = Window(
    Const("Напишите описание для задачи"),
    TextInput(id="description_input", filter=F.text, on_error=error, on_success=Next()),
    Back(Const("Назад")),
    Cancel(Const("Отмена")),
    state=BotMenu.add_description_task,
)

add_due_to_window = Window(
    Const("Напишите до какого числа нужно выполнить задачу\n"),
    Const("В формате YYYY-MM-DD HH:MM (например, 2025-12-04 17:00 для 4 декабря 2025 года 17:00)"),
    TextInput(
        id="due_to_input",
        filter=is_valid_date,
        on_error=Const("Неверный формат даты. Используйте YYYY-MM-DD HH:MM."),
        on_success=Next(),
    ),
    Cancel(Const("Отмена")),
    state=BotMenu.add_due_to_task,
)

add_category_window = Window(
    Const("Выберите категорию"),
    ScrollingGroup(
        Radio(
            checked_text=Format("🔘 {item[0]}"),
            unchecked_text=Format("⚪️ {item[0]}"),
            items="categories",
            item_id_getter=itemgetter(1),
            id=ID_RADIO,
            on_click=on_chosen_category
        ),
        width=1,
        height=5,
        id=ID_SYNC_SCROLL,
        on_page_changed=sync_scroll(ID_LIST_SCROLL),
    ),
    Cancel(Const("Отмена")),
    Back(Const("Назад")),
    state=BotMenu.add_category,
    getter=get_categories, 
    preview_data=get_categories,  
)

confirm_task_window = Window(
    Jinja(
        "<b>Название</b>: {{name}}, \n"
        "<b>Описание</b> {{description}} \n"
        "<b>Дата до</b>: {{due_to}}\n"
    ),
    Button(Const("Отправить в базу данных"), id="go", on_click=send_task_to_database),
    Cancel(Const("Отмена")),
    Back(Const("Назад")),
    state=BotMenu.confirm_task,
    getter=get_data_for_task,
)


add_comment_window = Window(
    Const("Напишите ваш комментарий"),
    TextInput(id="comment_input", filter=F.text, on_error=error, on_success=Next()),
    Button(
        Const("Назад"),
        id="back_main",
        on_click=back_main,
    ),
    Cancel(Const("Отмена")),
    state=BotMenu.add_text_comment,
)

confirm_comment_window = Window(
    Jinja(
        "<b>Комментарий</b>: {{comment}}, \n"
    ),
    Button(Const("Отправить в базу данных"), id="go2", on_click=send_comment_to_database),
    Cancel(Const("Отмена")),
    Back(Const("Назад")),
    state=BotMenu.confirm_comment,
    getter=get_data_for_comment,
)