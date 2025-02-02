from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from api_settings import DATABASE_URL

# Create an engine to connect to the PostgreSQL database
engine = create_engine(DATABASE_URL)

try:
    # Try to establish a connection to the database
    with engine.connect() as connection:
        print("Connection to the database is successful!")
except OperationalError as e:
    print(f"Error: Unable to connect to the database. {e}")
