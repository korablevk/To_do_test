from tg_bot.database.engine import metadata, engine, Base
from sqlalchemy import Table

user_table = Table('user', metadata, autoload_with=engine)

class Users(Base):
    __table__ = user_table