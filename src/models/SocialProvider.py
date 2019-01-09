from sqlalchemy import Column, String

from models import BaseModel


class SocialProvider(BaseModel):
    __tablename__ = "social_providers"

    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<SocialProvider(id='{}', name='{}', created_at='{}', updated_at='{}')>".format(
            self.id, self.name, self.created_at, self.updated_at
        )
