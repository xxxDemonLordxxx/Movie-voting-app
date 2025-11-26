from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import modules.models as models
from modules.database import engine, get_db
from modules.minio_db import minio_client
from modules.schemas import MovieSuggestionCreate, SuggestionResponse, PollResponse
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


# Главная страница (лента новостей)

@app.get(path="/posters",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Get all event posters",
    responses={},
    tags=["Main Page"]
)
def get_posters(db: Session = Depends(get_db)):
    try:
        events = db.query(models.Event).all()
        return ""
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# Голосования

@app.get(
    path="/polls",
    response_model=PollResponse,
    status_code=status.HTTP_200_OK,
    summary="See all polls",
    responses={},
    tags=["Polls"]
)
def get_polls(db: Session = Depends(get_db)):
    try:
        polls = db.query(models.Poll).all()
        return [PollResponse.from_orm(poll) for poll in polls]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    path="/polls/new",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Create new poll",
    responses={},
    tags=["Polls"]
)
def create_new_poll(poll_name: str, db: Session = Depends(get_db)):
    try:
        polls = db.query(models.Poll).all()
        return ""
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch(
    path="/polls/start/{poll_id}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Start voting",
    responses={},
    tags=["Polls"]
)
def start_poll(poll_name: str, db: Session = Depends(get_db)):
    try:
        polls = db.query(models.Poll).all()
        return ""
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch(
    path="/polls/stop/{poll_id}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Stop voting",
    responses={},
    tags=["Polls"]
)
def stop_poll(poll_name: str, db: Session = Depends(get_db)):
    try:
        polls = db.query(models.Poll).all()
        return ""
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






# Результаты голосований

@app.get(
    path="/polls/results/{poll_id}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="See poll results",
    responses={},
    tags=["Poll results"]
)
def get_poll_results(db: Session = Depends(get_db)):
    try:
        polls = db.query(models.Poll).all()
        return ""
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    path="/polls/confirm/{poll_id}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Confirm poll results and add movie to calendar",
    responses={},
    tags=["Poll results"]
)
def confirm_poll_results(db: Session = Depends(get_db)):
    try:
        polls = db.query(models.Poll).all()
        return ""
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Заявки

@app.get(
    path="/submissions/{poll_id}",
    response_model=list,
    status_code=status.HTTP_200_OK,
    summary="See all submissions for a poll",
    responses={},
    tags=["Submissions"]
)
def get_submissions(poll_id: int, db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.Submission).all()
        return submissions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    path="/submissions/{submission_id}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="See submission data",
    responses={},
    tags=["Submissions"]
)
def get_submission(submission_id: int, db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.Submission).all()
        return "data"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    path="/submissions/new",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Create a new submission",
    responses={},
    tags=["Submissions"]
)
def create_new_submission(db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.Submission).all()
        return "sss"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# Фильмы + TMDB API 

@app.get(
    path="/films/{film_id}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="See movie data by id",
    responses={},
    tags=["Films"]
)
def get_film_by_id(film_id: int, db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.Submission).all()
        return "data"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(
    path="/films/search/{film_name_query}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Find movie by word query",
    responses={},
    tags=["Films"]
)
def find_film_via_query(film_name_query: int, db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.Submission).all()
        return "data"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





# Календарь


@app.get(
    path="/events",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Get all events list",
    responses={},
    tags=["Events"]
)
def get_all_events(db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.Submission).all()
        return "data"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get(
    path="/events/current",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Get current events list (today and future)",
    responses={},
    tags=["Events"]
)
def get_current_events(db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.Submission).all()
        return "data"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get(
    path="/events/{event_id}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Get event data",
    responses={},
    tags=["Events"]
)
def get_event_data(db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.Submission).all()
        return "data"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post(
    path="/events/new",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Create a new event",
    responses={},
    tags=["Events"]
)
def create_event(db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.Submission).all()
        return "data"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete(
    path="/events/delete/{event_id}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Delete the event",
    responses={},
    tags=["Events"]
)
def delete_event(db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.Submission).all()
        return "data"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch(
    path="/events/edit/{event_id}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Edit the event",
    responses={},
    tags=["Events"]
)
def edit_event(db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.Submission).all()
        return "data"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Получение прав админа

@app.post(
    path="/admin/{password}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get admin rights",
    responses={},
    tags=["Admin Rights"]
)
def get_admin_rights(password, db: Session = Depends(get_db)):
    try:
        if password.lower() == "meow":
            return {'message':"Yup here are your rights", 'isadmin':True}
        else:
            return "Nope try again or ask your club head"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   




























""" 

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
        db_suggestion = models.Suggestion(
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
        suggestions = db.query(models.Suggestion).join(models.Movie).all()
        return [SuggestionResponse.from_orm(suggestion) for suggestion in suggestions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/suggestions/{suggestion_id}")
def get_suggestion_detail(suggestion_id: int, db: Session = Depends(get_db)):
    try:
        suggestion = db.query(models.Suggestion)\
            .join(models.Movie)\
            .filter(models.Suggestion.id == suggestion_id)\
            .first()
        if not suggestion:
            raise HTTPException(status_code=404, detail="Suggestion not found")
        return SuggestionResponse.from_orm(suggestion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) """








@app.get("/health")
def health_check():
    return {"status": "healthy"}