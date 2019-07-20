import requests
from dotenv import load_dotenv
from pytest import fixture

from src.consts import Emotion
from src.models import Quote

from .utils import base_url, session, token


@fixture
def quote(session):
    """Adds a temporary quote to the database"""

    quote = Quote(
        "To escape criticism: do nothing, say nothing, be nothing.",
        "Elbert Hubbard",
        Emotion.UPSET,
    )
    session.add(quote)
    session.commit()

    yield quote

    session.query(Quote).filter(Quote.id == quote.id).delete()
    session.commit()


def test_get_a_quote(base_url, token, quote):
    """Fetch a random quote"""

    emotion = quote.emotion.name.lower()

    url = f"{base_url}/quote/{emotion}"
    response = requests.get(url)
    json = response.json()

    assert response.status_code == 200
    assert json["emotion"].lower() == emotion


def test_get_a_quote_with_unknown_emotion(base_url, token, quote):
    """Attempt to fetch a quote but emotion is not valid"""

    emotion = "meh"

    url = f"{base_url}/quote/{emotion}"
    response = requests.get(url)

    assert response.status_code == 400
