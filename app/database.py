from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_host = "localhost"
db_port = "5432"
db_user = "postgres"
db_password = "123"
db_name = "postgres"

db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url)
# Create a session for communication with database.
session = sessionmaker(bind=engine)
# Basic model for table
Base = declarative_base()

def get_database():
    db = session()
    try:
        yield db
    finally:
        db.close()