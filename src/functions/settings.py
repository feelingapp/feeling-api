import json

from src.models import Settings
from src.utils.decorators import database, token_required, validate

schema = {
    "type": "object",
    "body": {
        "type": "object",
        "properties": {
            "daily_reminder": {
                "enabled": {"type": "boolean"},
                "time": {"hour": {"type": "number"}, "minute": {"type": "number"}},
            }
        },
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

    settingsJson = json.loads(settings.settings)
    settingsJson["id"] = settings.id

    return {"statusCode": 200, "body": settingsJson}


@database
@token_required
@validate(schema)
def put(event, context, session):
    body = event["body"]
    user_id = event["user_id"]

    # Fetch settings by user ID from the database
    settings = session.query(Settings).filter_by(user_id=user_id).first()

    # Update settings if found in the database
    if settings:
        settings.body = body
    else:
        # Create new settings if none exist
        new_settings = Settings(user_id, body)
        session.add(new_settings)

    session.commit()

    return {"statusCode": 200}
