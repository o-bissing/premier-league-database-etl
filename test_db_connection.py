from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Replace the following with your actual database URL
DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost:5432/premier_league"

# Create an engine to connect to the PostgreSQL database
engine = create_engine(DATABASE_URL)

try:
    # Try to establish a connection to the database
    with engine.connect() as connection:
        print("Connection to the database is successful!")
except OperationalError as e:
    print(f"Error: Unable to connect to the database. {e}")
