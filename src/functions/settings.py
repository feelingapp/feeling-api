import json

from src.models import Settings
from src.utils.decorators import database, token_required, validate

schema = {
    "type": "object",
    "properties": {
        "daily_reminder": {
            "enabled": {"type": "boolean"},
            "time": {"hour": {"type": "number"}, "minute": {"type": "number"}},
        }
    },
}


@database
@token_required
def get(event, context, session):
    user_id = event["user_id"]

    # Fetch settings by user ID from the database
    settings = session.query(Settings).filter_by(user_id=user_id).first()

    if not settings:
        return {"statusCode": 404}

    return {"statusCode": 200, "body": json.loads(settings.settings)}


@database
@token_required
@validate(schema)
def post(event, context, session):
    body = event["body"]
    user_id = event["user_id"]

    # Update settings in database
    settings = Settings(user_id, body)
    session.merge(settings)
    session.commit()

    return {"statusCode": 200}
