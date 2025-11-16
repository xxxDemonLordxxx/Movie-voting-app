from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from schemas import MovieSuggestionCreate, SuggestionResponse
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

@app.post("/suggestions")
def add_suggestion(suggestion: MovieSuggestionCreate, db: Session = Depends(get_db)):
    try:
        # Создаем фильм
        db_movie = models.Movie(
            title=suggestion.title,
            description=suggestion.description
        )
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        
        # Создаем предложение
        db_suggestion = models.MovieSuggestion(
            movie_id=db_movie.id,
            suggester_name=None if suggestion.is_anonymous else suggestion.suggester_name,
            is_anonymous=suggestion.is_anonymous
        )
        db.add(db_suggestion)
        db.commit()
        db.refresh(db_suggestion)
        
        return {"message": "Movie suggestion added", "id": db_suggestion.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/suggestions")
def get_suggestions(db: Session = Depends(get_db)):
    try:
        suggestions = db.query(models.MovieSuggestion).join(models.Movie).all()
        return [SuggestionResponse.from_orm(suggestion) for suggestion in suggestions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/suggestions/{suggestion_id}")
def get_suggestion_detail(suggestion_id: int, db: Session = Depends(get_db)):
    try:
        suggestion = db.query(models.MovieSuggestion)\
            .join(models.Movie)\
            .filter(models.MovieSuggestion.id == suggestion_id)\
            .first()
        if not suggestion:
            raise HTTPException(status_code=404, detail="Suggestion not found")
        return SuggestionResponse.from_orm(suggestion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}