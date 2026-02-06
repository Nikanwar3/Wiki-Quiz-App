from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from dotenv import load_dotenv

from database import WikiQuiz, init_db, get_db
from scraper import WikipediaScraper, validate_wikipedia_url
from quiz_generator import QuizGenerator

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Wiki Quiz API",
    description="Generate quizzes from Wikipedia articles using LLM",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    print("Database initialized successfully!")


# Pydantic models for request/response
class QuizGenerateRequest(BaseModel):
    url: str


class QuizResponse(BaseModel):
    id: int
    url: str
    title: str
    summary: str
    key_entities: dict
    sections: List[str]
    quiz: List[dict]
    related_topics: List[str]
    created_at: str

    class Config:
        from_attributes = True


class QuizHistoryItem(BaseModel):
    id: int
    url: str
    title: str
    created_at: str

    class Config:
        from_attributes = True


# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Wiki Quiz API is running!",
        "version": "1.0.0",
        "endpoints": {
            "generate_quiz": "/api/quiz/generate",
            "get_all_quizzes": "/api/quiz/history",
            "get_quiz_by_id": "/api/quiz/{quiz_id}"
        }
    }


@app.post("/api/quiz/generate", response_model=QuizResponse)
async def generate_quiz(
    request: QuizGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a quiz from a Wikipedia URL
    
    Steps:
    1. Validate URL
    2. Check if already in database (caching)
    3. Scrape Wikipedia article
    4. Generate quiz using LLM
    5. Store in database
    6. Return results
    """
    url = request.url.strip()
    
    # Validate Wikipedia URL
    if not validate_wikipedia_url(url):
        raise HTTPException(
            status_code=400,
            detail="Invalid Wikipedia URL. Please provide a valid English Wikipedia article URL."
        )
    
    try:
        # Check cache - if URL already processed, return cached result
        existing_quiz = db.query(WikiQuiz).filter(WikiQuiz.url == url).first()
        if existing_quiz:
            return QuizResponse(
                id=existing_quiz.id,
                url=existing_quiz.url,
                title=existing_quiz.title,
                summary=existing_quiz.summary,
                key_entities=existing_quiz.key_entities,
                sections=existing_quiz.sections,
                quiz=existing_quiz.quiz,
                related_topics=existing_quiz.related_topics,
                created_at=existing_quiz.created_at.isoformat()
            )
        
        # Step 1: Scrape Wikipedia
        print(f"Scraping Wikipedia: {url}")
        scraper = WikipediaScraper(url)
        scraped_data = scraper.scrape()
        
        # Step 2: Generate quiz using LLM
        print("Generating quiz with LLM...")
        quiz_gen = QuizGenerator()
        
        quiz_questions = quiz_gen.generate_quiz(
            title=scraped_data['title'],
            content=scraped_data['full_text'],
            num_questions=7  # Generate 7 questions
        )
        
        # Step 3: Generate related topics
        print("Generating related topics...")
        related_topics = quiz_gen.generate_related_topics(
            title=scraped_data['title'],
            summary=scraped_data['summary'],
            sections=scraped_data['sections']
        )
        
        # Step 4: Store in database
        print("Storing in database...")
        db_quiz = WikiQuiz(
            url=url,
            title=scraped_data['title'],
            summary=scraped_data['summary'],
            key_entities=scraped_data['key_entities'],
            sections=scraped_data['sections'],
            quiz=quiz_questions,
            related_topics=related_topics,
            raw_html=scraped_data['raw_html']  # Bonus: store raw HTML
        )
        
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        
        print(f"Quiz generated successfully! ID: {db_quiz.id}")
        
        # Return response
        return QuizResponse(
            id=db_quiz.id,
            url=db_quiz.url,
            title=db_quiz.title,
            summary=db_quiz.summary,
            key_entities=db_quiz.key_entities,
            sections=db_quiz.sections,
            quiz=db_quiz.quiz,
            related_topics=db_quiz.related_topics,
            created_at=db_quiz.created_at.isoformat()
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating quiz: {str(e)}"
        )


@app.get("/api/quiz/history", response_model=List[QuizHistoryItem])
async def get_quiz_history(db: Session = Depends(get_db)):
    """
    Get all previously generated quizzes (for history tab)
    Returns basic info: id, url, title, created_at
    """
    try:
        quizzes = db.query(WikiQuiz).order_by(WikiQuiz.created_at.desc()).all()
        
        return [
            QuizHistoryItem(
                id=quiz.id,
                url=quiz.url,
                title=quiz.title,
                created_at=quiz.created_at.isoformat()
            )
            for quiz in quizzes
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching quiz history: {str(e)}"
        )


@app.get("/api/quiz/{quiz_id}", response_model=QuizResponse)
async def get_quiz_by_id(quiz_id: int, db: Session = Depends(get_db)):
    """
    Get full quiz details by ID (for modal in history tab)
    """
    try:
        quiz = db.query(WikiQuiz).filter(WikiQuiz.id == quiz_id).first()
        
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        return QuizResponse(
            id=quiz.id,
            url=quiz.url,
            title=quiz.title,
            summary=quiz.summary,
            key_entities=quiz.key_entities,
            sections=quiz.sections,
            quiz=quiz.quiz,
            related_topics=quiz.related_topics,
            created_at=quiz.created_at.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching quiz: {str(e)}"
        )


@app.delete("/api/quiz/{quiz_id}")
async def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """Delete a quiz by ID (optional endpoint)"""
    try:
        quiz = db.query(WikiQuiz).filter(WikiQuiz.id == quiz_id).first()
        
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        db.delete(quiz)
        db.commit()
        
        return {"message": "Quiz deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting quiz: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"""
    ╔══════════════════════════════════════════╗
    ║     Wiki Quiz API Server Starting       ║
    ╚══════════════════════════════════════════╝
    
    🚀 Server: http://{host}:{port}
    📚 Docs: http://{host}:{port}/docs
    📖 ReDoc: http://{host}:{port}/redoc
    
    Press CTRL+C to stop
    """)
    
    uvicorn.run("main:app", host=host, port=port, reload=True)
