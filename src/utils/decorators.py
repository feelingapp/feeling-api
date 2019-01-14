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
            body = json.loads(args[0]["body"])

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
            return function(*args, errors)

        return wrap_function

    return decorator
