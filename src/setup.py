import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.User import User

# Set environment variables from .env
load_dotenv()

# Connect to database
database_url = os.getenv("DATABASE_URL")
database = create_engine(database_url)

Session = sessionmaker(bind=database)

session = Session()

# TODO: Build databases

session.close()

database.dispose()
