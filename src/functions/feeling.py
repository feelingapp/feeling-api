from src.consts import Emotion
from src.models import Feeling
from src.utils.decorators import database, token_required, validate

schema = {
    "type": "object",
    "body": {
        "type": "object",
        "properties": {
            "emotion": {"type": "string", "enum": Emotion.list()},
            "description": {"type": "string"},
            "hashtags": {
                "type": "array",
                "items": {"type": "string"},
                "uniqueItems": True,
            },
        },
        "required": ["emotion"],
    },
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
    body = event["body"]

    # Get feeling properties
    emotion = Emotion[body["emotion"]]
    description = body.get("description")
    hashtags = body.get("hashtags")
    user_id = event["user_id"]

    # Create a new feeling in the database
    feeling = Feeling(emotion, description, hashtags, user_id)
    session.add(feeling)
    session.commit()

    return {"statusCode": 200}


@database
@token_required
@validate(schema)
def put(event, context, session):
    body = event["body"]

    feeling_id = event["pathParameters"]["id"]
    user_id = event["user_id"]

    feeling = session.query(Feeling).filter_by(id=feeling_id, user_id=user_id).first()

    if not feeling:
        return {"statusCode": 404}

    feeling.set_emotion(body["emotion"])
    feeling.description = body.get("description")
    feeling.hashtags = body.get("hashtags")
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
