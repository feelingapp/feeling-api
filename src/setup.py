import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

# Set environment variables from .env
load_dotenv()

# Connect to database
database_url = os.getenv("DATABASE_URL")
database = create_engine(database_url)

# Create tables if they do not exist
Base.metadata.create_all(database)

# Close connection
database.dispose()
