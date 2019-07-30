import secrets
import string
import time
from base64 import b64encode
from hashlib import sha256

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from src.models import BaseModel


class AuthorizationCode(BaseModel):
    __tablename__ = "authorization_codes"

    CODE_LENGTH = 48
    CODE_LIFE = 300
    CODE_CHALLENGE_METHOD = "SHA256"

    code = Column(String(CODE_LENGTH), nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    issue_time = Column(Integer, nullable=False, default=lambda: int(time.time()))
    code_challenge = Column(String, nullable=False)
    code_challenge_method = Column(String, nullable=False)

    client = relationship("Client")

    def __init__(self, user_id, client_id, code_challenge, code_challenge_method):
        self.code = self.generate_code()
        self.user_id = user_id
        self.client_id = client_id
        self.code_challenge = code_challenge
        self.code_challenge_method = code_challenge_method

    def __repr__(self):
        return "<AuthorizationCode(id='{}', code='{}', user_id='{}', client_id='{}', issue_time='{}', code_challenge='{}', code_challenge_method='{}', created_at='{}', updated_at='{}')>".format(
            self.id,
            self.code,
            self.user_id,
            self.client_id,
            self.issue_time,
            self.code_challenge,
            self.code_challenge_method,
            self.created_at,
            self.updated_at,
        )

    @property
    def expires_in(self):
        return self.CODE_LIFE

    # TODO: test and verify this is the right way to do this
    def verify_code_challenge(self, verifier):
        if self.code_challenge_method != "SHA256":
            return False

        hashed_obj = sha256(verifier.encode())
        b64encoded_string = b64encode(hashed_obj.digest()).decode(encoding="UTF-8")

        return b64encoded_string == self.code_challenge

    def generate_code(self):
        """Generates an authorization code"""

        return "".join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(self.CODE_LENGTH)
        )

    def has_expired(self):
        """Check if the authorization code has expired"""

        return self.issue_time + self.CODE_LIFE < time.time()
