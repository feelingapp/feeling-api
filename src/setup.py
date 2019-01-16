import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base, Emotion as EmotionTable
from src.consts import Emotion

# Set environment variables from .env
load_dotenv()

# Connect to database
database_url = os.getenv("DATABASE_URL")
database = create_engine(database_url)

# Create tables if they do not exist
Base.metadata.create_all(database)

# create a Session
Session = sessionmaker(bind=database)
session = Session()


# Add emotions to Emotion table
for emotion in Emotion:
    session.add(EmotionTable(emotion.name))

# Finish and close session
session.commit()
session.close()

# End database connection
database.dispose()

