-- LearnDrift Database Schema

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    course_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_students_email ON students(email);
CREATE INDEX idx_students_course_id ON students(course_id);

-- Questions table
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    topic VARCHAR(100) NOT NULL,
    difficulty_level VARCHAR(20),
    correct_answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_questions_topic ON questions(topic);
CREATE INDEX idx_questions_difficulty ON questions(difficulty_level);

-- Student interactions table
CREATE TABLE IF NOT EXISTS student_interactions (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    question_id INTEGER NOT NULL REFERENCES questions(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_answer TEXT,
    is_correct BOOLEAN NOT NULL,
    time_taken_seconds FLOAT NOT NULL,
    retry_count INTEGER DEFAULT 0,
    confidence FLOAT,
    CONSTRAINT fk_student FOREIGN KEY (student_id) REFERENCES students(id),
    CONSTRAINT fk_question FOREIGN KEY (question_id) REFERENCES questions(id)
);

CREATE INDEX idx_interactions_student ON student_interactions(student_id);
CREATE INDEX idx_interactions_question ON student_interactions(question_id);
CREATE INDEX idx_interactions_timestamp ON student_interactions(timestamp);

-- Drift analysis table
CREATE TABLE IF NOT EXISTS drift_analysis (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    topic VARCHAR(100) NOT NULL,
    drift_score FLOAT NOT NULL,
    alert_status BOOLEAN DEFAULT FALSE,
    analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recommendation TEXT,
    stability_index FLOAT,
    CONSTRAINT fk_drift_student FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE INDEX idx_drift_student ON drift_analysis(student_id);
CREATE INDEX idx_drift_alert ON drift_analysis(alert_status);
CREATE INDEX idx_drift_timestamp ON drift_analysis(analysis_timestamp);
