from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.ext.compiler import compiles
from src.models.Base import BaseModel
from sqlalchemy.sql import expression
from hashlib import sha256
import secrets
from base64 import b64encode


class utc_in_30(expression.FunctionElement):
    type = DateTime()


@compiles(utc_in_30, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP) + (30 * interval '1 minute')"



class AuthorizationCode(BaseModel):
    __tablename__ = "AuthorizationCodes"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    authorization_code = Column(String, nullable=False, unique=True)
    code_challenge_method = Column(String, nullable=False)
    code_challenge = Column(String, nullable=False)
    redirect_uri = Column(String, nullable=False)
    expires_at = Column(DateTime(), nullable=False, server_default=utc_in_30(), onupdate=utc_in_30())


    def __init__(self, user_id, code_challenge_method, code_challenge, redirect_uri):
        self.user_id = user_id
        self.code_challenge_method = code_challenge_method
        self.code_challenge = code_challenge
        # TODO: need to add a rerun in the tiny possibility there is a duplicate
        self.authorization_code = self.generate_auth_code()
        self.redirect_uri = redirect_uri
        self.expires_at = utc_in_30()

    def __repr__(self):
        return "<AuthorizationCodes(user_id='{}', code_challenge_method='{}', " \
               "code_challenge='{}', authorization_code='{}', redirect_uri='{}'," \
               " created_at='{}', updated_at='{}')>".format(
               self.user_id, self.code_challenge_method,
               self.code_challenge, self.authorization_code, self.redirect_uri,
               self.created_at, self.updated_at
        )

    def verify_code_challenge(self, verifier):
        # TODO: find a way to clean this up
        if self.code_challenge_method == "S256":
            # TODO: test and verify this is the right way to do this
            hashed_obj = sha256(verifier)
            b64encoded_string = b64encode(hashed_obj.digest()).decode(encoding="UTF-8")
            if b64encoded_string == self.code_challenge:
                return True
            else:
                return False


    # TODO: double check secrets is a safe enough library
    def generate_auth_code(self):
        len_code = 40
        code = ''.join(secrets.choice(String.ascii_letters + String.digits) for _ in range(len_code))
        return code
