# Importing libraries
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from config.db_config import meta

# Initializing
users = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("email", String(255)),
    Column("password", String(255)),
    Column("createdAt", DateTime),
    Column("updatedAt", DateTime),
)
