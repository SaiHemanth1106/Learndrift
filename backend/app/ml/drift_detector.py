"""
Concept drift detection algorithms
"""
import numpy as np
from typing import List, Dict
from app.models.database import StudentInteraction, DriftAnalysis, Question
from sqlalchemy.orm import Session


def calculate_accuracy_window(interactions: List[StudentInteraction], window_size: int = 5) -> List[float]:
    """
    Calculate accuracy over sliding windows of interactions
    """
    if not interactions or window_size <= 0:
        return []
    
    sorted_interactions = sorted(interactions, key=lambda x: x.timestamp)
    accuracies = []
    
    for i in range(len(sorted_interactions) - window_size + 1):
        window = sorted_interactions[i:i + window_size]
        correct = sum(1 for interaction in window if interaction.is_correct)
        accuracy = correct / window_size
        accuracies.append(accuracy)
    
    return accuracies


def calculate_guessing_score(interactions: List[StudentInteraction]) -> float:
    """
    Detect guessing behavior based on:
    - High retry count with wrong answers
    - Very low time per question (suggests guessing)
    - Inconsistent performance
    """
    if not interactions:
        return 0.0
    
    high_retry_wrong = sum(1 for i in interactions if i.retry_count > 2 and not i.is_correct)
    avg_time = np.mean([i.time_taken_seconds for i in interactions]) if interactions else 0
    
    # If questions are solved too quickly, might be guessing
    quick_answers = sum(1 for i in interactions if i.time_taken_seconds < 5)
    
    guessing_indicators = (high_retry_wrong / len(interactions)) * 0.4 + \
                         (quick_answers / len(interactions)) * 0.3
    
    return min(guessing_indicators, 1.0)


def page_hinkley_test(accuracies: List[float], threshold: float = 0.5) -> float:
    """
    Page-Hinkley drift detection test
    Returns drift score between 0 and 1
    """
    if len(accuracies) < 2:
        return 0.0
    
    mean_val = np.mean(accuracies)
    cumsum = 0
    max_cumsum = 0
    
    for acc in accuracies:
        cumsum += (acc - mean_val)
        max_cumsum = max(max_cumsum, abs(cumsum))
    
    drift_score = min(max_cumsum / threshold if threshold > 0 else 0, 1.0)
    return float(drift_score)


def calculate_stability_index(interactions: List[StudentInteraction]) -> float:
    """
    Calculate concept stability index (0-1)
    Higher values = more stable understanding
    """
    if len(interactions) < 2:
        return 1.0
    
    accuracies = [1.0 if i.is_correct else 0.0 for i in interactions]
    variance = np.var(accuracies)
    
    # Stability is inverse of variance
    stability = 1.0 - min(variance, 1.0)
    return float(stability)


def analyze_student_drift(interactions: List[StudentInteraction], db: Session) -> Dict:
    """
    Comprehensive drift analysis for a student
    """
    if not interactions:
        return {"error": "No interactions found"}
    
    student_id = interactions[0].student_id
    groups_by_topic = {}
    
    # Group interactions by topic
    for interaction in interactions:
        question = db.query(Question).filter(Question.id == interaction.question_id).first()
        if question:
            if question.topic not in groups_by_topic:
                groups_by_topic[question.topic] = []
            groups_by_topic[question.topic].append(interaction)
    
    results = []
    avg_drift_score = 0
    alert_count = 0
    
    # Analyze each topic
    for topic, topic_interactions in groups_by_topic.items():
        sorted_interactions = sorted(topic_interactions, key=lambda x: x.timestamp)
        
        # Calculate metrics
        accuracies = calculate_accuracy_window(sorted_interactions, window_size=3)
        drift_score = page_hinkley_test(accuracies, threshold=0.3)
        guessing_score = calculate_guessing_score(sorted_interactions)
        stability_index = calculate_stability_index(sorted_interactions)
        
        # Combine scores
        final_drift_score = (drift_score * 0.6 + guessing_score * 0.4)
        
        # Determine alert
        alert_status = final_drift_score > 0.5
        
        # Generate recommendation
        recommendation = generate_recommendation(final_drift_score, stability_index, guessing_score)
        
        # Store in database
        analysis = DriftAnalysis(
            student_id=student_id,
            topic=topic,
            drift_score=final_drift_score,
            alert_status=alert_status,
            stability_index=stability_index,
            recommendation=recommendation
        )
        db.add(analysis)
        
        results.append({
            "topic": topic,
            "drift_score": float(final_drift_score),
            "stability_index": float(stability_index),
            "guessing_score": float(guessing_score),
            "alert_status": bool(alert_status),
            "recommendation": recommendation
        })
        
        avg_drift_score += final_drift_score
        if alert_status:
            alert_count += 1
    
    db.commit()
    
    return {
        "student_id": student_id,
        "analysis_count": len(results),
        "average_drift_score": float(avg_drift_score / len(results)) if results else 0,
        "alert_count": alert_count,
        "topics_analyzed": list(groups_by_topic.keys()),
        "detailed_results": results
    }


def generate_recommendation(drift_score: float, stability_index: float, guessing_score: float) -> str:
    """
    Generate AI-based recommendation for instructors
    """
    if drift_score > 0.7:
        if guessing_score > 0.6:
            return "High guessing behavior detected. Recommend one-on-one tutoring and concept review."
        else:
            return "Significant concept drift detected. Suggest targeted practice problems and review sessions."
    elif drift_score > 0.5:
        return "Moderate drift detected. Monitor student progress closely and provide additional practice."
    else:
        return "Learning behavior is stable. Continue current instructional approach."
