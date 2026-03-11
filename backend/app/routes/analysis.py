"""
Drift analysis endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.database import get_db, DriftAnalysis, StudentInteraction, Question
from app.models.schemas import DriftAnalysisResponse
from app.ml.drift_detector import analyze_student_drift

router = APIRouter()


@router.post("/analyze/{student_id}")
def trigger_drift_analysis(student_id: int, db: Session = Depends(get_db)):
    """Trigger drift analysis for a student"""
    # Get student interactions
    interactions = db.query(StudentInteraction).filter(
        StudentInteraction.student_id == student_id
    ).all()
    
    if not interactions:
        raise HTTPException(status_code=404, detail="No interactions found for this student")
    
    # Run drift detection
    results = analyze_student_drift(interactions, db)
    return results


@router.get("/student/{student_id}", response_model=List[DriftAnalysisResponse])
def get_student_drift_analysis(student_id: int, db: Session = Depends(get_db)):
    """Get drift analysis for a student"""
    analyses = db.query(DriftAnalysis).filter(
        DriftAnalysis.student_id == student_id
    ).all()
    return analyses


@router.get("/alerts")
def get_drift_alerts(db: Session = Depends(get_db)):
    """Get all students with drift alerts"""
    alerts = db.query(DriftAnalysis).filter(
        DriftAnalysis.alert_status == True
    ).all()
    return alerts


@router.get("/topic/{topic}", response_model=List[DriftAnalysisResponse])
def get_topic_drift_analysis(topic: str, db: Session = Depends(get_db)):
    """Get drift analysis for a specific topic"""
    analyses = db.query(DriftAnalysis).filter(
        DriftAnalysis.topic == topic
    ).all()
    return analyses
