import json

from src.models import Settings
from utils.decorators import database, token_required, validate

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

    return {
        "statusCode": 200,
        "body": {"settings": json.loads(settings.settings) if settings else None},
    }


@database
@token_required
@validate(schema)
def put(event, context, session):
    body = event["body"]
    user_id = event["user_id"]

    # Update settings in database
    settings = Settings(user_id, body)
    session.add(settings)
    session.commit()

    return {"statusCode": 200}
