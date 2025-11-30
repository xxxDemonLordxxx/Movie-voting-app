from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
import modules.models as models
from modules.database import engine, get_db, SessionLocal
from modules.minio_db import minio_client
import modules.schemas as schemas
import modules.crud as crud
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


@app.on_event("startup")
def startup_event():
    """
    Initialize database with default data on application startup
    """
    db = SessionLocal()
    try:
        crud.init_poll_states(db)
    finally:
        db.close()


# ---------------------------------------------------- Endpoints ------------------------------------------------------------- #
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
    response_model=List[schemas.PollResponse],
    status_code=status.HTTP_200_OK,
    summary="See all polls",
    responses={},
    tags=["Polls"]
)
def get_polls(db: Session = Depends(get_db)):
    try:
        polls = crud.get_all_polls(db=db)
        if not polls:
            raise HTTPException(status_code=404, detail="polls not found")
        return polls
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(
    path="/polls/{poll_id}",
    response_model=list[schemas.SubmissionResponse],
    status_code=status.HTTP_200_OK,
    summary="See all submissions for a poll",
    responses={},
    tags=["Polls"]
)
def get_submissions_by_poll(poll_id: int, db: Session = Depends(get_db)):
    try:
        submissions = crud.get_all_submissions_by_poll(db=db, poll_id=poll_id)
        return submissions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    path="/polls/new",
    response_model=schemas.PollResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new poll",
    responses={},
    tags=["Polls"]
)
def create_new_poll(poll: schemas.PollCreate, db: Session = Depends(get_db)):
    try:
        new_poll = crud.add_new_poll(db=db, poll=poll)

        db.refresh(new_poll, ['state'])      

        return new_poll
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch( # !!!!!!!!!!!!!!!!!!!!!!
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


@app.patch( # !!!!!!!!!!!!!!!!!!!!!!
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



 # Голосование


@app.post(
    path="/polls/vote",
    response_model=List[schemas.SubmissionResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Cast votes",
    responses={},
    tags=["Polls"]
)
def add_votes(ballot: list[schemas.VoteCreate], db: Session = Depends(get_db)):
    try:
        poll_id = ballot[0].poll_id if ballot else None

        if not ballot:
            raise HTTPException(status_code=400, detail="No votes provided")
        submissions_count = len(ballot)
        points = {rank: submissions_count - rank + 1 for rank in range(1, submissions_count + 1)}

        vote_responses = []
        for vote in ballot:
            point = points[vote.rank]
            vote_response = crud.add_new_vote(db=db, vote=vote, points = point)
            vote_responses.append(vote_response)
            crud.update_vote(db=db, submission_id=vote.submission_id, points = point) 
 
        return crud.get_all_submissions_by_poll(db=db, poll_id=poll_id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







# Результаты голосований

@app.get( # !!!!!!!!!!!!!!!!!!!!!!
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

@app.post( # !!!!!!!!!!!!!!!!!!!!!!
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















# Предложения


@app.get( 
    path="/submissions/{submission_id}",
    response_model=schemas.SubmissionResponse,
    status_code=status.HTTP_200_OK,
    summary="See submission data",
    responses={},
    tags=["Submissions"]
)
def get_submission(submission_id: int, db: Session = Depends(get_db)):
    try:
        submission = crud.get_submission_data_by_id(db=db, submission_id=submission_id)
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")
        return submission
       
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    path="/submissions/new",
    response_model=schemas.SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new submission",
    responses={},
    tags=["Submissions"]
)
def create_new_submission(submission: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    try:
        new_submission = crud.add_new_submission(db=db, submission=submission)   
        return new_submission
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    








# Фильмы + TMDB API 

@app.get( # !!!!!!!!!!!!!!!!!!!!!! - for TMDB integration
    path="/films/{movie_id}",
    response_model=schemas.MovieResponse,
    status_code=status.HTTP_200_OK,
    summary="See movie data by id",
    responses={},
    tags=["Movies"]
)
def get_film_data(movie_id: int, db: Session = Depends(get_db)):
    try:
        movie = crud.get_movie_data_by_id(db=db, movie_id=movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie
    except HTTPException:
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get( # !!!!!!!!!!!!!!!!!!!!!! - for TMDB integration
    path="/films/search/{movie_name_query}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Find movie by word query",
    responses={},
    tags=["Movies"]
)
def find_film_via_query(film_name_query: int, db: Session = Depends(get_db)):
    try:
        submissions = db.query(models.Submission).all()
        return "data"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





# Календарь


@app.get( # !!!!!!!!!!!!!!!!!!!!!!
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
    

@app.get( # !!!!!!!!!!!!!!!!!!!!!!
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
    

@app.get( # !!!!!!!!!!!!!!!!!!!!!!
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
    

@app.post( # !!!!!!!!!!!!!!!!!!!!!!
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


@app.delete( # !!!!!!!!!!!!!!!!!!!!!!
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

@app.patch( # !!!!!!!!!!!!!!!!!!!!!!
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





@app.get("/health")
def health_check():
    return {"status": "healthy"}