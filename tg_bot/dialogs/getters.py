from aiogram_dialog import DialogManager
from aiogram.types import Message, CallbackQuery
from tg_bot.services.dao.tasks import TasksDAO

from tg_bot.logger import logger


async def get_data_for_login(dialog_manager: DialogManager, **kwargs):
    return {
        "email": dialog_manager.dialog_data["email"],
        "password": dialog_manager.dialog_data["password"],
    }

async def get_user_id(
        callback: CallbackQuery,
        dialog_manager: DialogManager, **kwargs
        ):
    return {
        "first_name": dialog_manager.dialog_data["first_name"]
    }


async def get_user_tasks(
        dialog_manager: DialogManager, **kwargs
        ):
    try:
        tasks = TasksDAO.find_all(user_id=int(dialog_manager.dialog_data["user_id"]))
        logger.info(tasks)
        
        return {
        "first_name": dialog_manager.dialog_data["first_name"]
        }


    except Exception as e:
        logger.error(e)