from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Optional, List
import modules.models as models
from modules.database import engine, get_db, SessionLocal
import modules.minio_db as minio_db
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
        crud.init_event_types(db)
    finally:
        db.close()
    
    minio_db.init_minio("images-bucket")


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
    response_model=schemas.PollInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="See poll info and all submissions for a poll",
    responses={},
    tags=["Polls"]
)
def get_submissions_by_poll(poll_id: int, db: Session = Depends(get_db)):
    try:
        poll = crud.get_poll_data(db=db, poll_id=poll_id)
        submissions = crud.get_all_submissions_by_poll(db=db, poll_id=poll_id)

        poll_info = schemas.PollInfoResponse(
            poll_info = poll,
            submissions = submissions
        )

        return poll_info
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



















 # Голосование

@app.patch( # !!!!!!!!!!!!!!!!!!!!!!
    path="/polls/start/{poll_id}",
    response_model=schemas.PollResponse,
    status_code=status.HTTP_200_OK,
    summary="Start voting",
    responses={},
    tags=["Polls"]
)
def start_poll(poll_id: int, db: Session = Depends(get_db)):
    try:
        poll = crud.start_poll(db=db, poll_id=poll_id)
        if not poll:
            raise HTTPException(status_code=404, detail="Poll not found")
        return crud.get_poll_data(db=db, poll_id=poll.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post(
    path="/polls/vote",
    response_model=schemas.BallotResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cast a ballot",
    responses={},
    tags=["Polls"]
)
def add_ballot(ballot: schemas.BallotCreate, db: Session = Depends(get_db)):
    try:
        new_ballot = crud.add_new_ballot(db=db, ballot=ballot)
        return new_ballot
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch( # !!!!!!!!!!!!!!!!!!!!!!
    path="/polls/stop/{poll_id}",
    response_model=list[schemas.VotingStats],
    status_code=status.HTTP_200_OK,
    summary="Stop voting",
    responses={
        404: {"description": "Poll not found"},
        400: {"description": "Bad request - poll is not in votable state"},
        500: {"description": "Internal server error"}
    },
    tags=["Polls"]
)
def stop_poll(poll_id: int, db: Session = Depends(get_db)):
    try:
        voting_results = crud.stop_poll(db=db, poll_id=poll_id)
        return voting_results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
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



@app.get(
    path="/events/types",
    response_model=List[schemas.EventTypeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all event types list",
    responses={},
    tags=["Event types"]
)
def get_all_events(db: Session = Depends(get_db)):
    try:
        event_types = crud.get_all_event_types(db=db)
        if not event_types:
            raise HTTPException(status_code=404, detail="event typess not found")
        return event_types
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    path="/events/types/{event_type_id}",
    response_model=schemas.EventTypeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get event type data",
    responses={},
    tags=["Event types"]
)
def get_event_data(event_type_id: int, db: Session = Depends(get_db)):
    try:
        event_type = crud.get_event_type_data(db=db, event_type_id=event_type_id)
        if not event_type:
            raise HTTPException(status_code=404, detail="event type not found")
        return event_type
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post(
    path="/events/types/new",
    response_model=schemas.EventTypeResponse,
    status_code=status.HTTP_200_OK,
    summary="Create a new event type",
    responses={},
    tags=["Event types"]
)
def create_event(event_type: schemas.EventTypeCreate, db: Session = Depends(get_db)):
    try:
        new_event = crud.add_new_event_type(db=db, event_type=event_type)   
        return new_event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get(
    path="/events",
    response_model=List[schemas.EventResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all events list (with previous)",
    responses={},
    tags=["Events"]
)
def get_all_events(db: Session = Depends(get_db)):
    try:
        events = crud.get_all_events(db=db)
        if not events:
            raise HTTPException(status_code=404, detail="events not found")
        
        minio_client = minio_db.get_minio_client()
        
        result = []
        for event in events:
            event_data = event.__dict__.copy()
            
            if event.image_id:
                image_url = minio_client.get_file_url(
                    file_id=event.image_id,
                    folder="events"
                )
                event_data["image_url"] = image_url
            else:
                event_data["image_url"] = None
            
            result.append(schemas.EventResponse(**event_data))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post(
    path="/events/new",
    response_model=schemas.EventResponse,
    status_code=status.HTTP_200_OK,
    summary="Create a new event",
    responses={},
    tags=["Events"]
)
async def create_event(
    title: str = Form(...),
    date: str = Form(...),
    event_type_id: int = Form(...),
    description: Optional[str] = Form(None),
    submission_id: Optional[int] = Form(None),
    image_file: UploadFile = File(None),  
    db: Session = Depends(get_db)
):
    image_id = None
    
    if image_file:
        try:
            image_data = await image_file.read()
            
            minio_client = minio_db.get_minio_client()

            try:
                image_id = minio_client.upload_file(
                    file_data=image_data,
                    filename=image_file.filename,
                    folder="events"
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load image: {str(e)}")

    event = schemas.EventCreate(
        title=title,
        image_id=image_id,
        date=date,
        event_type_id=event_type_id,
        description=description if description else "",
        submission_id=submission_id if submission_id else 0
    )

    try:
        new_event = crud.add_new_event(db=db, event=event)   
        return new_event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get( 
    path="/events/{submission_id}",
    response_model=schemas.EventResponse,
    status_code=status.HTTP_200_OK,
    summary="See event data",
    responses={},
    tags=["Events"]
)
def get_event(event_id: int, db: Session = Depends(get_db)):
    try:
        event = crud.get_event_data_by_id(db=db, event_id=event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        

        minio_client = minio_db.get_minio_client()
        
        event_data = event.__dict__.copy()
        
        if event.image_id:
            image_url = minio_client.get_file_url(
                file_id=event.image_id,
                folder="events"
            )
            event_data["image_url"] = image_url
        else:
            event_data["image_url"] = None
        
        event_info = schemas.EventResponse(**event_data)
        return event_info
    
       
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


""" @app.delete( # !!!!!!!!!!!!!!!!!!!!!!
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
        raise HTTPException(status_code=500, detail=str(e)) """

""" @app.patch( # !!!!!!!!!!!!!!!!!!!!!!
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
        raise HTTPException(status_code=500, detail=str(e)) """


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



# тестовый эндпоинт для загрузки изображений

@app.post("/upload-event/")
async def upload_event(
    event_name: str = Form(...),
    organizer: str = Form(...),
    image: UploadFile = File(...)
):
    """
    Принимает multipart form data с названием мероприятия, именем организатора и изображением.
    Сохраняет изображение в MinIO и возвращает его id и длину названия и организатора.
    """
    
    # Читаем файл
    image_data = await image.read()
    
    # Получаем клиент MinIO
    minio_client = minio_db.get_minio_client()
    
    # Загружаем файл в MinIO (в папку events)
    try:
        file_id = minio_client.upload_file(
            file_data=image_data,
            filename=image.filename,
            folder="events"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")
    
    # Вычисляем длины
    event_name_length = len(event_name)
    organizer_length = len(organizer)
    
    return {
        "file_id": file_id,
        "event_name_length": event_name_length,
        "organizer_length": organizer_length,
        "message": "Image uploaded successfully"
    }


@app.get("/get-image/{file_id}")
async def get_image(file_id: str):
    """
    Возвращает изображение по его ID.
    """
    
    # Получаем клиент MinIO
    minio_client = minio_db.get_minio_client()
    
    # Проверяем существует ли файл
    if not minio_client.file_exists(file_id, folder="events"):
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        # Получаем данные файла
        image_data = minio_client.get_file_data(file_id, folder="events")
        
        # Получаем URL для определения content type
        # В реальном приложении лучше хранить content type в БД
        # Здесь используем прямое определение из расширения файла
        if '.' in file_id:
            ext = file_id.split('.')[-1].lower()
        else:
            ext = 'bin'
        
        # Определяем content type
        content_type = "application/octet-stream"
        if ext in ['jpg', 'jpeg']:
            content_type = 'image/jpeg'
        elif ext == 'png':
            content_type = 'image/png'
        elif ext == 'gif':
            content_type = 'image/gif'
        elif ext == 'webp':
            content_type = 'image/webp'
        elif ext == 'svg':
            content_type = 'image/svg+xml'
        
        # Возвращаем изображение
        return Response(
            content=image_data,
            media_type=content_type,
            headers={"Content-Disposition": f"inline; filename={file_id}"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve image: {str(e)}")

















@app.get("/health")
def health_check():
    return {"status": "healthy"}