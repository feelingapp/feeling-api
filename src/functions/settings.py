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
def put(event, context, session):
    body = event["body"]
    user_id = event["user_id"]

    # Update settings in database
    settings = Settings(user_id, body)
    session.add(settings)
    session.commit()

    return {"statusCode": 200}
