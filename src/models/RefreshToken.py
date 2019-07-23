from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from argon2 import PasswordHasher
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from hashlib import sha256

from src.models import BaseModel

# TODO: find somewhere to put this constant
# (14 DAYS IN MINUTES)
SECRET_SALT = "ASECRETBOI"
REFRESH_TOKEN_LIFE = "20160"
TOKEN_LIFE = "30"


class utc_valid_at(expression.FunctionElement):
    type = DateTime()


class utc_expires_at(expression.FunctionElement):
    type = DateTime()


@compiles(utc_valid_at, "postgresql")
def pg_utc_valid_at(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP) + ({} * interval '1 minute')".format(TOKEN_LIFE)


@compiles(utc_expires_at, "postgresql")
def pg_utc_expires_at(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP) + ({} * interval '1 minute')".format(REFRESH_TOKEN_LIFE)



class RefreshToken(BaseModel):
    __tablename__ = "refresh_token"

    token_hash = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    # TODO: make sure nothing needs to be done with creation order
    valid_at = Column(DateTime(), nullable=False, server_default=utc_valid_at())
    expires_at = Column(DateTime(), nullable=False, server_default=utc_expires_at())

    # TODO: confirm valid_at and and expires_at don't need to be put in here
    def __init__(self, token, user_id, client_id):
        self.token_hash = self.hash_token(token)
        self.user_id = user_id
        self.client_id = client_id

    def __repr__(self):
        return "<RefreshToken(id='{}', token_hash='{}', user_id='{}', client_id='{}', valid_at='{}', expires_at='{}' created_at='{}', updated_at='{}')>".format(
            self.id,
            self.token_hash,
            self.user_id,
            self.client_id,
            self.valid_at,
            self.expires_at,
            self.created_at,
            self.updated_at,
        )

    # TODO: verify that this is correct
    def hash_token(self, token):

        # TODO: use another hasher with salt because this won't work as there is nothing to identify the record with
        # e.g. if a user has a token how would he find it in the

        salted_string = SECRET_SALT + token
        return sha256(bytes(salted_string,'utf-8')).hexdigest()

    def verify_token(self, token):
        """Checks if a token matches with a hash"""

        return self.token_hash == self.hash_token(token)
