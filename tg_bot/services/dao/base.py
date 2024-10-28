from typing import Generic, TypeVar

from sqlalchemy import insert, select

from tg_bot.database.engine import SessionLocal

T = TypeVar('T')


class BaseDAO:
    model = None

    @classmethod
    def find_by_id(cls, model_id: int):
        with SessionLocal() as session:
            query = select(cls.model.__table__.columns).filter(cls.model.id == model_id)
            result = session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    def find_one_or_none(cls, **filter_by):
        with SessionLocal() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    def find_all(cls, **filter_by):
        with SessionLocal() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = session.execute(query)
            return result.mappings().all()

    @classmethod
    def add(cls, **data):
        with SessionLocal() as session:
            query = insert(cls.model).values(**data)
            session.execute(query)
            session.commit()