import json
import os
import re
from urllib import parse

import jwt
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import mapper
from urllib.parse import urlencode
from validators import url

from src.models import Client
from src.models import User
from src.models.AuthorizationCode import AuthorizationCode
from src.utils.decorators import database, validate, parse_parameters
from src.functions.authorize import AUTH_PRIVATE_KEY

STATE_LENGTH = 10
AUTHORIZATION_CODE_EXPIRY_TIME = 3600

body_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
        "redirect_uri": {"type": "string"},
        "code_challenge_method": {"type": "string"},
        "code_challenge": {"type": "string"},
        "state": {
            "type": "string",
            "minLength": STATE_LENGTH,
            "maxLength": STATE_LENGTH,
        },
    },
    "required": [
        "email",
        "password",
        "client_id",
        "response_type",
        "redirect_uri",
        "code_challenge_method",
        "code_challenge",
        "state",
    ],
}


@validate(body_sc=body_schema)
@database
def sign_in(event, context, session):
    body = json.loads(event["body"])

    email = body["email"]
    password = body["password"]
    client_id = body["client_id"]
    redirect_uri = body["redirect_uri"]
    code_challenge_method = body["code_challenge_method"]
    code_challenge = body["code_challenge"]
    code_challenge_token = body["code_challenge_token"]

    try:
        token_payload = jwt.decode(
            code_challenge_token, os.getenv("SECRET_KEY"), algorithms=["HS256"]
        )
    # TODO: add extra catches for different token errors
    except jwt.exceptions.InvalidSignatureError as error:
        return {
            "statusCode": 400,
            "body": {
                "error": [
                    {
                        "type": "invalid_code_challenge_token",
                        "message": "The code challenge token is invalid",
                    }
                ]
            },
        }

    if not token_payload["code_challenge"] == code_challenge:
        return {
            "statusCode": 400,
            "body": {
                "error": [
                    {
                        "type": "incorrect_code_challenge",
                        "message": "The code_challenge is incorrect",
                    }
                ]
            },
        }

    client = session.query(Client).filter(Client.id == client_id).first()
    if not client:
        return {"statusCode": 403, "body": {"error": "the client ID is not valid"}}

    if not client.verify_URI(redirect_uri):
        return {"statusCode": 403, "message": "client_id or redirect_uri is incorrect"}

    user = session.query(User).filter(User.email == email).first()

    if not user:
        return {"statusCode": 403, "message": "email or password is incorrect"}

    if not user.verify_password(password):
        return {"statusCode": 403, "message": "email or password is incorrect"}

    # Delete existing user's authorization code if it exists
    session.query(AuthorizationCode).filter_by(user_id == user.id).delete()

    code = AuthorizationCode(
        user.id, client_id, code_challenge_method, code_challenge, redirect_uri
    )

    url_parameters = urlencode({"authorization_code": str(code.authorization_code)})

    complete_redirect_uri = "https://{}?={}".format(redirect_uri, url_parameters)

    session.add(code)
    session.commit()



    return {
        "statusCode": 302,
        "header": {
            "Location": complete_redirect_uri
        }
    }
