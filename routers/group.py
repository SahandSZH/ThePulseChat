from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, schemas
from typing import List

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_group", response_model=schemas.GroupOut)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    existing = crud.get_group_by_name(db, name=group.name)
    if existing:
        raise HTTPException(status_code=400, detail="Group already exists")
    return crud.create_group(db=db, group=group)


@router.post("/join_group")
def join_group(request: schemas.GroupJoinRequest, db: Session = Depends(get_db)):

    user = crud.get_user_by_username(db, request.username)
    if not user or user.password != request.user_password:
        raise HTTPException(status_code=403, detail="Invalid username or password")

    group = crud.get_group_by_name(db, request.group_name)
    if not group or group.password != request.group_password:
        raise HTTPException(status_code=403, detail="Invalid group name or password")

    crud.add_user_to_group(db, user_id=user.id, group_id=group.id)

    return {"message": "Joined successfully!"}


@router.get("/groups", response_model=list[schemas.GroupOut])
def get_groups(db: Session = Depends(get_db)):
    return crud.get_all_groups(db)

@router.post("/register_user", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_username(db, username=user.username)
    if existing:
        raise HTTPException(status_code=400, detail="This username already exists!")
    return crud.save_new_user(db=db, user=user)

@router.get("/my_groups/{username}", response_model=List[schemas.GroupOut])
def get_user_groups(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return crud.get_user_groups(db=db, user_id=user.id)

@router.post("/send_message", response_model=schemas.MessageOut)
def send_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message)

@router.get("/messages/{group_id}", response_model=List[schemas.MessageOut])
def get_group_messages(group_id: int, db: Session = Depends(get_db)):
    return crud.messages_by_group(db, group_id)

@router.post("/submit_score", response_model=schemas.GameScoreOut)
def submit_score(game: schemas.GameScoreCreate, db: Session = Depends(get_db)):
    return crud.submit_game_score(db=db, game=game)

@router.get("/leaderboard/{group_id}/{game_name}", response_model=list[schemas.GameScoreOut])
def get_leaderboard(group_id: int, game_name: str, db: Session = Depends(get_db)):
    return crud.get_leaderboard_by_group(db=db, group_id=group_id, game_name=game_name)



@router.get("/user/{username}", response_model=schemas.UserOut)
def get_user_by_username_endpoint(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=403, detail="Invalid username or password")
    return {"message": "Login successful", "username": user.username}

