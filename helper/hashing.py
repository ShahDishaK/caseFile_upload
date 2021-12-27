# Importing libraries
from passlib.context import CryptContext

# Initializing
hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    # Hashed a password
    def get_hash(text: str):
        return hash_context.hash(text)

    # Verifies if the given password and hashed password is same
    def verify(plain_text: str, hashed_text: str):
        return hash_context.verify(plain_text, hashed_text)
