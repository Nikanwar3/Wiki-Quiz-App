from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/wiki_quiz_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class WikiQuiz(Base):
    """Database model for storing Wikipedia quiz data"""
    __tablename__ = "wiki_quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)
    key_entities = Column(JSON)  # Stores people, organizations, locations
    sections = Column(JSON)  # List of section titles
    quiz = Column(JSON)  # List of quiz questions
    related_topics = Column(JSON)  # List of related topics
    raw_html = Column(Text, nullable=True)  # Bonus: store raw HTML
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def init_db():
    """Initialize the database"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
