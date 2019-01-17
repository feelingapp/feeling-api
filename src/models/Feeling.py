from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.consts import Emotion
from src.models import BaseModel


class Feeling(BaseModel):
    __tablename__ = "feelings"

    emotion_id = Column(Integer, ForeignKey("emotions.id"), nullable=False)
    description = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    hashtags = relationship("Hashtag", secondary="feeling_hashtags", backref="feelings")

    def __init__(self, emotion: Emotion, description, user_id):
        self.emotion_id = emotion.value
        self.description = description
        self.user_id = user_id

    @property
    def emotion(self):
        return Emotion(self.emotion_id)

    def toJson(self):
        return {
            "id": str(self.id),
            "emotion": Emotion(self.emotion_id).name,
            "description": self.description,
            "user_id": self.user_id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    def __repr__(self):
        return "<Feeling(id='{}', emotion_id='{}', description='{}', user_id='{}', created_at='{}', updated_at='{}')>".format(
            self.id,
            self.emotion_id,
            self.description,
            self.user_id,
            self.created_at,
            self.updated_at,
        )
