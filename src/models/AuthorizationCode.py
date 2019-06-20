from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.ext.compiler import compiles
from models import BaseModel
from sqlalchemy.sql import expression
import secrets


class utc_in_30(expression.FunctionElement):
    type = DateTime()


@compiles(utc_in_30, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP) + (30 * interval '1 minute')"



class AuthorizationCode(BaseModel):
    __tablename__ = "emotions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    authorization_code = Column(String, nullable=False)
    code_challenge_method = Column(String, nullable=False)
    code_challenge = Column(String, nullable=False)
    expires_at = Column(DateTime(), nullable=False, server_default=utc_in_30(), onupdate=utc_in_30())


    def __init__(self, user_id, code_challenge_method, code_challenge):
        self.user_id = user_id
        self.code_challenge_method = code_challenge_method
        self.code_challenge = code_challenge
        self.authorization_code = self.generate_auth_code()
        self.expires_at = utc_in_30()

    def __repr__(self):
        return "<Emotion(id='{}', emotion='{}', emoji='{}', created_at='{}', updated_at='{}')>".format(
            self.id, self.emotion, self.emoji, self.created_at, self.updated_at
        )

    # TODO: double check secrets is a safe enough library
    def generate_auth_code(self):
        len_code = 40
        code = ''.join(secrets.choice(String.ascii_letters + String.digits) for _ in range(len_code))
        return code
