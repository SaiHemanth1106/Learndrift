"""
Data generation utilities
"""
import random
import numpy as np
from datetime import datetime, timedelta
from app.models.database import SessionLocal, Student, Question, StudentInteraction


def generate_synthetic_data(num_students: int = 20, num_questions: int = 50):
    """Generate synthetic student data for testing"""
    db = SessionLocal()
    
    # Create students
    students = []
    for i in range(num_students):
        student = Student(
            name=f"Student_{i+1}",
            email=f"student{i+1}@learndrift.edu",
            course_id=1
        )
        db.add(student)
        students.append(student)
    
    db.commit()
    
    # Create questions with different topics
    topics = ["Algebra", "Geometry", "Trigonometry", "Calculus", "Statistics"]
    questions = []
    
    for i in range(num_questions):
        question = Question(
            title=f"Question_{i+1}",
            topic=random.choice(topics),
            difficulty_level=random.choice(["Easy", "Medium", "Hard"]),
            correct_answer=f"Answer_{i+1}"
        )
        db.add(question)
        questions.append(question)
    
    db.commit()
    
    # Create interactions with different patterns
    patterns = ["normal", "drift", "guessing", "improving"]
    
    for student in students:
        pattern = random.choice(patterns)
        base_time = datetime.utcnow() - timedelta(days=30)
        
        for q_idx, question in enumerate(questions):
            # Vary number of attempts per question
            num_attempts = random.randint(1, 3)
            
            for attempt in range(num_attempts):
                # Different patterns
                if pattern == "normal":
                    is_correct = random.random() > 0.3  # 70% accuracy
                    time_taken = random.uniform(30, 120)
                    retry_count = attempt
                
                elif pattern == "drift":
                    # Starts good, gets worse
                    progression = (q_idx / len(questions))
                    is_correct = random.random() > (0.3 + progression * 0.5)
                    time_taken = random.uniform(20, 150 + progression * 100)
                    retry_count = attempt + int(progression * 3)
                
                elif pattern == "guessing":
                    is_correct = random.random() > 0.5  # 50% accuracy
                    time_taken = random.uniform(5, 30)  # Very fast answers
                    retry_count = attempt + random.randint(1, 3)
                
                else:  # improving
                    # Starts bad, gets better
                    progression = (q_idx / len(questions))
                    is_correct = random.random() > (0.7 - progression * 0.4)
                    time_taken = random.uniform(150 - progression * 50, 200)
                    retry_count = max(0, 3 - int(progression * 3))
                
                interaction = StudentInteraction(
                    student_id=student.id,
                    question_id=question.id,
                    user_answer=f"Answer_{attempt}",
                    is_correct=is_correct,
                    time_taken_seconds=time_taken,
                    retry_count=retry_count,
                    confidence=random.uniform(0.2, 1.0),
                    timestamp=base_time + timedelta(days=q_idx * 0.5, hours=attempt * 2)
                )
                db.add(interaction)
    
    db.commit()
    db.close()
    print(f"Generated {num_students} students, {num_questions} questions with interactions")
