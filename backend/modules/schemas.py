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
    created_at: datetime
    movie: MovieResponse

    model_config = ConfigDict(from_attributes=True)







# Схемы голосований
class PollBase(BaseModel):
    title: str
    description: Optional[str]
    start: datetime
    end: datetime
    winners: int

class PollCreate(PollBase):
    pass

class PollResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start: datetime
    end: datetime
    state_id: int
    winners: int
    created_at: datetime
    state_name: str
    
    model_config = ConfigDict(from_attributes=True)


class PollInfoResponse(BaseModel):
    poll_info: PollResponse
    submissions: List[SubmissionResponse]
    
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
  
class BallotBase(BaseModel):
    poll_id: int
    rankings: list[int]

class BallotCreate(BallotBase):
    pass

class BallotResponse(BaseModel):
    id: int
    poll_id: int
    rankings: list
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Схемы проведенного голосования

class VotingStats(BaseModel):
    rank: int
    submission: SubmissionResponse
    number_of_votes: float
    status: str

    model_config = ConfigDict(from_attributes=True)


# Схемы видов ивентов

class EventTypeBase(BaseModel):
    name: str
    description: str

class EventTypeCreate(EventTypeBase):
    pass

class EventTypeResponse(BaseModel):
    id: int
    name: str
    description: str
    
    model_config = ConfigDict(from_attributes=True)

# Схемы ивентов

class EventBase(BaseModel):
    title: str
    image_id: Optional[str]
    date: datetime
    event_type_id: int
    description: Optional[str]
    submission_id: Optional[int]

class EventCreate(EventBase):
    pass

class EventResponse(BaseModel):
    id: int
    title: str
    image_id: Optional[str]
    date: datetime
    event_type_id: int
    description: Optional[str]
    submission_id: Optional[int]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

