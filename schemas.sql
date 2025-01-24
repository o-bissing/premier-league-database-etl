-- Create Teams table
CREATE TABLE IF NOT EXISTS Teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    founded_year INT,
    stadium VARCHAR(100),
    manager VARCHAR(100)
);

-- Create Players table
CREATE TABLE IF NOT EXISTS Players (
    player_id SERIAL PRIMARY KEY,
    team_id INT REFERENCES Teams(team_id),
    player_name VARCHAR(100) NOT NULL,
    position VARCHAR(50),
    nationality VARCHAR(50),
    birth_date DATE,
    jersey_number INT
);

-- Create Matches table
CREATE TABLE IF NOT EXISTS Matches (
    match_id SERIAL PRIMARY KEY,
    home_team_id INT REFERENCES Teams(team_id),
    away_team_id INT REFERENCES Teams(team_id),
    match_date DATE,
    stadium VARCHAR(100),
    home_score INT,
    away_score INT,
    result VARCHAR(10) CHECK(result IN ('home', 'away', 'draw'))
);

-- Create Goals table
CREATE TABLE IF NOT EXISTS Goals (
    goal_id SERIAL PRIMARY KEY,
    match_id INT REFERENCES Matches(match_id),
    player_scored_id INT REFERENCES Players(player_id),
    player_assisted_id INT REFERENCES Players(player_id) NULL,
    team_id INT REFERENCES Teams(team_id),
    goal_time INT
);

-- Create Standings table
CREATE TABLE IF NOT EXISTS Standings (
    standings_id SERIAL PRIMARY KEY,
    team_id INT REFERENCES Teams(team_id),
    season INT,
    matches_played INT,
    wins INT,
    draws INT,
    losses INT,
    goals_for INT,
    goals_against INT,
    goal_difference INT,
    points INT,
    table_position INT
);