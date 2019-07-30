import os
import re
from urllib import parse
from urllib.parse import urlencode

import jwt
from sqlalchemy.orm import mapper

from src.models import AuthorizationCode, Client, User
from src.utils.decorators import database, validate

STATE_LENGTH = 10

sign_in_schema = {
    "type": "object",
    "properties": {
        "body": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "password": {"type": "string"},
                "response_type": {"type": "string"},
                "client_id": {"type": "string"},
                "redirect_uri": {"type": "string"},
                "code_challenge_method": {"type": "string"},
                "code_challenge": {"type": "string"},
                "code_challenge_token": {"type": "string"},
                "state": {
                    "type": "string",
                    "minLength": STATE_LENGTH,
                    "maxLength": STATE_LENGTH,
                },
            },
            "required": [
                "email",
                "password",
                "response_type",
                "client_id",
                "redirect_uri",
                "code_challenge_method",
                "code_challenge",
                "code_challenge_token",
                "state",
            ],
        }
    },
}


@validate(sign_in_schema)
@database
def sign_in(event, context, session, register=False):
    body = event["body"]

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

    if code_challenge_method != AuthorizationCode.CODE_CHALLENGE_METHOD:
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
                "errors": [
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
                "errors": [
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
                "errors": [
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
                "errors": [
                    {
                        "type": "invalid_redirect_uri",
                        "message": "The redirect_uri was not found",
                    }
                ]
            },
        }

    user = session.query(User).filter_by(email=email).first()

    if register:
        if user and user.verified:
            return {
                "statusCode": 400,
                "body": {
                    "errors": [
                        {
                            "type": "account_email_exists",
                            "message": "An account with the email provided already exists",
                        }
                    ]
                },
            }

        first_name = body["first_name"]
        last_name = body["last_name"]

        # Create a new account
        user = User(email, password, first_name, last_name)
        session.add(user)
        session.commit()
    else:
        if not user:
            return {
                "statusCode": 404,
                "body": {
                    "errors": [
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
                    "errors": [
                        {
                            "type": "wrong_password",
                            "message": "The password given is incorrect",
                        }
                    ]
                },
            }

    # Delete existing user's authorization code if it exists
    session.query(AuthorizationCode).filter_by(user_id=user.id).delete()

    # Create a new authorization code
    authorization_code = AuthorizationCode(
        user.id, client_id, code_challenge, code_challenge_method
    )
    session.add(authorization_code)
    session.commit()

    return {
        "statusCode": 200,
        "body": {
            "authorization_code": authorization_code.code,
            "expires_in": authorization_code.expires_in,
        },
    }


register_schema = {
    "type": "object",
    "properties": {
        "body": {
            "type": "object",
            "properties": {
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
            },
            "required": ["first_name", "last_name"],
        }
    },
}


@validate(register_schema)
def register(event, context):
    return sign_in(event, context, session=None, register=True)
