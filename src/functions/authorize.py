import jwt
from jinja2 import Environment, FileSystemLoader
import re
from src.jinjaobjects.params import params
from src.utils.decorators import database, validate
from src.models.Client import Client

STATE_LENGTH = 10

AUTH_PRIVATE_KEY = "secret_boi"

CODE_CHALLENGE_METHODS = ["SHA256"]

# TODO: use regex to check response_type, code_challenge_method
header_schema = {
    "type": "object",
    "properties": {
        "queryStringParameters" : {
            "type": "object",
            "properties" : {
                "client_id": {"type": "string"},
                "response_type": {"type": "string"},
                "redirect_uri" : {"type": "string"},
                "code_challenge_method" : {"type": "string"},
                "code_challenge" : {"type": "string"},
                "state": {"type": "string", "minLength": STATE_LENGTH, "maxLength":STATE_LENGTH}
            },
            "required": ["client_id", "response_type", "redirect_uri",
                         "code_challenge_method", "code_challenge", "state"]

        }
    }

}


# call /authorize with code_challenge
# infected browser then receives code_challenge in form hidden
# malware changes the code_challenge to seomthing it knows
# the user signs in and the browser gets given the auth_code
# the malware in the browser is now the only one to be able to use that auth_code as it knows the code_challenge


# call /authorize with code_challenge
# infected browser then receives code_challenge which is signed


# needs to validate the request
# this potentially causes issues as it allows anyone to insert as much as they want into the database
@database
@validate(header_sc=header_schema)
def authorize(event, context, session):
    # event is type dictionary
    client_parameters = event['queryStringParameters']
    client_id = client_parameters['client_id']
    response_type = client_parameters['response_type']
    redirect_uri = client_parameters['redirect_uri']
    code_challenge_method = client_parameters['code_challenge_method']
    code_challenge = client_parameters['code_challenge']
    state = client_parameters['state']

    # TODO: use the correct statusCode and check it's the response_type value
    if response_type != "authorization_code":
        return {"statusCode": 403, "error":{"only authorization_code flow is supported at the current time"}}

    # TODO: use the correct statusCode
    if code_challenge_method not in CODE_CHALLENGE_METHODS:
        return {"statusCode": 403, "body":{"error":"the code challenge method is not supported by our API; currently "
                                                   "only SHA256 is"}}

    # verifying the client_id exists
    clients = session.query(Client).filter(Client.id == client_id)
    if not clients.count():
        return {"statusCode": 403, "body":{"error":"the client ID is not valid"}}

    client = clients.one()

    if not client.verify_URI(redirect_uri):
        # TODO: check the statusCode of the error message
        return {"statusCode": 403, "body":{"error":"the redirect_uri is not valid"}}


    j2_env = Environment(loader=FileSystemLoader("templates"),
                         trim_blocks=True)


    # TODO: add an expiry time to the code_challenge tokens
    token_payload = {"code_challenge":code_challenge}

    token = jwt.encode(token_payload, AUTH_PRIVATE_KEY, algorithm='HS256').decode('utf-8')

    parameters = params()
    parameters.redirect_uri = redirect_uri
    parameters.response_type = response_type
    parameters.code_challenge_method = code_challenge_method
    parameters.code_challenge_token = token
    parameters.code_challenge = code_challenge
    parameters.client_id = client_id
    parameters.state = state

    j2_env.get_template('signin.html').render(
        params=parameters
    )

    webpage = j2_env.get_template('signin.html').render(params=parameters)

    return {"statusCode":200, "headers": {"Content-Type": "text/html"},"body":webpage}








# correct_param_names = verify_parameter_names(client_parameters)
# if not correct_param_names:
#     return {"statusCode": 400, "body": {"error" : "incorrect_parameters"}}
#
# allowed_connection = verify_redirect_address(client_parameters.addr)
# if not allowed_connection:
#     return {"statusCode": 400, }


# checks that the request is coming from an allowed app / address
# def verify_redirect_address(client_full_addr):
#     for alwd_address in ADDRESSES:
#         len_alwd_address = len(alwd_address)
#         client_sub_addr = client_full_addr[0:len_alwd_address]
#         if client_sub_addr == alwd_address:
#             return True
#     return False


# checks the parameters names are correct returns true if they are otherwise false
# def verify_parameter_names(parameters):
#     correct_param_names = set("client_id","response_type","redirect_uri","code_challenge_method","code_challenge","email","password")
#     set_parameters = set(parameters)
#     if set_parameters != correct_param_names:
#         return False
#     else:
#         return True


if __name__ == "__main__":
    authorize(None, None)
