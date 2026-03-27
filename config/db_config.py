from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from fastapi import Depends
from typing_extensions import Annotated
from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()

# ✅ Get DATABASE_URL from Render environment
DATABASE_URL = os.getenv("DATABASE_URL")

# 🔥 Safety check (very important)
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables")

# ✅ Create engine (PostgreSQL)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # prevents connection issues
)

# ✅ Session
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# ✅ Base class
Base = declarative_base()


# ✅ Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Type-safe dependency (optional but good)
dp_dependency = Annotated[Session, Depends(get_db)]