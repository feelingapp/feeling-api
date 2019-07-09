import os
import re
import json
import jsonschema

from dotenv import load_dotenv
from jsonschema import Draft4Validator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib import parse


def database(function):
    """Decorator to help connect to a database"""

    def wrap_function(*args):
        # Set environment variables from .env
        load_dotenv()

        # Connect to database
        database_url = os.getenv("DATABASE_URL")
        engine = create_engine(database_url)

        Session = sessionmaker(bind=engine)

        # create a Session
        session = Session()

        # Call function
        response = function(*args, session)

        # Close database connection
        session.close()
        engine.dispose()

        return response

    return wrap_function


# TODO: validate against DoS attacks by limiting the amount of items in lists and limiting the number of query parameters
def validate(header_sc=None, body_sc=None):
    """Decorator to help validate the body and header of the event"""

    def parse_error_message(message):
        """Removes escaped characters from error message"""

        return re.sub(r"(\\n|\\t|\\')", "", message)

    # TODO: make sure this all works with the other API function calls
    def decorator(function):
        def wrap_function(*args):
            event = args[0]
            #print(json.dumps(event, indent=4))  # this line causes errors elsewhere in the code for some reason

            if header_sc:
                try:
                    jsonschema.validate(event,header_sc)
                except jsonschema.exceptions.ValidationError as e:
                    return {"statusCode": 400, "body": {"error": e.message}}

            if body_sc and event["body"]:

                body = parse_parameters(event["body"])
                # Create JSON schema validator
                # TODO: check specifications on each of the validators and why to use them
                validator = Draft4Validator(body_sc)

                # Generate errors
                errors = [
                    {
                        "type": "validation-error",
                        "message": parse_error_message(error.message),
                    }
                    for error in validator.iter_errors(body)
                ]

                # Return error to client if body is invalid
                if errors:
                    return {"statusCode": 400, "body": {"errors": errors}}

            # Call function
            return function(*args)

        return wrap_function

    return decorator


def token_required(function):
    """Decorator handle access tokens"""

    def wrap_function(*args):
        event = args[0]
        headers = event["headers"]

        authorization = headers.get("Authorization")

        if authorization:
            token = authorization.split("Bearer ")[1]

            # TODO: check if token is expired

            # TODO: parse token
            user_id = None

            # Add user ID to event argument
            new_event = {**event, "user_id": user_id}
            args = (new_event, *args[1:])

            # Call function
            return function(*args)

        return {"statusCode": 401}

    return wrap_function


# TODO: double check why parse_qs makes every item a list
def parse_parameters(body):
    dict = parse.parse_qs(body)
    for item in dict:
        dict[item] = dict[item][0]
    return dict
