from hashlib import sha256

from argon2 import PasswordHasher
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression

from src.models import BaseModel


class RefreshToken(BaseModel):
    __tablename__ = "refresh_token"

    # Equivalent to 14 days
    TOKEN_LIFE = "20160"

    token_hash = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    def __init__(self, token, user_id, client_id):
        self.token_hash = self.hash_token(token)
        self.user_id = user_id
        self.client_id = client_id

    def __repr__(self):
        return "<RefreshToken(id='{}', token_hash='{}', user_id='{}', client_id='{}', valid_at='{}', expires_at='{}' created_at='{}', updated_at='{}')>".format(
            self.id,
            self.token_hash,
            self.user_id,
            self.client_id,
            self.valid_at,
            self.expires_at,
            self.created_at,
            self.updated_at,
        )

    def hash_token(self, token):
        """Hashes a token with SHA256"""

        return sha256(token.encode()).hexdigest()

    def verify_token(self, token):
        """Checks if a token matches with a hash"""

        return self.token_hash == self.hash_token(token)
