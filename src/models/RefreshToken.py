from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from models import BaseModel


class RefreshToken(BaseModel):
    __tablename__ = "refresh_token"

    token_hash = Column(String, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    client_id = Column(UUID, ForeignKey("clients.id"), nullable=False)

    def __init__(self, token_hash, user_id, client_id):
        self.token_hash = token_hash
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
