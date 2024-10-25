import bcrypt
from sqlalchemy import select
from tg_bot.services.dao.base import BaseDAO
from tg_bot.models.tasks import Tasks
from tg_bot.database.engine import SessionLocal

class TasksDAO(BaseDAO):
    model = Tasks
