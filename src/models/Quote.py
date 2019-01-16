from sqlalchemy import Column, ForeignKey, Integer, String

from src.consts import Emotion
from src.models import BaseModel


class Quote(BaseModel):
    __tablename__ = "quotes"

    quote = Column(String, nullable=False)
    author = Column(String, nullable=False)
    emotion_id = Column(Integer, ForeignKey("emotions.id"), nullable=False)

    def __init__(self, quote, author, emotion: Emotion):
        self.quote = quote
        self.author = author
        self.emotion_id = emotion.value

    @property
    def emotion(self):
        return Emotion(self.emotion_id)

    def __repr__(self):
        return "<Quote(id='{}', quote='{}', author='{}', emotion='{}', created_at='{}', updated_at='{}')>".format(
            self.id,
            self.quote,
            self.author,
            self.emotion,
            self.created_at,
            self.updated_at,
        )
