from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, StudyPlan, User

router = APIRouter()

class StudyPlanCreate(BaseModel):
    user_id: int
    subject: str
    time_allocated: int

class StudyProgressUpdate(BaseModel):
    user_id: int
    minutes_studied: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_study_plan(plan: StudyPlanCreate, db: Session = Depends(get_db)):
    new_plan = StudyPlan(user_id=plan.user_id, subject=plan.subject, time_allocated=plan.time_allocated)
    db.add(new_plan)
    db.commit()
    return {"message": f"Study plan for {plan.subject} created"}

@router.post("/update-progress")
def update_study_progress(progress: StudyProgressUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == progress.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    study_plan = db.query(StudyPlan).filter(StudyPlan.user_id == progress.user_id).first_