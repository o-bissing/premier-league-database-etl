## Introduction

Goal of this project is to enchance my Data Engineering and Analytics skills. Data for this project is fetched from a [Sport API](https://dashboard.api-football.com/).

## Background

I love watching English Premier League and at some point I came up with an idea that it would be great to create a dataset using PostgreSQL by fetching data from some API. Football data provides an excellent opportunity for analyse and visualisation.

## Tools I used

To create this project I worked with following tools:

- **ETL**
- **REST**
- **requests library** for fetching the data from the API
- **SQLAlchemy library** for transfering the data from .json file to the table
- **pgAdmin** for managing the database, creating ERD diagram
- **ChatGPT** to help with fixing some errors and creating a complicated SQL-query
- **Power BI** to create a report
- **Bash** for interaction with OS, doing terminal based tasks and working with GitHub
- **Git** for version control

## Creating tables using PostgreSQL

I started with creating schemas for my future tables.

```sql
CREATE TABLE IF NOT EXISTS Teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    founded_year INT,
    stadium VARCHAR(100),
    manager VARCHAR(100)
);
```

ERD diagram of my tables correlation looks as follows (made using pgAdmin):

![ERD diagram](img/ERD.png)

## Filling tables via fetching from an API

To fetch the data from the API python's requests library had been used.

```python
# Function to fetch data from a specific endpoint
def fetch_data(endpoint, params=None):
    response = requests.get(base_url + endpoint, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None
```

Response had been then saved as .json file for further use.

To transfer the data from .json file to the table I used python's SQLAlchemy library.
Firstly a mapping should be done. In this case I have been using imperative table definitions because I was going to use raw SQL queries to train these skills as well. Example of mapping is below:

```python
matches_table = Table(
    "matches", metadata,
    Column("match_id", Integer, primary_key=True, autoincrement=True),
    Column("home_team_id", Integer, ForeignKey("teams.team_id"), nullable=False),
    Column("away_team_id", Integer, ForeignKey("teams.team_id"), nullable=False),
    Column("match_date", Date),
    Column("stadium", String(100)),
    Column("home_score", Integer),
    Column("away_score", Integer),
    Column("result", String(10), CheckConstraint("result IN ('home', 'away', 'draw')"))
)
```

Then all the data has been transfered into the tables.

## SQL queries

To practice SQL-skills I came up with 4 queries: to find top scoring stadiums (where the most goals were scored), home standings table (how standings would have looked like if only home games count), away standings table (how standings would have looked like if only away games count) and longest winning streaks for each team.

Home standings query looks as follows:

```sql
SELECT
    t.team_name AS team,
    COUNT(*) AS home_matches_played,
    SUM(CASE WHEN m.result = 'home' THEN 1 ELSE 0 END) AS home_wins,
    SUM(CASE WHEN m.result = 'draw' THEN 1 ELSE 0 END) AS home_draws,
    SUM(CASE WHEN m.result = 'away' THEN 1 ELSE 0 END) AS home_losses,
    SUM(m.home_score) AS goals_scored_at_home,
    SUM(m.away_score) AS goals_conceded_at_home,
    SUM(
        CASE
            WHEN m.result = 'home' THEN 3
            WHEN m.result = 'draw' THEN 1
            ELSE 0
        END
    ) AS home_points
FROM Matches m
JOIN Teams t ON m.home_team_id = t.team_id
GROUP BY t.team_name
ORDER BY home_points DESC, goals_scored_at_home DESC;
```

With following results (visualized using Power BI):

![Power BI visualisation](img/Power_BI_visualisation.jpg)

!!! To get map visualisations data adjustments in Power BI were neccesary (to get map to see cities: fetched city info was loaded in a inappropriate format and also naming needed to be adjusted since maps do not recognize them if there is additional information, for example "Wolverhampton, West Midlands" needed to be changed to just "Wolverhampton").
