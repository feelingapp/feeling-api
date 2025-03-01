from argon2.exceptions import VerifyMismatchError
from sqlalchemy import Boolean, Column, String
from argon2 import PasswordHasher

from src.models import BaseModel

password_hasher = PasswordHasher()


class User(BaseModel):
    __tablename__ = "users"

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String)
    verified = Column(Boolean, nullable=False, default=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower()
        self.password_hash = self.hash_password(password)

    def hash_password(self, password):
        """Uses Argon2id to generate a password hash"""

        return password_hasher.hash(password)

    def verify_password(self, password):
        """Checks if a password matches with a hash"""
        try:
            return password_hasher.verify(self.password_hash, password)
        except VerifyMismatchError:
            return False

    def toJson(self):
        # Password not included in output for to security reasons
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "verified": self.verified,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    def __repr__(self):
        return "<User(id='{}', first_name='{}', last_name='{}', email='{}', password_hash='{}', verified='{}', created_at='{}', updated_at='{}')>".format(
            self.id,
            self.first_name,
            self.last_name,
            self.email,
            self.password_hash,
            self.verified,
            self.created_at,
            self.updated_at,
        )
