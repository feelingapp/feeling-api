from sqlalchemy import Column, String

from src.models import BaseModel


class Emotion(BaseModel):
    __tablename__ = "emotions"

    emotion = Column(String, nullable=False)

    def __init__(self, emotion):
        self.emotion = emotion

    def __repr__(self):
        return "<Emotion(id='{}', emotion='{}', created_at='{}', updated_at='{}')>".format(
            self.id, self.emotion, self.created_at, self.updated_at
        )
