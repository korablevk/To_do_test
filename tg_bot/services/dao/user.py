import bcrypt
from sqlalchemy import and_, select, update
from tg_bot.services.dao.base import BaseDAO
from tg_bot.models.user import Users
from tg_bot.database.engine import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    def update_telegram_id(
        cls,
        telegram_id: str,
        user_id: int,
    ):
        try:
            with SessionLocal() as session:

                update_telegram = (
                    update(Users)
                    .where(
                        and_(
                            Users.id == user_id,
                        )
                    )
                    .values(
                        telegram_id=telegram_id,
                    )
                )

                result = session.execute(update_telegram)
                session.commit()


        except SQLAlchemyError as e:
            session.rollback()  # Roll back the session on error
            raise Exception("Database Error: Cannot update comment") from e
        except Exception as e:
            raise Exception(f"Error while updating comment: {str(e)}") from e


    @classmethod
    def user_has_telegram_id(cls, user_id: int) -> bool:
        with SessionLocal() as session:
            query = select(cls.model).where(cls.model.id == user_id)
            result = session.execute(query).scalar_one_or_none()
            return result is not None and result.telegram_id is not None