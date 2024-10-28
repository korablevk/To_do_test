from aiogram.filters.state import State, StatesGroup


class BotMenu(StatesGroup):
    waiting_for_email = State()
    waiting_for_password = State()
    verify_login_data = State()
    main = State()
    task = State()
    comment = State()
    add_name_task = State()
    add_description_task = State()
    add_due_to_task = State()
    add_category = State()
    confirm_task = State()
    add_text_comment = State()
    confirm_comment = State()
