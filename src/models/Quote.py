from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from models import BaseModel


class Quote(BaseModel):
    __tablename__ = "quotes"

    quote = Column(String, nullable=False)
    author = Column(String, nullable=False)
    emotion_id = Column(UUID, ForeignKey("emotions.id"), nullable=False)

    def __init__(self, quote, author, emotion):
        self.quote = quote
        self.author = author
        self.emotion = emotion

    def __repr__(self):
        return "<Quote(id='{}', quote='{}', author='{}', emotion='{}', created_at='{}', updated_at='{}')>".format(
            self.id,
            self.quote,
            self.author,
            self.emotion,
            self.created_at,
            self.updated_at,
        )
