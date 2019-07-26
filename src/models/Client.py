import re

from sqlalchemy import Column, String

from src.models import BaseModel


class Client(BaseModel):
    __tablename__ = "clients"

    name = Column(String, nullable=False)
    redirect_uri = Column(String, nullable=False)

    def __init__(self, name, redirect_uri):
        self.name = name
        self.redirect_uri = redirect_uri

    def __repr__(self):
        return "<Client(id='{}', name='{}', redirect_uri='{}' created_at='{}', updated_at='{}')>".format(
            self.id, self.name, self.redirect_uri, self.created_at, self.updated_at
        )

