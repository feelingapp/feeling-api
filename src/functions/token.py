import os
from datetime import datetime, timedelta

from src.models import AccessToken, AuthorizationCode, RefreshToken
from src.utils.decorators import database, validate, token_required

schema = {
    "type": "object",
    "properties": {
        "body": {
            "type": "object",
            "properties": {
                "grant_type": {"type": "string"},
                "state": {"type": "string"},
            },
            "required": ["grant_type", "state"],
        }
    },
}


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


authorization_code_grant_schema = {
    "type": "object",
    "properties": {
        "body": {
            "type": "object",
            "properties": {
                "code": {"type": "string"},
                "code_verifier": {"type": "string"},
                "redirect_uri": {"type": "string"},
                "client_id": {"type": "string"},
            },
            "required": ["grant_type", "code_verifier", "redirect_uri", "client_id"],
        }
    },
}


@validate(authorization_code_grant_schema)
def authorization_code_grant(event, session):
    body = event["body"]

    code = body["code"]
    code_verifier = body["code_verifier"]
    redirect_uri = body["redirect_uri"]
    client_id = body["client_id"]
    state = body["state"]

    authorization_code = session.query(AuthorizationCode).filter_by(code=code).first()

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

    if not redirect_uri == authorization_code.client.redirect_uri:
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

    access_token = AccessToken(authorization_code.user_id)

    refresh_token = RefreshToken(
        authorization_code.user_id, authorization_code.client_id
    )

    session.delete(authorization_code)
    session.add(refresh_token)
    session.commit()

    return {
        "statusCode": 200,
        "body": {
            "access_token": access_token.token,
            "expires_in": access_token.expires_in,
            "token_type": "bearer",
            "refresh_token": refresh_token.token,
            "state": state,
        },
    }


refresh_token_grant_schema = {
    "type": "object",
    "properties": {
        "body": {
            "type": "object",
            "properties": {"refresh_token": {"type": "string"}},
            "required": ["refresh_token"],
        }
    },
}

# TODO: Figure out reissuing refresh tokens
@token_required
@validate(refresh_token_grant_schema)
def refresh_token_grant(event, session):
    body = event["body"]

    refresh_token = body["refresh_token"]
    state = body["state"]

    hashed_refresh_token = RefreshToken.hash_token(refresh_token)

    db_refresh_token = (
        session.query(RefreshToken).filter_by(token_hash=hashed_refresh_token).first()
    )

    if not db_refresh_token:
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

    if db_refresh_token.has_expired():
        session.delete(db_refresh_token)

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

    access_token = AccessToken(db_refresh_token.user_id)

    refresh_token = RefreshToken(db_refresh_token.user_id, db_refresh_token.client_id)
    session.add(refresh_token)
    session.commit()

    return {
        "statusCode": 200,
        "body": {
            "access_token": access_token.token,
            "expires_in": access_token.expires_in,
            "token_type": "bearer",
            "refresh_token": refresh_token.token,
            "state": state,
        },
    }
