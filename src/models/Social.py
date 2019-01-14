from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.models import BaseModel


class Social(BaseModel):
    __tablename__ = "socials"

    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    provider_id = Column(UUID, ForeignKey("social_providers.id"), nullable=False)
    social_id = Column(Integer, nullable=False)

    def __init__(self, user_id, provider_id, social_id):
        self.user_id = user_id
        self.provider_id = provider_id
        self.social_id = social_id

    def __repr__(self):
        return "<Social(id='{}', user_id='{}' provider_id='{}', social_id='{}', created_at='{}', updated_at='{}')>".format(
            self.id,
            self.user_id,
            self.provider_id,
            self.social_id,
            self.created_at,
            self.updated_at,
        )
