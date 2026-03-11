# LearnDrift Development Guide

## Project Overview

LearnDrift is a full-stack application for detecting concept drift in student learning behavior.

## Running Locally (Without Docker)

### 1. Start PostgreSQL Database

```bash
# Using native PostgreSQL
createdb learndrift
psql learndrift < database/init.sql
```

Or use Docker just for the database:

```bash
docker run -d --name learndrift-db \
  -e POSTGRES_USER=learndrift_user \
  -e POSTGRES_PASSWORD=learndrift_password \
  -e POSTGRES_DB=learndrift \
  -p 5432:5432 \
  postgres:15
```

### 2. Start Backend Server

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env

# Initialize database with tables
python run_setup.py

# Start the server
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000

### 3. Start Frontend Development Server

```bash
cd frontend
npm install
npm start
```

Frontend will be available at: http://localhost:3000

## Using Docker Compose

### Start All Services

```bash
docker-compose up
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend
```

## API Testing

### Using FastAPI Swagger UI

Navigate to http://localhost:8000/docs to test all endpoints interactively.

### Using cURL

#### Create a Student

```bash
curl -X POST http://localhost:8000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "course_id": 1
  }'
```

#### Record an Interaction

```bash
curl -X POST http://localhost:8000/api/interactions \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "question_id": 1,
    "user_answer": "Option A",
    "is_correct": true,
    "time_taken_seconds": 45.5,
    "retry_count": 1,
    "confidence": 0.8
  }'
```

#### Trigger Drift Analysis

```bash
curl -X POST http://localhost:8000/api/analysis/analyze/1
```

#### Get Dashboard Overview

```bash
curl http://localhost:8000/api/dashboard/overview
```

## Project Structure Details

### Backend (`/backend`)

- **app/main.py** - FastAPI application setup
- **app/models/database.py** - SQLAlchemy ORM models
- **app/models/schemas.py** - Pydantic request/response schemas
- **app/routes/** - API route handlers
- **app/ml/drift_detector.py** - Concept drift detection algorithms
- **app/utils/data_generator.py** - Synthetic data generation

### Frontend (`/frontend`)

- **src/pages/** - Page components (Dashboard, StudentAnalysis, Alerts)
- **src/components/** - Reusable components (Charts)
- **src/services/api.js** - API client service
- **src/App.js** - Main app component

### Database (`/database`)

- **init.sql** - Database schema initialization script

## Common Tasks

### Generate Synthetic Data

Inside a Python shell with the backend environment:

```python
from app.utils.data_generator import generate_synthetic_data
generate_synthetic_data(num_students=50, num_questions=100)
```

### Run Backend Tests

```bash
cd backend
pytest
```

### Build Production Docker Images

```bash
docker-compose build --prod
```

### Access Database Shell

```bash
# Within Docker container
docker-compose exec postgres psql -U learndrift_user -d learndrift

# Locally
psql -U learndrift_user -d learndrift -h localhost
```

### Common SQL Queries

```sql
-- Count students
SELECT COUNT(*) FROM students;

-- Get students with high drift scores
SELECT s.name, da.drift_score, da.topic 
FROM students s 
JOIN drift_analysis da ON s.id = da.student_id 
WHERE da.drift_score > 0.7;

-- Get interaction statistics
SELECT is_correct, COUNT(*) as count 
FROM student_interactions 
GROUP BY is_correct;
```

## Troubleshooting

### Backend won't start

1. Check PostgreSQL is running
2. Verify DATABASE_URL in .env
3. Try creating tables: `python backend/run_setup.py`

### Frontend won't start

1. Clear node_modules: `rm -rf node_modules && npm install`
2. Clear npm cache: `npm cache clean --force`
3. Check for port 3000 conflicts

### Database connection issues

1. Verify PostgreSQL credentials
2. Check if database exists: `psql -l`
3. Check port 5432 is not in use

### Docker issues

1. Clean up: `docker-compose down -v`
2. Rebuild: `docker-compose build --no-cache`
3. Check images: `docker images`
4. Check containers: `docker ps -a`

## Contributing Guidelines

1. Create feature branches: `git checkout -b feature/feature-name`
2. Follow PEP 8 for Python code
3. Use functional components in React
4. Add docstrings to functions
5. Write tests for new features
6. Update README if adding new features

---

For more information, see the main [README.md](../README.md)
