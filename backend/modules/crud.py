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



def add_new_ballot(db: Session, ballot: schemas.BallotCreate) -> models.Ballot:
    db_ballot = models.Ballot(
        poll_id = ballot.poll_id,
        rankings = ballot.rankings,
        created_at = datetime.now()
    )
    db.add(db_ballot)
    db.commit()
    db.refresh(db_ballot)
    return db_ballot






def start_poll(db: Session, poll_id: int) -> models.Poll:
    poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    if not poll:
        return None

    if poll.state_id == 1:
        poll.state_id = 2
        db.commit()
        db.refresh(poll)
    return db.query(models.Poll).filter(models.Poll.id == poll_id).options(selectinload(models.Poll.state)).first()


def stop_poll(db: Session, poll_id: int) -> list[schemas.VotingStats]: 
    poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    if not poll:
        raise ValueError("Poll not found")

    if poll.state_id != 2:
        raise ValueError(f"Poll is not in votable state. Current state_id: {poll.state_id}")

    try:

        ballots = db.query(models.Ballot).filter(models.Ballot.poll_id == poll_id).all()
        ballots_list = [ballot.rankings for ballot in ballots]
        # !!!!!!!!! Сделать проверку, что все айдишки есть в таблице submissions

        if not ballots_list:
            raise ValueError("No ballots found for this poll")
        
        if poll.winners <= 0:
            raise ValueError(f"Invalid winners count: {poll.winners}")
        
        election_results = utils.commit_voting(
            ballots_list=ballots_list,
            winners_count=poll.winners
            )
        
        if not election_results:
            raise ValueError("Vote counting failed - no results returned")
        
        sorted_election_results = sorted(election_results, key=lambda x: x['number_of_votes'], reverse=True)

        submissions = db.query(models.Submission).filter(models.Submission.poll_id == poll_id).all()
        submission_dict = {submission.id: submission for submission in submissions}


        full_election_results = []

        for index, result in enumerate(sorted_election_results):
            full_election_results.append(
                schemas.VotingStats(
                    rank = index + 1,
                    submission = submission_dict[result['submission_id']],
                    number_of_votes = result['number_of_votes'],
                    status = result['status']
                )
            )

        poll.state_id = 3
        db.commit()
        db.refresh(poll)

        return full_election_results
    
    except ValueError as e:
        db.rollback()
        raise e
        
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error processing poll results: {str(e)}")


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
        image_id = event.image_id, # доделать работу с изображениями
        date = event.date,
        event_type_id = event.event_type_id,
        description = event.description,
        submission_id = event.submission_id if event.submission_id else None,
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










