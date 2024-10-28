from aiogram_dialog import DialogManager
from aiogram.types import Message, CallbackQuery
from tg_bot.services.dao.tasks import TasksDAO, CategoriesDAO
from tg_bot.services.dao.comments import CommentsDAO

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


async def get_user_tasks(dialog_manager: DialogManager, **kwargs):
    try:
        tasks = TasksDAO.find_all(user_id=int(dialog_manager.dialog_data["user_id"]))
        
        logger.info(tasks)

        task_details = [
            (task['name'], task['id'], task['description'], task['due_date'].strftime('%Y-%m-%d %H:%M'), task['completed']) 
            for task in tasks
        ]

        return {
            "first_name": dialog_manager.dialog_data["first_name"],
            "tasks": task_details
        }

    except Exception as e:
        logger.error(e)
        return {
            "first_name": dialog_manager.dialog_data.get("first_name", ""),
            "tasks": [] 
        }

async def get_categories(dialog_manager: DialogManager, **kwargs):
    try:
        user_id = int(dialog_manager.dialog_data["user_id"])
        categories = CategoriesDAO.find_all_categories(user_id=int(user_id) if user_id else None)

        category_details = [
            (category['name'], category['id'], category['slug']) 
            for category in categories
        ]
        return {
            "categories": category_details
        }

    except Exception as e:
        logger.error(e)
        return {
            "categories": []
        }


async def get_comments(dialog_manager: DialogManager, **kwargs):
    try:
        task_id = dialog_manager.dialog_data.get('task_id')
        # task = TasksDAO.find_by_id(task_id=task_id)
        comments = CommentsDAO.find_all(task_id=task_id)
        
        # logger.info(task)

        comments_details = [
            (comment['comment_text'], comment['id']) 
            for comment in comments
        ]

        return {
            "comments": comments_details
        }

    except Exception as e:
        logger.error(e)
        return {
            "comments": [] 
        }
    

async def get_data_for_task(dialog_manager: DialogManager, **kwargs):
    return {
        "name": dialog_manager.find("name_input").get_value(),
        "description": dialog_manager.find("description_input").get_value(),
        "due_to": dialog_manager.find("due_to_input").get_value(),
        "category": dialog_manager.dialog_data["category_id"],
    }

async def get_data_for_comment(dialog_manager: DialogManager, **kwargs):
    return {
        "comment": dialog_manager.find("comment_input").get_value(),
    }