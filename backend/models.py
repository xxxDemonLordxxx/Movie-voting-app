from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class SuggestedMovie(Base):
    __tablename__ = "suggested_movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())