from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select
from sqlalchemy.orm import sessionmaker
import json
from mapping import standings_table
from api_settings import DATABASE_URL
from functions import get_team_id

# Database connection setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Check if standings exist and insert if not
def upsert_standings(standing, season):
    team_id = get_team_id(session, standing['team']['name'])  # Extract team name from the nested structure
    matches_played = standing['all']['played']
    wins = standing['all']['win']
    draws = standing['all']['draw']
    losses = standing['all']['lose']
    goals_for = standing['all']['goals']['for']
    goals_against = standing['all']['goals']['against']
    goal_difference = standing['goalsDiff']
    points = standing['points']
    table_position = standing['rank']
    
    # Query to check for existing standings
    query = select(standings_table).where(
        standings_table.c.team_id == team_id,
        standings_table.c.season == season
    )
    result = session.execute(query).fetchone()
    
    if result:
        print(f"Standings for team '{standing['team']['name']}' in season '{season}' already exist in the database.")
    else:
        # Insert standings
        insert_query = standings_table.insert().values(
            team_id=team_id,
            season=season,
            matches_played=matches_played,
            wins=wins,
            draws=draws,
            losses=losses,
            goals_for=goals_for,
            goals_against=goals_against,
            goal_difference=goal_difference,
            points=points,
            table_position=table_position
        )
        session.execute(insert_query)
        session.commit()
        print(f"Standings for team '{standing['team']['name']}' in season '{season}' have been added to the database.")

# Load JSON data
with open('json_files/standings2023.json', 'r') as file:
    data = json.load(file)

# Loop through the standings and upsert into the database
season = data['response'][0]['league']['season']  # Extract season from the JSON
standings_list = data['response'][0]['league']['standings'][0]  # Extract the first (and only) standings list

for standing in standings_list:
    upsert_standings(standing, season)

# Close session when done
session.close()
