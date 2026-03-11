"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StudentCreate(BaseModel):
    """Schema for creating a student"""
    name: str
    email: str
    course_id: int


class StudentResponse(BaseModel):
    """Schema for student response"""
    id: int
    name: str
    email: str
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    """Schema for creating a question"""
    title: str
    topic: str
    difficulty_level: str
    correct_answer: str


class StudentInteractionCreate(BaseModel):
    """Schema for recording student interaction"""
    student_id: int
    question_id: int
    user_answer: str
    is_correct: bool
    time_taken_seconds: float
    retry_count: int = 0
    confidence: Optional[float] = None


class StudentInteractionResponse(BaseModel):
    """Schema for student interaction response"""
    id: int
    student_id: int
    question_id: int
    timestamp: datetime
    user_answer: str
    is_correct: bool
    time_taken_seconds: float
    retry_count: int

    class Config:
        from_attributes = True


class DriftAnalysisResponse(BaseModel):
    """Schema for drift analysis response"""
    id: int
    student_id: int
    topic: str
    drift_score: float
    alert_status: bool
    analysis_timestamp: datetime
    recommendation: Optional[str]
    stability_index: float

    class Config:
        from_attributes = True
