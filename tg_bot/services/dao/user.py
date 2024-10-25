import bcrypt
from sqlalchemy import select
from tg_bot.services.dao.base import BaseDAO
from tg_bot.models.user import Users
from tg_bot.database.engine import SessionLocal

class UsersDAO(BaseDAO):
    model = Users
