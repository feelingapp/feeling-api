from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from models import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, default=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password

    def __repr__(self):
        return "<User(id='{}', first_name='{}' last_name='{}', email='{}', password_hash='{}', verified='{}', created_at='{}', updated_at='{}')>".format(
            self.id,
            self.first_name,
            self.last_name,
            self.email,
            self.password_hash,
            self.verified,
            self.created_at,
            self.updated_at,
        )
