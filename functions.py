import requests
import json
from sqlalchemy import select
from api_settings import base_url, headers
from mapping import teams_table
from api_settings import base_url, headers

# Save JSON response to a file
def save_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)  # Save with pretty formatting
    print(f"Data saved to {filename}")

# Function to fetch data from a specific endpoint
def fetch_data(endpoint, params=None):
    response = requests.get(base_url + endpoint, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

# Function to retrieve team_id
def get_team_id(session, team_name):
    # Query the teams table for the team_id based on the team_name
    team_query = select(teams_table.c.team_id).where(teams_table.c.team_name == team_name)
    team_id = session.execute(team_query).scalar_one_or_none()

    if team_id is None:
        raise ValueError(f"Team '{team_name}' not found in the teams table.")
    
    return team_id
