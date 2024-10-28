import random
import string
from passlib.context import CryptContext
from pydantic import EmailStr

from tg_bot.services.dao.user import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str):
    user = UsersDAO.find_one_or_none(email=email)
    if user and verify_password(password, user.hashed_password):
        return user
    
def generate_custom_pk(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))