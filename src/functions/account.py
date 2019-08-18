import json

from src.models import User
from src.utils.decorators import database, token_required, validate


schema = {
    "type": "object",
    "properties": {
        "queryStringParameters": {
            "type": "object",
            "properties": {"email": {"type": "string"}},
            "required": ["email"],
        }
    },
}


@database
@token_required
@validate(schema)
def exists(event, context, session):
    # Search for a user with a verified email
    email = event["queryStringParameters"]["email"]
    user = session.query(User).filter_by(email=email.lower(), verified=True).first()

    return {
        "statusCode": 200,
        "body": {
            "exists": user != None,
            "first_name": user.first_name if user != None else None,
        },
    }


@database
@token_required
def me(event, context, session):
    user_id = event["user_id"]
    user = session.query(User).filter_by(id=user_id).first()

    return {"statusCode": 200, "body": {"user": user.toJson()}}
