from src.models import Settings, User
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
@validate(schema)
def settings(event, context, session):
    body = event["body"]
    user_id = event["user_id"]

    # Update settings in database
    user_settings = Settings(user_id, body)
    session.add(user_settings)
    session.commit()

    return {"statusCode": 200}
