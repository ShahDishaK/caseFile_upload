# Importing libraries
from sqlalchemy import MetaData
from sqlalchemy.engine import create_engine
import os

# Initialization
meta = MetaData()


# Creating engine
auth = f"{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
engine = create_engine(
    f"mysql+pymysql://{auth}@{os.getenv('DATABASE_URL')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}",
    pool_recycle=3600,
)

# Connecting db
with engine.connect() as db:
    meta.reflect(db)