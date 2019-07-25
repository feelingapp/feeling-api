import jwt
from jinja2 import Environment, FileSystemLoader
import re
from src.jinjaobjects.params import params
from src.utils.decorators import database, validate
from src.models.Client import Client

STATE_LENGTH = 10

AUTH_PRIVATE_KEY = "secret_boi"

CODE_CHALLENGE_METHOD = "SHA256"

# TODO: use regex to check response_type, code_challenge_method
# TODO: change
query_param_schema = {
    "type": "object",
    "properties": {
        "queryStringParameters": {
            "type": "object",
            "properties": {
                "client_id": {"type": "string"},
                "response_type": {"type": "string"},
                "redirect_uri": {"type": "string"},
                "code_challenge_method": {"type": "string"},
                "code_challenge": {"type": "string"},
                "state": {
                    "type": "string",
                    "minLength": STATE_LENGTH,
                    "maxLength": STATE_LENGTH,
                },
            },
            "required": [
                "client_id",
                "response_type",
                "redirect_uri",
                "code_challenge_method",
                "code_challenge",
                "state",
            ],
        }
    },
}

@database
@validate(query_param_sc=query_param_schema)
def authorize(event, context, session):
    # event is type dictionary
    client_parameters = event["queryStringParameters"]
    client_id = client_parameters["client_id"]
    response_type = client_parameters["response_type"]
    redirect_uri = client_parameters["redirect_uri"]
    code_challenge_method = client_parameters["code_challenge_method"]
    code_challenge = client_parameters["code_challenge"]
    state = client_parameters["state"]

    if response_type != "code":
        return {
            "statusCode": 400,
            "body": {
                "errors": [
                    {
                        "type": "invalid_response_type",
                        "message": "Only the authorization code grant type is supported"
                    },
                ],
            }
        }

    if code_challenge_method != CODE_CHALLENGE_METHOD:
        return {
            "statusCode": 400,
            "body": {
                "errors": [
                    {
                        "type": "invalid_code_challenge_method",
                        "message": "Only SHA256 is supported for the code challenge method"
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
                        "message": "Client ID was not found"
                    }
                ]
            },
        }

    if client.redirect_uri != redirect_uri:
        return {
            "statusCode": 400,
            "body": {
                "error": [
                    {
                        "type": "invalid_redirect_uri",
                        "message": "The redirect_uri was not found"
                    }
                ]
            }
        }

    # TODO: add an expiry time to the code_challenge tokens
    token_payload = {"code_challenge": code_challenge}
    token = jwt.encode(token_payload, AUTH_PRIVATE_KEY, algorithm="HS256").decode("utf-8")

    return {
        "statusCode": 200,
        "body": {
            "redirect_uri": redirect_uri,
            "response_type": response_type,
            "code_challenge_method": code_challenge_method,
            "code_challenge_token": token,
            "code_challenge": code_challenge,
            "client_id": client_id,
            "state": state
        },
    }
