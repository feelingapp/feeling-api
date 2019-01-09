from sqlalchemy import Column, String

from models import BaseModel


class Emotion(BaseModel):
    __tablename__ = "emotions"

    emotion = Column(String, nullable=False)
    emoji = Column(String, nullable=False)

    def __init__(self, emotion, emoji):
        self.emotion = emotion
        self.emoji = emoji

    def __repr__(self):
        return "<Emotion(id='{}', emotion='{}', emoji='{}', created_at='{}', updated_at='{}')>".format(
            self.id, self.emotion, self.emoji
        )
