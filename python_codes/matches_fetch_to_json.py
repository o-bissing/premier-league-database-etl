from functions import save_json_to_file, fetch_data

# Fetch matches in the English Premier League (league id: 39, season: 2023)
matches_data = fetch_data('fixtures', params={'league': 39, 'season': 2023})
filename = 'json_files/matches2023.json'

save_json_to_file(matches_data, filename)
