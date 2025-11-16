from pydantic import BaseModel

class MovieSuggestion(BaseModel):
    title: str

class MovieResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True 