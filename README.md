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
