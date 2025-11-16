from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/moviedb")

# Add connection retry logic
def create_engine_with_retry():
    for i in range(5):
        try:
            engine = create_engine(DATABASE_URL)
            with engine.connect() as conn:
                break
        except Exception as e:
            if i == 4:
                raise e
            time.sleep(2 ** i)
    return engine

engine = create_engine_with_retry()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()