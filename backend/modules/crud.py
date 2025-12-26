from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import selectinload

from . import models, schemas, utils







# Главная


# Голосования

def init_poll_states(db: Session):
    existing_states = db.query(models.PollState).count()
    
    if existing_states > 0:
        print("Poll states already initialized")
        return
    
    # Define default states
    default_states = [
        {"name": "offer"},
        {"name": "vote"},
        {"name": "previous"}
    ]
    
    # Create states
    for state_data in default_states:
        db_state = models.PollState(**state_data)
        db.add(db_state)
    
    db.commit()
    print("Poll states initialized successfully")

def init_event_types(db: Session):
    existing_event_types = db.query(models.EventType).count()
    
    if existing_event_types > 0:
        print("Event types already initialized")
        return
    
    # Define default states
    default_event_types = [
        {"name": "Watch party", "description": "Watching movies together !"},
        {"name": "Discussion club", "description": "Discussing things"},
        {"name": "Filming sessions", "description": "Lets film something together"}
    ]
    
    # Create states
    for event_type_data in default_event_types:
        db_event_type = models.EventType(**event_type_data)
        db.add(db_event_type)
    
    db.commit()
    print("Event types initialized successfully")

def add_new_poll(db: Session, poll: schemas.PollCreate) -> models.Poll:
    db_poll = models.Poll(
        title = poll.title,
        description = poll.description,
        state_id = 1,
        start = poll.start,
        end = poll.end,
        winners = poll.winners,
        created_at = datetime.now()
    )
    db.add(db_poll)
    db.commit()
    db.refresh(db_poll)
    return db_poll


def get_all_polls(db: Session) -> List[models.Poll]:
    return db.query(models.Poll).options(selectinload(models.Poll.state)).all()

def get_poll_data(db: Session, poll_id: int) -> models.Poll:
    return db.query(models.Poll).filter(models.Poll.id == poll_id).first()



def add_new_vote(db: Session, vote: schemas.VoteCreate, points: int) -> models.Vote:
    db_vote = models.Vote(
        poll_id = vote.poll_id,
        points = points,
        submission_id = vote.submission_id,
        rank = vote.rank,
        created_at = datetime.now()
    )
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote

def update_vote(db: Session, submission_id: int, points: int):
    submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not submission:
        return None

    submission.current_votes = submission.current_votes + points

    db.commit()
    db.refresh(submission)
    return submission


def start_poll(db: Session, poll_id: int) -> models.Poll:
    poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    if not poll:
        return None

    if poll.state_id == 1:
        poll.state_id = 2
        db.commit()
        db.refresh(poll)
    return db.query(models.Poll).filter(models.Poll.id == poll_id).options(selectinload(models.Poll.state)).first()

def stop_poll(db: Session, poll_id: int) -> models.Poll: 
    poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    if not poll:
        return None

    if poll.state_id == 2:
        poll.state_id = 3
        db.commit()
        db.refresh(poll)

    return db.query(models.Poll).filter(models.Poll.id == poll_id).options(selectinload(models.Poll.state)).first()


# Submissions

def add_new_submission(db: Session, submission: schemas.SubmissionCreate) -> models.Submission:
    movie = db.query(models.Movie).filter(models.Movie.title == submission.movie.title).first()

    if not movie:
        movie = models.Movie(
            title= submission.movie.title,
            tmdb_id = 0,
            language = submission.movie.language
        )
        db.add(movie)
        db.flush()  # добавить поиск в базе imdb

    db_submission = models.Submission(
        poll_id = submission.poll_id,
        movie_id = movie.id,
        author = submission.author,
        comment = submission.comment,
        image_url = "", # доделать сохранение изображений
        current_votes = 0,
        created_at = datetime.now()
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)

    db_submission.movie = movie
    
    return db_submission


def get_all_submissions_by_poll(db: Session, poll_id: int) -> List[models.Submission]:
    return db.query(models.Submission).filter(models.Submission.poll_id == poll_id).all()


def get_submission_data_by_id(db: Session, submission_id: int) -> models.Submission:
    return db.query(models.Submission).filter(models.Submission.id == submission_id).first()






# Фильмы
def get_movie_data_by_id(db: Session, movie_id: int) -> models.Movie:
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()



# Календарь


def add_new_event(db: Session, event: schemas.EventCreate) -> models.Event:
    db_event = models.Event(
        title = event.title,
        image_url = event.image_url, # доделать работу с изображениями
        date = event.date,
        event_type_id = event.event_type_id,
        description = event.description,
        submission_id = event.submission_id,
        created_at = datetime.now()
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_all_events(db: Session) -> List[models.Event]:
    return db.query(models.Event).all()

def get_current_events(db: Session) -> List[models.Event]:
    now = datetime.now()
    return db.query(models.Event).filter(models.Event.date >= now).all()

def get_event_data(db: Session, event_id: int) -> models.Event:
    return db.query(models.Event).filter(models.Event.id == event_id).first()


# типы ивентов
def add_new_event_type(db: Session, event_type: schemas.EventTypeCreate) -> models.EventType:
    db_event_type = models.EventType(
        name =  event_type.name,
        description = event_type.description
    )
    db.add(db_event_type)
    db.commit()
    db.refresh(db_event_type)
    return db_event_type


def get_all_event_types(db: Session) -> List[models.EventType]:
    return db.query(models.EventType).all()

def get_event_type_data(db: Session, event_type_id: int) -> models.EventType:
    return db.query(models.EventType).filter(models.EventType.id == event_type_id).first()



# Пароль админа










