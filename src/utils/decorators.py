import os
import re
import json

from dotenv import load_dotenv
from jsonschema import Draft4Validator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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
        engine.dispose()

        return response

    return wrap_function


def validate(schema):
    """Decorator to help validate the body of the event"""

    def parse_error_message(message):
        """Removes escaped characters from error message"""

        return re.sub(r"(\\n|\\t|\\')", "", message)

    def decorator(function):
        def wrap_function(*args):
            event = args[0]
            body = json.loads(event["body"])

            # Create JSON schema validator
            validator = Draft4Validator(schema)

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

        print(event)

        authorization = headers.get("Authorization")

        if authorization:
            token = authorization.split("Bearer ")[0]

            # TODO: parse token
            user_id = None

            # Add user ID to event argument
            args = ({**event, "user_id": user_id}, *event[1:])

        # Call function
        return function(*args)

    return wrap_function
