from models import AuthorizationCode
from models import RefreshToken
from datetime import datetime, timedelta
import secrets
# use the pyJWT library
import jwt
# needs
import hashlib, binascii

# take this from a file after testing
PRIVATE_KEY = "privatekey"

# needs to validate the request
@database
def token(event, context, session):
    client_parameters = event['queryStringParameters']

    # validate query parameters here

    grant_type = client_parameters['grant_type']

    user_id = None

    if "code" in client_parameters.keys():
        param_auth_code = client_parameters['code']
        # potentially rename codes and code
        codes = session.query(AuthorizationCode.authorization_code == param_auth_code)
        if len(codes) == 0:
            # should I state whether the auth code is correct or not or authcode or challenge is incorrect
            return {"statusCode": 401, "body" : {"error" : "incorrect_authorization_code"}}

        code = codes[0]
        code_challenge_method = code.code_challenge_method
        code_challenge = code.code_challenge
        code_verifier = client_parameters['code_verifier']

        code_verifier_hashed = ""

        # do different hashes here
        if code_challenge_method == "sha256":
            # needs renaming potentially
            code_verifier_hashed = hashlib.pbkdf2_hmac('sha256', code_verifier, b'', 100000)
            code_verifier_hashed = binascii.hexlify(code_verifier_hashed)


        if code_verifier_hashed != code_challenge:
            return {"statusCode": 401, "body": {"error": "incorrect_code_verifier"}}


    elif "refresh_token" in client_parameters.keys():
        return

    # produce the token
    user_id = code.user_id
    client_id = client_parameters['client_id']

    current_time = datetime.utcnow()
    expiry_time = current_time.hour + timedelta(hours=1)

    payload = {"user_id" : user_id, "expiry_time" : expiry_time}

    jwtoken = jwt.encode(payload, PRIVATE_KEY, algorithm='HS256')

    refresh_token = generate_refresh_token()

    db_refresh_token = RefreshToken(refresh_token, user_id, client_id)
    session.add(db_refresh_token)
    session.commit()

    return {"statusCode": 200, "body": {"token" : jwtoken, "refresh_token" : refresh_token}}





def generate_refresh_token():
    len_code = 40

    # TODO: look if there is a better library than secrets and if so use it
    code = ''.join(secrets.choice(String.ascii_letters + String.digits) for _ in range(len_code))
    return code

    #     return a jwt

    #     if len(codes) > 1:
    #          report error





