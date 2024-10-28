from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from tg_bot.config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create MetaData without the bind argument
metadata = MetaData()


metadata.create_all(engine)
# reflect all tables
metadata.reflect(engine)

class Base(DeclarativeBase):
    pass