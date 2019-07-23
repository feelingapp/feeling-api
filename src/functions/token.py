import string

from src.models.AuthorizationCode import AuthorizationCode
from src.models import RefreshToken
from datetime import datetime, timedelta
import secrets
import jwt

# take this from a file after testing
from src.utils.decorators import database, validate, parse_parameters

PRIVATE_KEY = "privatekey"

# TODO: finish schema
schema = {}
# needs to validate the request
@validate(schema)
@database
def token(event, context, session):

    client_parameters = parse_parameters(event['body'])
    grant_type = client_parameters['grant_type']
    if grant_type == "authorization_code":
        return auth_code_flow(event, session)
    elif grant_type == "refresh_token":
        return refresh_flow(event, session)
    else:
        # TODO: insert an error log as input sanitization has failed or something fishy is happening
        return {"statusCode":400, "body":{"error": "what'ya doing there buddy"}}


# TODO: finish schema
auth_schema = {}

@validate(auth_schema)
def auth_code_flow(event, session):
    post_body = parse_parameters(event["body"])

    code = post_body["code"]
    code_verifier = post_body["code_verifier"]
    redirect_uri = post_body["redirect_uri"]
    client_id = post_body["client_id"]

    db_codes = session.query(AuthorizationCode).filter(AuthorizationCode.authorization_code == code)

    if not db_codes.all():
        return {"statusCode":403, "error": "invalid authorisation code"}

    db_code = db_codes.one()

    if not client_id == str(db_code.client_id):
        return {"statusCode":403, "error": "incorrect client ID"}

    if not redirect_uri == db_code.redirect_uri:
        return {"statusCode":403, "error": "incorrect redirect URI"}

    if not db_code.verify_code_challenge(code_verifier):
        return {"statusCode":403, "error": "incorrect code verifier"}

    # TODO: find a correct format and type for expiry_time
    expiry_time = "in 30 mins"

    payload = {"user_id" : str(db_code.user_id), "expiry_time" : str(expiry_time)}

    jwtoken = jwt.encode(payload, PRIVATE_KEY, algorithm='HS256').decode('utf-8')

    refresh_token = generate_refresh_token()

    db_refresh_token = RefreshToken(refresh_token,db_code.user_id, db_code.client_id)

    session.add(db_refresh_token)
    session.commit()

    return {"statusCode": 200, "body": {"token": jwtoken, "refresh_token": refresh_token}}


refresh_schema = {}


@validate(refresh_schema)
def refresh_flow(client_params, session):
    # TODO: input schema validation here
    refresh_token = client_params["refresh_token"]
    hashed_refresh_token = RefreshToken.hash_token(refresh_token)
    session.query(RefreshToken).filter(RefreshToken.token_hash)
    return {"statusCode": 200, "body": {"token": "no token yet"}}


def generate_refresh_token():
    len_code = 20
    # TODO: look if there is a better library than secrets and if so use it
    code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(len_code))
    return code
