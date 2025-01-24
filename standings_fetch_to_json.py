import requests
import json
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

# Fetch standings in the English Premier League (league id: 39, season: 2023)
teams_data = fetch_data('standings', params={'league': 39, 'season': 2023})
filename = 'standings2023.json'

save_json_to_file(teams_data, filename)
