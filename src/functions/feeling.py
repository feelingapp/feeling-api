import json

from src.consts import Emotion
from src.models import Feeling, Hashtag
from src.utils.decorators import database, token_required, validate

schema = {
    "type": "object",
    "properties": {
        "emotion": {"type": "string", "enum": Emotion.list()},
        "description": {"type": "string"},
        "hashtags": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
    },
    "required": ["emotion"],
}


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
@validate(schema)
def post(event, context, session):
    body = json.loads(event["body"])
    user_id = event["user_id"]

    # Create a new feeling in the database
    emotion = Emotion[body["emotion"]]
    description = body["description"]
    feeling = Feeling(emotion, description, user_id)

    # If hashtags, add them to the database
    if body.get("hashtags"):
        for name in body["hashtags"]:
            hashtag = Hashtag(name)
            feeling.hashtags.append(hashtag)

    session.add(feeling)
    session.commit()

    return {"statusCode": 200}


@database
@token_required
def delete(event, context, session):
    feeling_id = event["pathParameters"]["id"]
    user_id = event["user_id"]

    # Delete feeling by ID
    session.query(Feeling).filter_by(id=feeling_id, user_id=user_id).delete()
    session.commit()

    return {"statusCode": 200}
