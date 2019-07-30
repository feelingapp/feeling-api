import os
import time

import jwt


class AccessToken:
    # Equivalent to 2 hours
    TOKEN_LIFE = 7200

    token = None

    def __init__(self, token):
        self.token = token

    def build(self, user_id):
        expires_in = int(time.time()) + self.TOKEN_LIFE

        payload = {"sub": str(user_id), "exp": expires_in}

        self.token = jwt.encode(
            payload, os.getenv("SECRET_KEY"), algorithm="HS256"
        ).decode("utf-8")

    @property
    def expires_in(self):
        return self.TOKEN_LIFE

    @property
    def has_expired(self, token):
        payload = self.payload(token)

        return payload["expires_in"] + self.TOKEN_LIFE < time.time()

    @property
    def payload(self, token):
        return jwt.decode(token, os.getenv("SECRET_KEY"), algorithm="HS256")
