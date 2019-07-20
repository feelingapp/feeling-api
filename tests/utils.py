import os

from pytest import fixture
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import User


@fixture()
def base_url():
    load_dotenv()
    return os.getenv("API_URL")


@fixture()
def session():
    """Create a SQLAlchemy database session"""

    # Set environment variables from .env
    load_dotenv()

    # Connect to database
    database_url = os.getenv("DATABASE_URL")
    database = create_engine(database_url)

    # Create a session
    SessionMaker = sessionmaker(bind=database)
    created_session = SessionMaker()

    yield created_session

    created_session.close()


@fixture
def user(session):
    user = User("Michael", "Lee", "michael_lee@gmail.com", "password")
    session.add(user)
    session.commit()

    yield user

    session.query(User).filter(User.id == user.id).delete()
    session.commit()


@fixture
def token(session):
    return None
