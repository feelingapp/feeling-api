from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database = create_engine("postgres://localhost:5432/postgres")
Session = sessionmaker(bind=database)

session = Session()

# TODO: Build databases

session.close()

database.dispose()
