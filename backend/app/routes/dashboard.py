"""
Dashboard and reporting endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.database import get_db, Student, StudentInteraction, DriftAnalysis, Question

router = APIRouter()


@router.get("/overview")
def get_dashboard_overview(db: Session = Depends(get_db)):
    """Get overall dashboard overview"""
    total_students = db.query(func.count(Student.id)).scalar()
    total_interactions = db.query(func.count(StudentInteraction.id)).scalar()
    students_at_risk = db.query(func.count(DriftAnalysis.student_id)).filter(
        DriftAnalysis.alert_status == True
    ).distinct().scalar()
    
    return {
        "total_students": total_students,
        "total_interactions": total_interactions,
        "students_at_risk": students_at_risk,
        "timestamp": datetime.utcnow()
    }


@router.get("/student/{student_id}/summary")
def get_student_summary(student_id: int, db: Session = Depends(get_db)):
    """Get summary data for a student"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return {"error": "Student not found"}
    
    interactions = db.query(StudentInteraction).filter(
        StudentInteraction.student_id == student_id
    ).all()
    
    correct_count = sum(1 for i in interactions if i.is_correct)
    avg_time = sum(i.time_taken_seconds for i in interactions) / len(interactions) if interactions else 0
    
    return {
        "student_id": student_id,
        "student_name": student.name,
        "total_attempts": len(interactions),
        "correct_answers": correct_count,
        "accuracy": correct_count / len(interactions) if interactions else 0,
        "average_time_seconds": avg_time
    }


@router.get("/topic-performance")
def get_topic_performance(db: Session = Depends(get_db)):
    """Get performance metrics by topic"""
    topics = db.query(Question.topic).distinct().all()
    
    performance = {}
    for (topic,) in topics:
        interactions = db.query(StudentInteraction).join(
            Question, StudentInteraction.question_id == Question.id
        ).filter(Question.topic == topic).all()
        
        if interactions:
            correct = sum(1 for i in interactions if i.is_correct)
            performance[topic] = {
                "total_attempts": len(interactions),
                "correct": correct,
                "accuracy": correct / len(interactions)
            }
    
    return performance


@router.get("/recent-alerts")
def get_recent_alerts(hours: int = 24, db: Session = Depends(get_db)):
    """Get recent drift alerts"""
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    
    alerts = db.query(DriftAnalysis).filter(
        DriftAnalysis.alert_status == True,
        DriftAnalysis.analysis_timestamp >= cutoff_time
    ).all()
    
    return {
        "alert_count": len(alerts),
        "alerts": alerts,
        "time_window_hours": hours
    }
