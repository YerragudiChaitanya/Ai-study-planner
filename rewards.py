from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.points.desc()).all()
    leaderboard = [{"username": user.username, "points": user.points} for user in users]
    return {"leaderboard": leaderboard}