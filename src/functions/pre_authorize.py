import os

import jwt

from src.models.Client import Client
from src.utils.decorators import database, validate


schema = {
    "type": "object",
    "properties": {
        "queryStringParameters": {
            "type": "object",
            "properties": {"code_challenge": {"type": "string"}},
            "required": ["code_challenge"],
        }
    },
}


@database
@validate(schema)
def authorize(event, context, session):
    code_challenge = event["queryStringParameters"]["code_challenge"]

    token_payload = {"code_challenge": code_challenge}

    token = jwt.encode(token_payload, os.getenv("SECRET_KEY"), algorithm="HS256")

    return {"statusCode": 200, "body": {"code_challenge_token": token}}
