import secrets
import string
import time
from hashlib import sha256

from argon2 import PasswordHasher
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression

from src.models import BaseModel


class RefreshToken(BaseModel):
    __tablename__ = "refresh_token"

    TOKEN_LIFE = 20160  # Equivalent to 14 days
    TOKEN_LENGTH = 20

    token = None
    token_hash = Column(String, nullable=False, unique=True)
    issue_time = Column(DateTime(), nullable=False, default=lambda: int(time.time()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    def __init__(self, user_id, client_id):
        self.token = self.generate_token()
        self.token_hash = RefreshToken.hash_token(self.token)
        self.user_id = user_id
        self.client_id = client_id

    def __repr__(self):
        return "<RefreshToken(id='{}', token_hash='{}', user_id='{}', client_id='{}', issue_time='{}', created_at='{}', updated_at='{}')>".format(
            self.id,
            self.token_hash,
            self.issue_time,
            self.user_id,
            self.client_id,
            self.created_at,
            self.updated_at,
        )

    @property
    def expires_in(self):
        return self.issue_time + self.TOKEN_LIFE

    def generate_token(self):
        return "".join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(self.TOKEN_LENGTH)
        )

    @staticmethod
    def hash_token(unhashed_token):
        """Hashes a token with SHA256"""

        return sha256(unhashed_token.encode()).hexdigest()

    def verify_token(self, token):
        """Checks if a token matches with a hash"""

        return self.token_hash == self.hash_token(token)
