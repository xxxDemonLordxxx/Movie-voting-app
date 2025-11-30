from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# Схемы главной

# Схемы фильмов
class MovieBase(BaseModel):
    tmdb_id: Optional[int] = None
    title: str
    language: Optional[str] = 'en-US'


class MovieCreate(BaseModel):
    pass


class MovieResponse(BaseModel):
    id: int
    tmdb_id: Optional[int] = None
    title: str
    language: Optional[str] = 'en-US'
    # дописать инфу из tmdb

    class Config:
        from_attributes = True





# Схемы заявок
class SubmissionBase(BaseModel):
    poll_id: int
    author: Optional[str] = None
    comment: str
    image_url: Optional[str] = None


class SubmissionCreate(SubmissionBase):
    movie: MovieBase


class SubmissionResponse(BaseModel):
    id: int
    poll_id: int
    author: Optional[str] = None
    comment: str
    image_url: Optional[str] = None
    current_votes: int = 0
    created_at: datetime
    movie: MovieResponse

    model_config = ConfigDict(from_attributes=True)







# Схемы голосований
class PollBase(BaseModel):
    title: str
    start: datetime
    end: datetime
    state_id: int

class PollCreate(PollBase):
    pass

class PollResponse(BaseModel):
    id: int
    title: str
    start: datetime
    end: datetime
    state_id: int
    created_at: datetime
    state_name: str
    
    model_config = ConfigDict(from_attributes=True)








# Состояния голосований
class PollStateBase(BaseModel):
    name: str

class PollStateCreate(PollStateBase):
    pass

class PollStateResponse(PollStateBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)





# Схемы голосования (от юзера) - ballots
  
class VoteBase(BaseModel):
    poll_id: int
    submission_id: int
    rank: int

class VoteCreate(VoteBase):
    pass

class VoteResponse(BaseModel):
    id: int
    poll_id: int
    submission_id: int
    rank: int
    points: int = 0
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Схемы ивентов
