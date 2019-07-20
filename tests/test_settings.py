import requests
from dotenv import load_dotenv
from pytest import fixture

from src.models import Settings

from .utils import base_url, session, token


@fixture
def settings(session, user):
    settings = Settings(
        user.id,
        {"daily_reminder": {"enabled": True, "time": {"hour": 20, "minute": 00}}},
    )
    session.add(settings)
    session.commit()

    yield settings

    session.query(Settings).filter(Settings.id == settings.id).delete()
    session.commit()


def test_get_settings(base_url, token, settings):
    """Fetch a user's settings"""

    url = f"{base_url}/settings"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    json = response.json()

    assert response.status_code == 200
    assert json.settings == settings.toJson()


def test_update_settings(base_url, token, settings):
    """Update a user's settings"""

    new_settings = {
        "daily_reminder": {"enabled": False, "time": {"hour": 21, "minute": 30}}
    }

    url = f"{base_url}/settings"
    response = requests.post(
        url, headers={"Authorization": f"Bearer {token}"}, data=new_settings
    )
    json = response.json()

    assert response.status_code == 200
    assert json.settings == new_settings
