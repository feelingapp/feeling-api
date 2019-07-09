import string

from models.AuthorizationCode import AuthorizationCode
from models import RefreshToken
from datetime import datetime, timedelta
import secrets
import jwt

# take this from a file after testing
from utils.decorators import database, validate, parse_parameters

PRIVATE_KEY = "privatekey"

schema = {}
# needs to validate the request
@validate(schema)
@database
def token(event, context, session):

    client_parameters = event['queryStringParameters']
    grant_type = event['grant_type']
    if grant_type == "authorization_code":
        return auth_code_flow(event, session)
    elif grant_type == "refresh_token":
        return refresh_flow(event, session)
    else:
        # TODO: insert an error log as input sanitization has failed or something fishy is happening
        return {"statusCode":400, "body":{"error": "what'ya doing there buddy"}}


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
        return {"statusCode":403, "error" : "invalid authorisation code"}

    db_code = db_codes.one()

    if not client_id == db_code.client_id:
        return {"statusCode":403, "error": "incorrect client ID"}


    if not redirect_uri == db_code.redirect_uri:
        return {"statusCode":403, "error": "incorrect redirect URI"}


    if not db_code.verify_code_challenge(code_verifier):
        return {"statusCode":403, "error": "incorrect code verifier"}


    payload = {"user_id" : db_code.user_id, "expiry_time" : expiry_time}

    jwtoken = jwt.encode(payload, PRIVATE_KEY, algorithm='HS256').decode('utf-8')

    refresh_token = generate_refresh_token()

    db_refresh_token = RefreshToken(refresh_token,db_code.user_id, db_code.client_id)


    return {"statusCode": 200, "body": {"token": jwtoken}}

    # user_id = None
    #
    # if "code" in client_parameters.keys():
    #     param_auth_code = client_parameters['code']
    #     # potentially rename codes and code
    #     codes = session.query(AuthorizationCode.authorization_code == param_auth_code)
    #     if len(codes) == 0:
    #         # should I state whether the auth code is correct or not or authcode or challenge is incorrect
    #         return {"statusCode": 401, "body" : {"error" : "incorrect_authorization_code"}}
    #
    #     code = codes[0]
    #     code_challenge_method = code.code_challenge_method
    #     code_challenge = code.code_challenge
    #     code_verifier = client_parameters['code_verifier']
    #
    #     code_verifier_hashed = ""
    #
    #     # do different hashes here
    #     if code_challenge_method == "sha256":
    #         # needs renaming potentially
    #         code_verifier_hashed = hashlib.pbkdf2_hmac('sha256', code_verifier, b'', 100000)
    #         code_verifier_hashed = binascii.hexlify(code_verifier_hashed)
    #
    #
    #     if code_verifier_hashed != code_challenge:
    #         return {"statusCode": 401, "body": {"error": "incorrect_code_verifier"}}
    #
    #
    # elif "refresh_token" in client_parameters.keys():
    #     return
    #
    # # produce the token
    # user_id = code.user_id
    # client_id = client_parameters['client_id']
    #
    # current_time = datetime.utcnow()
    # expiry_time = current_time.hour + timedelta(hours=1)
    #
    # payload = {"user_id" : user_id, "expiry_time" : expiry_time}
    #
    # jwtoken = jwt.encode(payload, PRIVATE_KEY, algorithm='HS256')
    #
    # refresh_token = generate_refresh_token()
    #
    # db_refresh_token = RefreshToken(refresh_token, user_id, client_id)
    # session.add(db_refresh_token)
    # session.commit()
    #
    # return {"statusCode": 200, "body": {"token" : jwtoken, "refresh_token" : refresh_token}}




refresh_schema = {}
@validate(refresh_schema)
def refresh_flow(client_params, session):
    # TODO: input shcema validation here
    refresh_token = client_params["refresh_token"]
    return {"statusCode": 200, "body": {"token": "no token yet, my dudes"}}


def generate_refresh_token():
    len_code = 20
    # TODO: look if there is a better library than secrets and if so use it
    code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(len_code))
    return code
