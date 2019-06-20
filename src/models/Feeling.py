from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from src.consts import Emotion
from src.models import BaseModel


class Feeling(BaseModel):
    __tablename__ = "feelings"

    emotion_id = Column(Integer, ForeignKey("emotions.id"), nullable=False)
    description = Column(String)
    hashtags = Column(ARRAY(String))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    def __init__(self, emotion: Emotion, description, hashtags, user_id):
        self.emotion_id = emotion.value
        self.description = description
        self.hashtags = hashtags
        self.user_id = user_id

    @property
    def emotion(self):
        return Emotion(self.emotion_id)

    def set_emotion(self, emotion):
        self.emotion_id = Emotion[emotion].value

    def toJson(self):
        return {
            "id": str(self.id),
            "emotion": Emotion(self.emotion_id).name,
            "description": self.description,
            "hashtags": self.hashtags,
            "user_id": str(self.user_id),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    def __repr__(self):
        return "<Feeling(id='{}', emotion_id='{}', description='{}', hashtags='{}', user_id='{}', created_at='{}', updated_at='{}')>".format(
            self.id,
            self.emotion_id,
            self.description,
            self.hashtags,
            self.user_id,
            self.created_at,
            self.updated_at,
        )
