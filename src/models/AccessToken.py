import os
import time

import jwt


class AccessToken:
    # Equivalent to 2 hours
    TOKEN_LIFE = 7200

    def __init__(self, token=None):
        self.token = token

    def create(self, user_id):
        expires_in = int(time.time()) + self.TOKEN_LIFE
        payload = {"sub": str(user_id), "exp": expires_in}

        self.token = jwt.encode(
            payload, os.getenv("SECRET_KEY"), algorithm="HS256"
        ).decode("utf-8")

    @property
    def expires_in(self):
        return self.TOKEN_LIFE

    def has_expired(self):
        return self.payload["exp"] + self.TOKEN_LIFE < time.time()

    @property
    def payload(self):
        return jwt.decode(self.token, os.getenv("SECRET_KEY"), algorithm="HS256")
