from sqlalchemy import Column, String

from models import BaseModel


class Client(BaseModel):
    __tablename__ = "clients"

    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Client(id='{}', name='{}', created_at='{}', updated_at='{}')>".format(
            self.id, self.name, self.created_at, self.updated_at
        )
