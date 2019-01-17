from src.models import Feeling
from src.utils.decorators import database, token_required


@database
@token_required
def get(event, context, session):
    feeling_id = event["pathParameters"]["id"]
    user_id = event["user_id"]

    # Fetch feeling by feeling ID and user ID from the database
    # It's important to filter by user_id in the access token so no other user can see another user's feelings
    feeling = session.query(Feeling).filter_by(id=feeling_id, user_id=user_id).first()

    if not feeling:
        return {"statusCode": 404}

    return {"statusCode": 200, "body": feeling.toJson()}


@database
@token_required
def delete(event, context, session):
    feeling_id = event["pathParameters"]["id"]
    user_id = event["user_id"]

    # Delete feeling by ID
    session.query(Feeling).filter_by(id=feeling_id, user_id=user_id).delete()
    session.commit()

    return {"statusCode": 200}
