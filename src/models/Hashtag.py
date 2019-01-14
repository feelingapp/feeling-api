from sqlalchemy import Column, String

from src.models import BaseModel


class Hashtag(BaseModel):
    __tablename__ = "hashtags"

    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Hashtag(id='{}', name='{}', created_at='{}', updated_at='{}')>".format(
            self.id, self.name, self.created_at, self.updated_at
        )
