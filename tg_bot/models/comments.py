from tg_bot.database.engine import metadata, engine, Base
from sqlalchemy import Table

comment_table = Table('comment',metadata,autoload_with=engine)
class Comments(Base):
    __table__ = comment_table