from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Схемы главной

# Схемы фильмов
class MovieBase(BaseModel):
    title: str
    description: str

class MovieResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

# Схемы заявок
class SuggestionBase(BaseModel):
    suggester_name: Optional[str] = None
    is_anonymous: bool = False

class MovieSuggestionCreate(MovieBase, SuggestionBase):
    pass


class SuggestionResponse(BaseModel):
    id: int
    movie_id: int
    suggester_name: Optional[str]
    is_anonymous: bool
    created_at: datetime
    movie: MovieResponse

    class Config:
        from_attributes = True


# Схемы голосований
class PollResponse(BaseModel):
    id: int
    title: str
    state: str
    poll_start: datetime = None
    poll_end: datetime = None
    created_at: datetime

    class Config:
        from_attributes = True

# Схемы результатов голосований


# Схемы ивентов
