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



def add_new_poll(db: Session, poll: schemas.PollCreate) -> models.Poll:
    db_poll = models.Poll(
        title = poll.title,
        state_id = 1,
        start = poll.start,
        end = poll.end,
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


# Пароль админа










