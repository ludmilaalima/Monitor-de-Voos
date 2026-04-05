from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
connect_args = {}

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# fast api
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# worker
def get_session():
    return SessionLocal()

class Base(DeclarativeBase):
    ...



