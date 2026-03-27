from models.users_table import User
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ValidationHelper:
    def authenticate_user(username: str, password: str, db):
        user = db.query(User).filter(User.email == username).first()
        if user is None:
            return False
        if not bcrypt_context.verify(password, user.password):
            return False
        return user

