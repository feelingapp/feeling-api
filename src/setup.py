import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.User import User
from models import Base

# Set environment variables from .env
load_dotenv()

# Connect to database
database_url = os.getenv("DATABASE_URL")
database = create_engine(database_url)

Base.metadata.create_all(database)

database.dispose()
