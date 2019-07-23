import json
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
# DEBUGGING LIBRARIES
import inspect


STATE_LENGTH=10


body_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
        "redirect_uri" : {"type": "string"},
        "code_challenge_method" : {"type": "string"},
        "code_challenge" : {"type": "string"},
        "state": {"type": "string", "minLength": STATE_LENGTH, "maxLength":STATE_LENGTH}
    },
    "required": ["email", "password","client_id", "response_type", "redirect_uri",
                 "code_challenge_method", "code_challenge", "state"]

}

@validate(body_sc=body_schema)
@database
def sign_in(event, context,session):
    post_body = parse_parameters(event["body"])
    email = post_body["email"]
    password = post_body["password"]
    client_id = post_body["client_id"]
    redirect_uri = post_body["redirect_uri"]
    code_challenge_method = post_body["code_challenge_method"]
    code_challenge = post_body["code_challenge"]
    code_challenge_token = post_body["code_challenge_token"]

    try:
        token_payload = jwt.decode(code_challenge_token,AUTH_PRIVATE_KEY, algorithms=['HS256'])
    #     TODO: add extra catches for different token errors
    except jwt.exceptions.InvalidSignatureError as e:
        return {"statusCode": 403, "message": "invalid code_challenge_token"}

    if not token_payload["code_challenge"] == code_challenge:
        return {"statusCode": 403, "message": "code_challenge_token doe not match code_challenge"}

    clients = session.query(Client).filter(Client.id == client_id)
    if not clients.all():
        return {"statusCode": 403, "body":{"error":"the client ID is not valid"}}

    client = clients.one()

    if not client.verify_URI(redirect_uri):
        return {"statusCode":403, "message":"client_id or redirect_uri is incorrect"}

    #TODO: need to guarantee python has not got strange string comparison stuff like javascript
    users = session.query(User).filter(User.email == email)

    if not users.all():
        return {"statusCode":403, "message":"email or password is incorrect"}

    user = users.one()

    if not user.verify_password(password):
        return {"statusCode": 403, "message": "email or password is incorrect"}

    # in the case of a client already having an authorization code the previous authorization code is discarded and a
    # new one is created
    user_owned_code = session.query(AuthorizationCode).filter(AuthorizationCode.user_id == user.id)
    if user_owned_code.count():
        session.delete(user_owned_code.one())

    code = AuthorizationCode(user.id, client_id, code_challenge_method, code_challenge, redirect_uri)

    # this is to stop possible DoS attacks if they find an exploit in the authorization codes which
    # would cause the below loop to loop forever, however that is very unlikely
    counter = 0

    # This is in the very unlikely event that two auth_codes overlap the counter is set to 10 as it would be near
    # impossible to get two overlapping codes
    while is_overlapping_code(session, code.authorization_code) and counter < 10:
        code.authorization_code = code.generate_auth_code()
        counter += 1


    url_parameters = urlencode({
        "authorisation_code": str(code.authorization_code)
    })

    complete_redirect_uri = "https://{}?={}".format(redirect_uri, url_parameters)

    j2_env = Environment(loader=FileSystemLoader("templates"),
                         trim_blocks=True)

    webpage = j2_env.get_template('redirect.html').render(redirect_uri=complete_redirect_uri)

    # the code is added to the database right at the end to make sure that we are not using the database when there is
    # an error in the code
    session.add(code)
    session.commit()

    return {"statusCode": 201, "headers": {"Content-Type": "text/html"},"body":webpage}



# Only to be run after everything has been validated by the client
# this function removes any previous codes the user had
# TODO: rename to something better
def rmv_old_codes(session, id):
    auth_codes = session.query(AuthorizationCode).filter(AuthorizationCode.user_id == id)
    if not auth_codes.all():
        return
    session.delete(auth_codes.one())

# TODO: potentially merge the function above into one
# If there is an overlapping code the function will True else Flase
def is_overlapping_code(session, code):
    codes = session.query(AuthorizationCode).filter(AuthorizationCode.authorization_code == code)
    if not codes.all():
        return False
    code = codes.one()
    if code.is_expired():
        session.delete(code)
        return False
    else:
        return True

