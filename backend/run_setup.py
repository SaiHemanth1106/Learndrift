"""
LearnDrift Backend - Main entry point setup script
Run this to initialize the database with sample data
"""

if __name__ == "__main__":
    from app.models.database import engine, Base
    from app.utils.data_generator import generate_synthetic_data
    
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    print("\nGenerating synthetic data...")
    generate_synthetic_data(num_students=20, num_questions=50)
    print("✓ Synthetic data generated")
    
    print("\nLearnDrift backend is ready!")
    print("Run 'uvicorn app.main:app --reload' to start the API server")
