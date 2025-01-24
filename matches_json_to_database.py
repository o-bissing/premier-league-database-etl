from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from api_settings import DATABASE_URL  # Assuming you've set up your DATABASE_URL correctly
from mapping import teams_table, matches_table 

# Database connection setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define the Matches table schema
metadata = MetaData()

# Fetch data from matches2023.json
with open('json_files/matches2023.json', 'r') as file:
    data = json.load(file)

def upsert_match(match_data):
    # Extract data from the match
    fixture = match_data['fixture']
    teams = match_data['teams']
    goals = match_data['goals']
    
    # Extract match details
    match_date = datetime.strptime(fixture['date'], '%Y-%m-%dT%H:%M:%S+00:00').date()
    stadium = fixture['venue']['name']
    home_score = goals['home']
    away_score = goals['away']
    
    # Determine result
    if home_score > away_score:
        result = 'home'
    elif away_score > home_score:
        result = 'away'
    else:
        result = 'draw'
    
    # Get team IDs from the teams table
    home_team_name = teams['home']['name']
    away_team_name = teams['away']['name']
    
    # Query to get team IDs
    home_team = session.execute(select(teams_table).where(teams_table.c.team_name == home_team_name)).fetchone()
    away_team = session.execute(select(teams_table).where(teams_table.c.team_name == away_team_name)).fetchone()

    # Ensure that the result is not None and access the team_id correctly
    if home_team and away_team:
        home_team_id = home_team[0]  # Accessing by index, assuming 'team_id' is the first column
        away_team_id = away_team[0]  # Accessing by index, assuming 'team_id' is the first column
    else:
        print(f"Team(s) not found for match: {home_team_name} vs {away_team_name}")
        return

    # Insert match into the database
    insert_query = matches_table.insert().values(
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        match_date=match_date,
        stadium=stadium,
        home_score=home_score,
        away_score=away_score,
        result=result
    )
    session.execute(insert_query)
    session.commit()

    print(f"Match {home_team_name} vs {away_team_name} has been added to the database.")

# Loop through the matches and upsert into the database
for match_entry in data['response']:
    upsert_match(match_entry)

# Close session when done
session.close()
