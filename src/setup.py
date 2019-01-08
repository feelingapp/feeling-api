from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Set environment variables from .env
load_dotenv()

# Connect to database
database = create_engine("postgres://localhost:5432/postgres")
Session = sessionmaker(bind=database)

session = Session()

# TODO: Build databases

session.close()

database.dispose()
