import os
import re
from urllib import parse
from urllib.parse import urlencode

import jwt

from src.models import AuthorizationCode, Client, User
from src.utils.decorators import database, validate

sign_in_schema = {
    "type": "object",
    "properties": {
        "body": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "pattern": r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                },
                "password": {"type": "string"},
                "response_type": {"type": "string"},
                "client_id": {"type": "string"},
                "redirect_uri": {"type": "string"},
                "code_challenge_method": {"type": "string"},
                "code_challenge": {"type": "string"},
            },
            "required": [
                "email",
                "password",
                "response_type",
                "client_id",
                "redirect_uri",
                "code_challenge_method",
                "code_challenge",
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
                        "message": "The redirect URI was not found",
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
                "password": {"type": "string", "minLength": 8},
            },
            "required": ["first_name", "last_name", "password"],
        }
    },
}


@validate(register_schema)
def register(event, context):
    password = event["body"]["password"]

    if not (
        any(map(str.isdigit, password))
        and any(map(str.islower, password))
        and any(map(str.isupper, password))
    ):
        return {
            "statusCode": 400,
            "body": {
                "errors": [
                    {
                        "type": "valildation_error",
                        "message": "The password must contain a number, a lowercase letter and an uppercase letter",
                    }
                ]
            },
        }

    return sign_in(event, context, session=None, register=True)
