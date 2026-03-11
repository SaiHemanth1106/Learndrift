# LearnDrift - AI System for Detecting Concept Drift in Student Learning Behavior

## 📋 Overview

LearnDrift is an AI-powered system designed to monitor and detect concept drift in student learning behavior on digital learning platforms. The system analyzes student interaction data and provides early alerts to instructors for timely academic intervention.

## ✨ Key Features

- **Behavioral Drift Detection**: Analyzes learning patterns to detect subtle behavioral shifts
- **Drift Score Calculation**: Probabilistic scoring indicating the likelihood of concept drift
- **Guessing Pattern Detection**: Identifies abnormal solving patterns suggesting guessing behavior
- **Concept Stability Index**: Measures consistency of conceptual understanding across topics
- **Instructor Insights**: AI-generated recommendations for targeted learning support
- **Real-time Monitoring**: Dashboard for tracking student learning trends
- **Early Alerts**: Automated alerts for students showing signs of concept drift

## 🏗️ System Architecture

```
Digital Learning Platform
        ↓
Interaction Data Collection
        ↓
Data Preprocessing & Feature Engineering
        ↓
Behavior Analysis Model
        ↓
Concept Drift Detection Engine
        ↓
Drift Score Generator
        ↓
Instructor Dashboard & Alert System
```

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: React.js with Recharts/Chart.js
- **Database**: PostgreSQL
- **Machine Learning**: Scikit-learn, TensorFlow
- **Deployment**: Docker, Docker Compose

## 📦 Project Structure

```
learndrift/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── models/
│   │   │   ├── database.py         # ORM models and database config
│   │   │   └── schemas.py          # Pydantic schemas
│   │   ├── routes/
│   │   │   ├── students.py         # Student management endpoints
│   │   │   ├── interactions.py     # Student interaction endpoints
│   │   │   ├── analysis.py         # Drift analysis endpoints
│   │   │   └── dashboard.py        # Dashboard endpoints
│   │   ├── ml/
│   │   │   └── drift_detector.py   # Drift detection algorithms
│   │   └── utils/
│   │       └── data_generator.py   # Synthetic data generation
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/             # React components
│   │   ├── pages/                  # Page components
│   │   ├── services/               # API service
│   │   ├── App.js
│   │   └── App.css
│   ├── package.json
│   ├── Dockerfile
├── database/
│   └── init.sql                    # Database schema
├── docker-compose.yml
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose (recommended)
- Python 3.11+ (for local setup)
- Node.js 18+ (for frontend local setup)
- PostgreSQL 15+ (for local setup)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd learndrift
   ```

2. **Start all services**
   ```bash
   docker-compose up
   ```

3. **Access the services**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Database: localhost:5432

### Local Setup (Without Docker)

#### Backend Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your PostgreSQL credentials
   ```

4. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm start
   ```

## 📊 Database Schema

### Students
Stores student information with enrollment details.

### Questions
Contains learning questions with topic and difficulty metadata.

### Student_Interactions
Records each student interaction:
- Timestamp
- Correct/Incorrect answer
- Time taken
- Retry attempts
- Confidence level

### Drift_Analysis
Stores drift detection results:
- Drift score (0-1)
- Alert status
- Topic analyzed
- Recommendation

## 🧠 Drift Detection Algorithm

LearnDrift uses a combination of machine learning algorithms:

1. **Page-Hinkley Test**: Detects concept drift by monitoring cumulative performance changes
2. **Accuracy Window Analysis**: Calculates performance over sliding windows
3. **Guessing Detection**: Identifies abnormal solving patterns (high retries, very low solving time)
4. **Concept Stability Index**: Measures consistency across attempts

### Drift Score Calculation

```
Final Drift Score = (Page-Hinkley Score × 0.6) + (Guessing Score × 0.4)
```

- Score > 0.7: High risk - immediate intervention recommended
- Score 0.5-0.7: Medium risk - close monitoring advised
- Score < 0.5: Low risk - stable learning behavior

## 📈 Dashboard Features

- **Overview Cards**: Total students, interactions, at-risk students
- **Drift Score Charts**: Visual representation of concept drift metrics
- **Topic Performance**: Accuracy and attempt metrics per topic
- **Alert Management**: View and manage drift alerts
- **Student Analysis**: Detailed interaction history and trend analysis

## 🔧 API Endpoints

### Students
- `GET /api/students` - List all students
- `POST /api/students` - Create new student
- `GET /api/students/{id}` - Get student details
- `PUT /api/students/{id}` - Update student
- `DELETE /api/students/{id}` - Delete student

### Interactions
- `POST /api/interactions` - Record student interaction
- `GET /api/interactions/student/{student_id}` - Get student interactions
- `GET /api/interactions/student/{student_id}/topic/{topic}` - Get topic interactions

### Analysis
- `POST /api/analysis/analyze/{student_id}` - Trigger drift analysis
- `GET /api/analysis/student/{student_id}` - Get student analysis
- `GET /api/analysis/alerts` - Get all drift alerts

### Dashboard
- `GET /api/dashboard/overview` - Dashboard overview
- `GET /api/dashboard/student/{student_id}/summary` - Student summary
- `GET /api/dashboard/topic-performance` - Topic performance metrics
- `GET /api/dashboard/recent-alerts` - Recent alerts

## 📝 Example: Recording a Student Interaction

```bash
curl -X POST http://localhost:8000/api/interactions \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "question_id": 1,
    "user_answer": "Answer A",
    "is_correct": true,
    "time_taken_seconds": 45.5,
    "retry_count": 1,
    "confidence": 0.8
  }'
```

## 🧪 Testing with Synthetic Data

Generate synthetic student data for testing:

```python
from app.utils.data_generator import generate_synthetic_data

generate_synthetic_data(num_students=20, num_questions=50)
```

## 📊 Analysis Example

```bash
# Trigger analysis for student
curl -X POST http://localhost:8000/api/analysis/analyze/1

# Get drift alerts
curl http://localhost:8000/api/analysis/alerts
```

## 🔐 Environment Configuration

Update `.env` file with your settings:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/learndrift
SECRET_KEY=your_secret_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## 📈 Future Enhancements

- Reinforcement learning-based personalized tutoring
- AI-generated learning recommendations
- Real-time learning analytics
- Integration with existing LMS platforms
- Advanced visualization dashboards
- Mobile application

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Create a feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit your changes (`git commit -m 'Add AmazingFeature'`)
3. Push to the branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

## 🎯 Project Impact

LearnDrift aims to:
- Detect conceptual misunderstandings early
- Enable data-driven teaching decisions
- Improve student learning outcomes
- Support adaptive learning environments
- Reduce student dropout rates

---

**LearnDrift** - Empowering Educators with AI-Driven Learning Insights