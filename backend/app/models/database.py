"""
Database connection and ORM models
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./learndrift.db")

# Handle SQLite and PostgreSQL
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
else:
    engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ORM Models
class Student(Base):
    """Student model"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    course_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Question(Base):
    """Question model"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    topic = Column(String, index=True)
    difficulty_level = Column(String)  # Easy, Medium, Hard
    correct_answer = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class StudentInteraction(Base):
    """Student interaction with questions"""
    __tablename__ = "student_interactions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    user_answer = Column(String)
    is_correct = Column(Boolean)
    time_taken_seconds = Column(Float)
    retry_count = Column(Integer, default=0)
    confidence = Column(Float)  # 0-1, student's self-assessed confidence


class DriftAnalysis(Base):
    """Drift analysis results"""
    __tablename__ = "drift_analysis"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True)
    topic = Column(String)
    drift_score = Column(Float)  # 0-1, probability of concept drift
    alert_status = Column(Boolean, default=False)
    analysis_timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    recommendation = Column(String)  # AI-generated recommendation
    stability_index = Column(Float)  # Concept stability
