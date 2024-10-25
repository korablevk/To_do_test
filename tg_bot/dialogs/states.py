from aiogram.filters.state import State, StatesGroup


class BotMenu(StatesGroup):
    waiting_for_email = State()
    waiting_for_password = State()
    verify_login_data = State()
    main = State()
    task = State()