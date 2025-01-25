from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.orm import sessionmaker
import json
from api_settings import DATABASE_URL
from mapping import teams_table

# Database connection setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Metadata for table definitions
metadata = MetaData()

# Check if a team exists and insert if not
def upsert_team(team_data):
    team_name = team_data['team']['name']
    city = team_data['venue']['city']
    founded_year = team_data['team']['founded']
    stadium = team_data['venue']['name']
    manager = None  # no manager info in this response
    
    # Query to check for existing team
    query = select(teams_table).where(teams_table.c.team_name == team_name)
    result = session.execute(query).fetchone()
    
    if result:
        print(f"Team '{team_name}' already exists in the database.")
    else:
        # Insert the new team
        insert_query = teams_table.insert().values(
            team_name=team_name,
            city=city,
            founded_year=founded_year,
            stadium=stadium,
            manager=manager
        )
        session.execute(insert_query)
        session.commit()
        print(f"Team '{team_name}' has been added to the database.")

# Load JSON data
with open('json_files/teams2023.json', 'r') as file:
    data = json.load(file)

# Loop through the teams and upsert into the database
for team_entry in data['response']:
    upsert_team(team_entry)

# Close session when done
session.close()