from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GroupCreate(BaseModel):
    name: str
    password: str

class GroupOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class GroupJoinRequest(BaseModel):
    group_name: str
    group_password: str
    username: str
    user_password: str

class MessageCreate(BaseModel):
    group_id: int
    sender_id: int
    text: str
    reply_to_id: Optional[int] = None

class MessageOut(BaseModel):
    id: int
    group_id: int
    sender_username: str
    text: str
    timestamp: datetime
    reply_to_id: Optional[int]
    reply_to_text: Optional[str]=None

    class Config:
        orm_mode = True


class GameScoreCreate(BaseModel):
    username: str
    group_name: str
    game_name: str
    score: int


class GameScoreOut(BaseModel):
    username: str
    score: int
    timestamp: datetime

    class Config:
        orm_mode = True

