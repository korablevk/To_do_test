import bcrypt
from datetime import date
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from tg_bot.services.dao.base import BaseDAO
from tg_bot.models.comments import Comments
from tg_bot.database.engine import SessionLocal

class CommentsDAO(BaseDAO):
    model = Comments