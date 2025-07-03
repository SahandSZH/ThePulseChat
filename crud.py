from sqlalchemy.orm import Session
import schemas
from models import GroupChat, GameScore
from schemas import GroupCreate
from models import User
from schemas import UserCreate
from models import Membership
from models import Message
from fastapi import HTTPException
from schemas import GameScoreCreate


def get_group_by_name(db: Session, name: str):
    return db.query(GroupChat).filter(GroupChat.name == name).first()

def create_group(db: Session, group: GroupCreate):
    db_group = GroupChat(name=group.name, password=group.password)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_all_groups(db: Session):
    return db.query(GroupChat).all()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def save_new_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def add_user_to_group(db: Session, user_id: int, group_id: int):
    existing = db.query(Membership).filter(
        Membership.user_id == user_id,
        Membership.group_id == group_id
    ).first()

    if not existing:
        new_membership = Membership(user_id=user_id, group_id=group_id)
        db.add(new_membership)
        db.commit()

def get_user_groups(db: Session, user_id: int):
    return (
        db.query(GroupChat)
        .join(Membership, GroupChat.id == Membership.group_id)
        .filter(Membership.user_id == user_id)
        .all()
    )

def create_message(db: Session, message: schemas.MessageCreate):
    if message.reply_to_id is not None:
        replied_msg = db.query(Message).filter(
            Message.id == message.reply_to_id,
            Message.group_id == message.group_id
        ).first()
        if not replied_msg:
            raise HTTPException(status_code=400, detail="Invalid reply_to_id")
    new_message = Message(
        group_id=message.group_id,
        sender_id=message.sender_id,
        text=message.text,
        reply_to_id=message.reply_to_id,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def messages_by_group(db: Session, group_id: int):
    messages = (
        db.query(Message)
        .filter(Message.group_id == group_id)
        .order_by(Message.timestamp.asc())
        .all()
    )

    result = []
    for msg in messages:
        # Get reply text if needed
        reply_text = None
        if msg.reply_to_id:
            replied_msg = db.query(Message).filter(Message.id == msg.reply_to_id).first()
            if replied_msg:
                reply_text = replied_msg.text

        
        user = db.query(User).filter(User.id == msg.sender_id).first()
        sender_username = user.username if user else "Unknown"

        result.append({
            "id": msg.id,
            "group_id": msg.group_id,
            "sender_username": sender_username,  # ✅ send username instead of sender_id
            "text": msg.text,
            "timestamp": msg.timestamp,
            "reply_to_id": msg.reply_to_id,
            "reply_to_text": reply_text
        })

    return result


def submit_game_score(db: Session, game: GameScoreCreate):
    user = get_user_by_username(db, game.username)
    group = get_group_by_name(db, game.group_name)
    if not user or not group:
        raise HTTPException(status_code=404, detail="User or Group not found")

    db_score = GameScore(
        user_id=user.id,
        group_id=group.id,
        game_name=game.game_name,
        score=game.score
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)

    return {
        "username": user.username,
        "score": db_score.score,
        "timestamp": db_score.timestamp
    }


def get_leaderboard_by_group(db: Session, group_id: int, game_name: str):
    scores = (
        db.query(GameScore)
        .filter(GameScore.group_id == group_id, GameScore.game_name == game_name)
        .order_by(GameScore.score.desc())
        .limit(10)
        .all()
    )

    result = []
    for s in scores:
        user = db.query(User).filter(User.id == s.user_id).first()
        result.append({
            "username": user.username,
            "score": s.score,
            "timestamp": s.timestamp
        })

    return result
