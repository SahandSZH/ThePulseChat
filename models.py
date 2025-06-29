from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from sqlalchemy import ForeignKey
from datetime import datetime



class GroupChat(Base):
    __tablename__ = "group_chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Membership(Base):
    __tablename__ = "membership"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("group_chats.id"), primary_key=True)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("group_chats.id"))
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    reply_to_id = Column(Integer, ForeignKey("messages.id"), nullable=True)

class GameScore(Base):
    __tablename__ = "game_scores"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("group_chats.id"), nullable=False)
    game_name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
