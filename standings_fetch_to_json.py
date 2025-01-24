from functions import save_json_to_file, fetch_data

# Fetch standings in the English Premier League (league id: 39, season: 2023)
teams_data = fetch_data('standings', params={'league': 39, 'season': 2023})
filename = 'json_files/standings2023.json'

save_json_to_file(teams_data, filename)
