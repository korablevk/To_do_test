from aiogram import types
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from tg_bot.dialogs.windows import (
    main_window, email_window, password_window, 
    verify_login_data_window, comment_window, add_task_window,
    add_description_window, add_due_to_window, confirm_task_window,
    add_category_window, add_comment_window, confirm_comment_window)

from aiogram_dialog import Dialog, DialogManager, Window, LaunchMode


bot_menu_dialogs = Dialog(
    email_window,
    password_window,
    verify_login_data_window,
    main_window,
    comment_window,
    add_task_window,
    add_description_window,
    add_due_to_window,
    add_category_window,
    confirm_task_window,
    add_comment_window,
    confirm_comment_window
)