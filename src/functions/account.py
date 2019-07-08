import json

from src.models import User
from src.utils.decorators import database, token_required, validate


@database
def exists(event, context, session):
    # Make sure email is in the query string parameters
    if not event["queryStringParameters"] or event["queryStringParameters"]["email"]:
        return {"statusCode": 400}

    # Search for a user with a verified email
    email = event["queryStringParameters"]["email"]
    user = session.query(User).filter_by(email=email, verified=True).first()

    return {"statusCode": 200, "body": {"exists": user != None}}

