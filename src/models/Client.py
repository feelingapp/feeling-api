from sqlalchemy import Column, String

from src.models import BaseModel


class Client(BaseModel):
    __tablename__ = "clients"

    name = Column(String, nullable=False)
    redirect_rgx = Column(String, nullable=False)

    def __init__(self, name, redirect_rgx):
        self.name = name
        self.redirect_rgx = redirect_rgx

    def __repr__(self):
        return "<Client(id='{}', name='{}', redirect_rgx='{}' created_at='{}', updated_at='{}')>".format(
            self.id, self.name, self.redirect_rgx, self.created_at, self.updated_at
        )
