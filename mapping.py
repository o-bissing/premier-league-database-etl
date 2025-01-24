from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

# Metadata for table definitions
metadata = MetaData()

# Define the Teams table schema
teams_table = Table(
    "teams", metadata,
    Column("team_id", Integer, primary_key=True, autoincrement=True),
    Column("team_name", String(100)),
    Column("city", String(100)),
    Column("founded_year", Integer),
    Column("stadium", String(100)),
    Column("manager", String(100))
)

# Define the Standings table schema
standings_table = Table(
    "standings", metadata,
    Column("standings_id", Integer, primary_key=True, autoincrement=True),
    Column("team_id", Integer, ForeignKey("teams.team_id")),
    Column("season", String(10)),
    Column("matches_played", Integer),
    Column("wins", Integer),
    Column("draws", Integer),
    Column("losses", Integer),
    Column("goals_for", Integer),
    Column("goals_against", Integer),
    Column("goal_difference", Integer),
    Column("points", Integer),
    Column("table_position", Integer)
)