from jinja2 import Environment, FileSystemLoader
from src.jinjaobjects.params import params
from src.utils.decorators import database, validate
from src.models.Client import Client

STATE_LENGTH = 10

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


    print(client_id)
    print(response_type)
    print(redirect_uri)
    print(code_challenge_method)
    print(code_challenge)
    print(state)

    # TODO: check whether it's best to insert a URL regex for each client_id into the database to get cleaner code
    if not verify_client_id_URI(client_id,redirect_uri, session):
        # TODO: check the statusCode of the error message
        return {"statusCode": 400, "body":{"error":"the client ID is not valid"}}

    # if there are other response types in future then there should be code added here
    if response_type != "code":
        # TODO: check the statusCode for the error message
        return {"statusCode":400, "body":{"error":"only authorisation code grant flow is supported at this time"}}


    j2_env = Environment(loader=FileSystemLoader("templates"),
                         trim_blocks=True)

    parameters = params()
    parameters.redirect_uri = redirect_uri
    parameters.response_type = response_type
    parameters.code_challenge_method = code_challenge_method
    parameters.code_challenge = code_challenge
    parameters.client_id = client_id
    parameters.state = state

    j2_env.get_template('signin.html').render(
        params=parameters
    )

    webpage = j2_env.get_template('signin.html').render(params=parameters)

    return {"statusCode":200, "headers": {"Content-Type": "text/html"},"body":webpage}




# TODO verify URI
def verify_client_id_URI(id, uri, session):
    clients = session.query(Client.id == id)
    if clients:
        return True
    else:
        return False





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
