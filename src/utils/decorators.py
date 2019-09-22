import os
import re
import json
import jsonschema

from dotenv import load_dotenv
from jsonschema import Draft4Validator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib import parse

from src.models import AccessToken


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


def validate(schema):
    """Decorator to help validate the body and header of the event"""

    def parse_error_message(message):
        """Removes escaped characters from error message"""

        return re.sub(r"(\\n|\\t|\\')", "", message)

    def decorator(function):
        def wrap_function(*args):
            event = args[0]

            # Convert body from string to JSON
            if isinstance(event["body"], str):
                try:
                    event["body"] = json.loads(event["body"])
                except:
                    return {
                        "statusCode": 400,
                        "body": {
                            "errors": {
                                "type": "invalid-body",
                                "message": "The request body is not valid JSON",
                            }
                        },
                    }

            # Create JSON schema validator
            validator = Draft4Validator(schema)

            # Generate errors
            errors = [
                {
                    "type": "validation_error",
                    "message": parse_error_message(error.message),
                }
                for error in validator.iter_errors(event)
            ]

            # Return error to client if event is invalid
            if errors:
                return {"statusCode": 400, "body": {"errors": errors}}

            # Call function
            return function(*args)

        return wrap_function

    return decorator


def token_required(function):
    """Decorator to handle access tokens"""

    def wrap_function(*args):
        event = args[0]

        # Headers should be case-insensitive so make them lower case
        headers = dict(
            (header.lower(), value) for header, value in event["headers"].items()
        )

        authorization = headers.get("authorization")

        if authorization:
            token = authorization.split("Bearer ")[1]
            access_token = AccessToken(token)

            if access_token.has_expired():
                return {
                    "statusCode": 401,
                    "body": {
                        "errors": [
                            {
                                "type": "access_token_expired",
                                "message": "The access token has expired",
                            }
                        ]
                    },
                }

            # Add user ID to event argument
            user_id = access_token.payload["sub"]
            event["user_id"] = user_id

            # Call function
            args = (event, *args[1:])
            return function(*args)

        return {"statusCode": 401}

    return wrap_function
