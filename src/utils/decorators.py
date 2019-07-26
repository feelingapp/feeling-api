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


def validate(schema):
    """Decorator to help validate the body and header of the event"""

    def parse_error_message(message):
        """Removes escaped characters from error message"""

        return re.sub(r"(\\n|\\t|\\')", "", message)

    def decorator(function):
        def wrap_function(*args):
            event = args[0]

            # Convert body from string to JSON
            if (
                type(event["body"]) == str
                and event["headers"].get("Content-Type") == "application/json"
            ):
                event["body"] = json.loads(event["body"])

            # Create JSON schema validator
            validator = Draft4Validator(schema)

            # Generate errors
            errors = [
                {
                    "type": "validation-error",
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
