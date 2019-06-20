from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from argon2 import PasswordHasher

from src.models import BaseModel

password_hasher = PasswordHasher()

class RefreshToken(BaseModel):
    __tablename__ = "refresh_token"

    token_hash = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    def __init__(self, token, user_id, client_id):
        self.token_hash = self.hash_token(token)
        self.user_id = user_id
        self.client_id = client_id

    def __repr__(self):
        return "<RefreshToken(id='{}', token_hash='{}', user_id='{}', client_id='{}', created_at='{}', updated_at='{}')>".format(
            self.id,
            self.token_hash,
            self.user_id,
            self.client_id,
            self.created_at,
            self.updated_at,
        )

    def hash_token(self, token):
        """Uses Argon2id to generate a password hash"""

        return password_hasher.hash(token)

    def verify_token(self, token):
        """Checks if a password matches with a hash"""

        return password_hasher.verify(self.token_hash, token)
