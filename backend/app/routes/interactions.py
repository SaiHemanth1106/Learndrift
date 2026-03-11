"""
Student interaction endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.database import get_db, StudentInteraction
from app.models.schemas import StudentInteractionCreate, StudentInteractionResponse

router = APIRouter()


@router.post("/", response_model=StudentInteractionResponse)
def record_interaction(interaction: StudentInteractionCreate, db: Session = Depends(get_db)):
    """Record a student interaction with a question"""
    db_interaction = StudentInteraction(**interaction.dict())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction


@router.get("/student/{student_id}", response_model=List[StudentInteractionResponse])
def get_student_interactions(student_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all interactions for a student"""
    interactions = db.query(StudentInteraction).filter(
        StudentInteraction.student_id == student_id
    ).offset(skip).limit(limit).all()
    return interactions


@router.get("/student/{student_id}/topic/{topic}", response_model=List[StudentInteractionResponse])
def get_student_topic_interactions(student_id: int, topic: str, db: Session = Depends(get_db)):
    """Get interactions for a specific topic"""
    from app.models.database import Question
    
    interactions = db.query(StudentInteraction).join(
        Question, StudentInteraction.question_id == Question.id
    ).filter(
        StudentInteraction.student_id == student_id,
        Question.topic == topic
    ).all()
    return interactions


@router.get("/{interaction_id}", response_model=StudentInteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Get a specific interaction"""
    interaction = db.query(StudentInteraction).filter(StudentInteraction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction
