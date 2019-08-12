import json
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.consts import Emotion
from src.models import Base, User, Emotion as EmotionTable

# Set environment variables from .env
load_dotenv()

# Connect to database
database_url = os.getenv("DATABASE_URL")
database = create_engine(database_url)

# Create tables if they do not exist
Base.metadata.create_all(database)

# Create a Session
Session = sessionmaker(bind=database)
session = Session()

# Add emotions to Emotion table
for emotion in Emotion:
    session.add(EmotionTable(emotion.name))

# Check if the --generate-data flag is provided
if len(sys.argv) > 1 and sys.argv[1] == "--generate-data":
    # Read the mock users file and add the users to the database
    with open("src/data/users.json", "r") as file:
        mock_users = json.load(file)

        for mock_user in mock_users:
            user = User(
                mock_user["first_name"],
                mock_user["last_name"],
                mock_user["email"],
                mock_user["password"],
            )
            user.verified = mock_user["verified"]
            session.add(user)

# Finish and close session
session.commit()
session.close()

# End database connection
database.dispose()
