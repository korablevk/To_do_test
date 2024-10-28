from tg_bot.database.engine import metadata, engine, Base
from sqlalchemy import Table

task_table = Table('task',metadata,autoload_with=engine)
class Tasks(Base):
    __table__ = task_table


category_table = Table('category',metadata,autoload_with=engine)
class Categories(Base):
    __table__ = category_table