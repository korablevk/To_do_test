import bcrypt
from sqlalchemy import select
from tg_bot.services.dao.base import BaseDAO
from tg_bot.models.tasks import Tasks, Categories
from tg_bot.database.engine import SessionLocal

class TasksDAO(BaseDAO):
    model = Tasks

class CategoriesDAO(BaseDAO):
    model = Categories

    @classmethod
    def find_all_categories(cls, user_id: int = None):
        with SessionLocal() as session:
            query = select(cls.model.__table__.columns)
            if user_id is None:
                query = query.filter(cls.model.user_id.is_(None))
            else:
                query = query.filter((cls.model.user_id == user_id) | (cls.model.user_id.is_(None)))

            result = session.execute(query)
            return result.mappings().all()