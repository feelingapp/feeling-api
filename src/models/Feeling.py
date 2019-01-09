from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from models import BaseModel


class Feeling(BaseModel):
    __tablename__ = "feelings"

    emotion_id = Column(UUID, ForeignKey("emotions.id"), nullable=False)
    description = Column(String)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)

    def __init__(self, emotion_id, description, user_id):
        self.emotion_id = emotion_id
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return "<Feeling(id='{}', emotion_id='{}', description='{}', user_id='{}', created_at='{}', updated_at='{}')>".format(
            self.id,
            self.emotion_id,
            self.description,
            self.user_id,
            self.created_at,
            self.updated_at,
        )
