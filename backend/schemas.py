from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MovieBase(BaseModel):
    title: str
    description: str

class SuggestionBase(BaseModel):
    suggester_name: Optional[str] = None
    is_anonymous: bool = False

class MovieSuggestionCreate(MovieBase, SuggestionBase):
    pass

class MovieResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

class SuggestionResponse(BaseModel):
    id: int
    movie_id: int
    suggester_name: Optional[str]
    is_anonymous: bool
    created_at: datetime
    movie: MovieResponse

    class Config:
        from_attributes = True