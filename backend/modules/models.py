from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(Integer, ForeignKey("polls.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    author = Column(String, nullable=True)
    comment = Column(Text)
    image_url = Column(String, nullable=True)
    current_votes = Column(Integer, nullable=True, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    movie = relationship("Movie")

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    tmdb_id = Column(Integer, nullable=True, index=True)
    language = Column(String, default='en-US')

class Poll(Base):
    __tablename__ = "polls"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    state_id = Column(Integer, ForeignKey("poll_states.id"))
    start = Column(DateTime(timezone=True))
    end = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    state = relationship("PollState", backref="polls", lazy="joined")
    
    @property
    def state_name(self):
        return self.state.name if self.state else None

class PollState(Base):
    __tablename__ = "poll_states"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    

class Vote(Base):
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(Integer, ForeignKey("polls.id"), index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    rank = Column(Integer)
    points = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    image_id = Column(Integer, nullable=True)
    date = Column(DateTime(timezone=True))
    event_type = Column(Integer, ForeignKey("event_types.id"))
    description = Column(Text)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EventType(Base):
    __tablename__ = "event_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)

