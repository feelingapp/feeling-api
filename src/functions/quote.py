import json

from sqlalchemy.sql.expression import func

from src.consts import Emotion
from src.models import Quote
from src.utils.decorators import database, token_required, validate


@database
@token_required
def get(event, context, session):
    emotion = event["pathParameters"]["emotion"].upper()

    # Get emotion ID from emotion name
    emotion_id = Emotion.getId(emotion)

    # Handle if no emotion ID
    if not emotion_id:
        return {"statusCode": 400}

    # Fetch random quote from the database
    quote = (
        session.query(Quote)
        .filter_by(emotion_id=emotion_id)
        .order_by(func.random())
        .limit(1)
        .first()
    )

    # Handle if no quote exists for the emotion
    if not quote:
        return {"statusCode": 404}

    return {"statusCode": 200, "body": {"quote": quote.quote, "author": quote.author}}
