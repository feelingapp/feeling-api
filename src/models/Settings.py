from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB

from models import BaseModel


class Settings(BaseModel):
    __tablename__ = "settings"

    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    settings = Column(JSONB, nullable=False)

    def __init__(self, user_id, settings):
        self.user_id = user_id
        self.settings = settings

    def __repr__(self):
        return "<Settings(id='{}', user_id='{}' settings='{}', created_at='{}', updated_at='{}')>".format(
            self.id, self.user_id, self.settings, self.created_at, self.updated_at
        )
