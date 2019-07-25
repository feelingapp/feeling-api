import json
from datetime import datetime, timedelta

import jwt

from src.models import AuthorizationCode, RefreshToken

# take this from a file after testing
from src.utils.decorators import database, parse_parameters, validate

# TODO: finish schema
schema = {}


@validate(schema)
@database
def get_token(event, context, session):
    client_parameters = parse_parameters(event["body"])
    grant_type = client_parameters["grant_type"]
    if grant_type == "authorization_code":
        return auth_code_flow(event, session)
    elif grant_type == "refresh_token":
        return refresh_flow(event, session)
    else:
        # TODO: insert an error log as input sanitization has failed or something fishy is happening
        return {"statusCode": 400, "body": {"error": "what'ya doing there buddy"}}


# TODO: finish schema
auth_schema = {}


@validate(body_sc=auth_schema)
def auth_code_flow(event, session):
    body = json.loads(event["body"])

    code = body["code"]
    code_verifier = body["code_verifier"]
    redirect_uri = body["redirect_uri"]
    client_id = body["client_id"]

    db_code = (
        session.query(AuthorizationCode)
        .filter(AuthorizationCode.authorization_code == code)
        .first()
    )

    # TODO: fix things
    if not db_code:
        return {"statusCode": 403, "error": "invalid authorization code"}

    if not client_id == str(db_code.client_id):
        return {"statusCode": 403, "error": "incorrect client ID"}

    if not redirect_uri == db_code.redirect_uri:
        return {"statusCode": 403, "error": "incorrect redirect URI"}

    if not db_code.verify_code_challenge(code_verifier):
        return {"statusCode": 403, "error": "incorrect code verifier"}

    # TODO: find a correct format and type for expiry_time
    expiry_time = "in 30 mins"

    payload = {"user_id": str(db_code.user_id), "expiry_time": str(expiry_time)}

    jwtoken = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode(
        "utf-8"
    )

    refresh_token = generate_refresh_token()

    db_refresh_token = RefreshToken(refresh_token, db_code.user_id, db_code.client_id)

    session.add(db_refresh_token)
    session.commit()

    return {
        "statusCode": 200,
        "body": {"access_token": jwtoken, "refresh_token": refresh_token},
    }


refresh_schema = {}


# TODO: input schema validation here
@validate(body_sc=refresh_schema)
def refresh_flow(client_params, session):
    refresh_token = client_params["refresh_token"]
    hashed_refresh_token = RefreshToken.hash_token(refresh_token)
    db_refresh_tokens = session.query(RefreshToken).filter(
        RefreshToken.token_hash == hashed_refresh_token
    )
    if not db_refresh_tokens.count():
        # TODO: fix the statusCode
        return {
            "statusCode": 300,
            "body": {"error": "that refresh token does not exist"},
        }
    # TODO: create a second table of previous refresh tokens or add another field so that we can catch potential breaches

    db_refresh_token = db_refresh_tokens.one()
    if db_refresh_token.expired():
        # TODO: fix the statusCode
        return {
            "statusCode": 300,
            "body": {
                "error": "the token has expired, to get another you must get an "
                "authorization code"
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
    refresh_token = generate_refresh_token()
    db_refresh_token = RefreshToken(
        refresh_token, db_refresh_token.user_id, db_refresh_token.client_id
    )

    session.add(db_refresh_token)

    session.commit()
    return {
        "statusCode": 200,
        "body": {"access_token": jwtoken, "refresh_token": refresh_token},
    }
