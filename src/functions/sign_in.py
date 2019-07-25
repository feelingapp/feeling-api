import json
import os
import re
from urllib import parse
from urllib.parse import urlencode

import jwt
from sqlalchemy.orm import mapper

from src.models import Client, User
from src.models.AuthorizationCode import AuthorizationCode
from src.utils.decorators import database, parse_parameters, validate

STATE_LENGTH = 10
AUTHORIZATION_CODE_EXPIRY_TIME = 3600
CODE_CHALLENGE_METHOD = "SHA256"

body_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
        "response_type": {"type": "string"},
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
    response_type = body["response_type"]
    redirect_uri = body["redirect_uri"]
    code_challenge_method = body["code_challenge_method"]
    code_challenge = body["code_challenge"]
    code_challenge_token = body["code_challenge_token"]

    if response_type != "code":
        return {
            "statusCode": 400,
            "body": {
                "errors": [
                    {
                        "type": "invalid_response_type",
                        "message": "Only the authorization code grant type is supported",
                    }
                ]
            },
        }

    if code_challenge_method != CODE_CHALLENGE_METHOD:
        return {
            "statusCode": 400,
            "body": {
                "errors": [
                    {
                        "type": "invalid_code_challenge_method",
                        "message": "Only SHA256 is supported for the code challenge method",
                    }
                ]
            },
        }

    try:
        token_payload = jwt.decode(
            code_challenge_token, os.getenv("SECRET_KEY"), algorithms=["HS256"]
        )
    except:
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
        return {
            "statusCode": 400,
            "body": {
                "error": [
                    {
                        "type": "invalid_client_id",
                        "message": "The client ID is not valid",
                    }
                ]
            },
        }

    if client.redirect_uri != redirect_uri:
        return {
            "statusCode": 400,
            "body": {
                "error": [
                    {
                        "type": "invalid_redirect_uri",
                        "message": "The redirect_uri was not found",
                    }
                ]
            },
        }

    user = session.query(User).filter(User.email == email).first()

    if not user:
        return {
            "statusCode": 404,
            "body": {
                "error": [
                    {
                        "type": "account_not_found",
                        "message": "An account does not exist with the email provided",
                    }
                ]
            },
        }

    if not user.verify_password(password):
        return {
            "statusCode": 401,
            "body": {
                "error": [
                    {
                        "type": "wrong_password",
                        "message": "The password given is incorrect",
                    }
                ]
            },
        }

    # Delete existing user's authorization code if it exists
    session.query(AuthorizationCode).filter_by(user_id=user.id).delete()

    authorization_code = AuthorizationCode(
        user.id, client_id, code_challenge_method, code_challenge, redirect_uri
    )
    session.add(authorization_code)
    session.commit()

    return {
        "statusCode": 200,
        "body": {
            "authorization_code": authorization_code,
            "expires_in": AUTHORIZATION_CODE_EXPIRY_TIME,
            "redirect_uri": redirect_uri,
        },
    }
