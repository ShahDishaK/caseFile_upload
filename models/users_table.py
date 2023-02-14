# Importing libraries
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, Text, Boolean
from config.db_config import meta

# Initializing
users_table = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True),
    Column("email", Text),
    Column("password", Text),
    Column("is_admin", Boolean),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    extend_existing=True
)
