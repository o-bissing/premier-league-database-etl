from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select

# Metadata for table definitions
metadata = MetaData()

# Define the Teams table schema
teams_table = Table(
    "teams", metadata,
    Column("team_id", Integer, primary_key=True),
    Column("team_name", String(100)),
    Column("city", String(100)),
    Column("founded_year", Integer),
    Column("stadium", String(100)),
    Column("manager", String(100))
)