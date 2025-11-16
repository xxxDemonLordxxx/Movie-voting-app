from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from schemas import MovieSuggestion, MovieResponse
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Movie Suggestion API"}

@app.post("/input")
def add_suggestion(movie: MovieSuggestion, db: Session = Depends(get_db)):
    try:
        db_movie = models.SuggestedMovie(title=movie.title)
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return {"message": "Movie suggestion added", "movie": movie.title}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/suggestions")
def get_suggestions(db: Session = Depends(get_db)):
    try:
        movies = db.query(models.SuggestedMovie).all()
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}