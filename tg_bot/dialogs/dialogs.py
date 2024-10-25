from aiogram import types
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from tg_bot.dialogs.windows import main_window, email_window, password_window, verify_login_data_window

from aiogram_dialog import Dialog, DialogManager, Window, LaunchMode


bot_menu_dialogs = Dialog(
    email_window,
    password_window,
    verify_login_data_window,
    main_window,
)