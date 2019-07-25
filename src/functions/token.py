import json
import os
from datetime import datetime, timedelta

import jwt

from src.models import AuthorizationCode, RefreshToken
from src.utils.decorators import database, validate

# TODO: finish schema
schema = {}


@validate(schema)
@database
def token(event, context, session):
    body = event["body"]
    grant_type = body["grant_type"]

    if grant_type == "authorization_code":
        return authorization_code_grant(event, session)

    if grant_type == "refresh_token":
        return refresh_token_grant(event, session)

    return {
        "statusCode": 400,
        "body": {
            "errors": [
                {
                    "type": "invalid_grant_type",
                    "message": "Only authorization_code or refresh_token grant types are supported",
                }
            ]
        },
    }


# TODO: finish schema
authorization_code_grant_schema = {}


@validate(authorization_code_grant_schema)
def authorization_code_grant(event, session):
    body = json.loads(event["body"])

    code = body["code"]
    code_verifier = body["code_verifier"]
    redirect_uri = body["redirect_uri"]
    client_id = body["client_id"]

    authorization_code = (
        session.query(AuthorizationCode)
        .filter(AuthorizationCode.authorization_code == code)
        .first()
    )

    # TODO: fix things
    if not authorization_code:
        return {
            "statusCode": 400,
            "body": {
                "errors": [
                    {
                        "type": "invalid_authorization_code",
                        "message": "The authorization code is invalid",
                    }
                ]
            },
        }

    if not client_id == str(authorization_code.client_id):
        return {
            "statusCode": 401,
            "body": {
                "errors": [
                    {
                        "type": "invalid_client_id",
                        "message": "The client ID is not invalid",
                    }
                ]
            },
        }

    if not redirect_uri == authorization_code.redirect_uri:
        return {
            "statusCode": 401,
            "body": {
                "errors": [
                    {
                        "type": "invalid_redirect_uri",
                        "message": "The redirect URI is not invalid",
                    }
                ]
            },
        }

    if not authorization_code.verify_code_challenge(code_verifier):
        return {
            "statusCode": 400,
            "body": {
                "errors": [
                    {
                        "type": "invalid_code_verifier",
                        "message": "The code verifier is not invalid",
                    }
                ]
            },
        }

    # TODO: find a correct format and type for expiry_time
    expiry_time = "in 30 mins"

    payload = {
        "user_id": str(authorization_code.user_id),
        "expiry_time": str(expiry_time),
    }

    jwtoken = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode(
        "utf-8"
    )

    refresh_token = RefreshToken(
        authorization_code.user_id, authorization_code.client_id
    )
    session.add(refresh_token)
    session.commit()

    return {
        "statusCode": 200,
        "body": {"access_token": jwtoken, "refresh_token": refresh_token.token},
    }


refresh_token_grant_schema = {}


@validate(refresh_token_grant_schema)
def refresh_token_grant(client_params, session):
    refresh_token = client_params["refresh_token"]
    hashed_refresh_token = RefreshToken.hash_token(refresh_token)
    db_refresh_tokens = session.query(RefreshToken).filter(
        RefreshToken.token_hash == hashed_refresh_token
    )
    if not db_refresh_tokens.count():
        return {
            "statusCode": 400,
            "body": {
                "errors": [
                    {
                        "type": "invalid_refresh_token",
                        "message": "The refresh token is not invalid",
                    }
                ]
            },
        }

    db_refresh_token = db_refresh_tokens.one()
    if db_refresh_token.expired():
        return {
            "statusCode": 401,
            "body": {
                "errors": [
                    {
                        "type": "expired_refresh_token",
                        "message": "The refresh token has expired",
                    }
                ]
            },
        }

    session.delete(db_refresh_token)

    # TODO: find a correct format and type for expiry_time
    expiry_time = "in 2 weeks"

    jwt_payload = {"user_id": db_refresh_token.user_id, "expiry_time": str(expiry_time)}

    jwtoken = jwt.encode(
        jwt_payload, os.getenv("SECRET_KEY"), algorithm="HS256"
    ).decode("utf-8")

    # if an overlap ever happens with the refresh token it means that it is not secure enough
    refresh_token = RefreshToken(db_refresh_token.user_id, db_refresh_token.client_id)
    session.add(db_refresh_token)
    session.commit()

    return {
        "statusCode": 200,
        "body": {"access_token": jwtoken, "refresh_token": refresh_token.token},
    }
