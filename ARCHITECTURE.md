# 🏗️ System Architecture

## Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                     (Frontend - index.html)                     │
│                                                                 │
│  ┌──────────────┐              ┌──────────────┐               │
│  │  TAB 1:      │              │  TAB 2:      │               │
│  │  Generate    │              │  History     │               │
│  │  Quiz        │              │  View        │               │
│  └──────────────┘              └──────────────┘               │
│         │                              │                        │
└─────────┼──────────────────────────────┼────────────────────────┘
          │                              │
          │ HTTP POST /api/quiz/generate │ HTTP GET /api/quiz/history
          │                              │ HTTP GET /api/quiz/{id}
          ▼                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                            │
│                      (main.py - Port 8000)                      │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              API ENDPOINTS                             │   │
│  │  • POST /api/quiz/generate                            │   │
│  │  • GET  /api/quiz/history                             │   │
│  │  • GET  /api/quiz/{quiz_id}                           │   │
│  │  • DELETE /api/quiz/{quiz_id}                         │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │   Scraper    │    │    Quiz      │    │   Database   │    │
│  │   Module     │───▶│  Generator   │───▶│   Module     │    │
│  │ (scraper.py) │    │(quiz_gen.py) │    │(database.py) │    │
│  └──────────────┘    └──────────────┘    └──────────────┘    │
│         │                     │                    │           │
└─────────┼─────────────────────┼────────────────────┼───────────┘
          │                     │                    │
          ▼                     ▼                    ▼
    Wikipedia API         Google Gemini        PostgreSQL DB
    (beautifulsoup)         (LangChain)        (wiki_quiz_db)
```

## Data Flow

### 1. Quiz Generation Flow

```
User enters URL
      │
      ▼
Frontend sends POST request
      │
      ▼
Backend validates URL
      │
      ├─── Check cache (database)
      │    └─── If exists, return cached quiz
      │
      ▼
Scraper fetches Wikipedia page
      │
      ├─── Extract title
      ├─── Extract summary
      ├─── Extract sections
      ├─── Extract entities (people, orgs, locations)
      └─── Extract full text
      │
      ▼
Quiz Generator (LLM)
      │
      ├─── Generate quiz questions
      │    └─── Uses LangChain + Gemini
      │         • Question
      │         • 4 Options
      │         • Correct answer
      │         • Explanation
      │         • Difficulty level
      │
      └─── Generate related topics
      │
      ▼
Store in PostgreSQL
      │
      ▼
Return JSON response
      │
      ▼
Frontend displays quiz
```

### 2. History View Flow

```
User clicks "Quiz History" tab
      │
      ▼
Frontend sends GET /api/quiz/history
      │
      ▼
Backend queries database
      │
      ▼
Returns list of all quizzes
      │
      ▼
Frontend displays table
      │
User clicks "View Details"
      │
      ▼
Frontend sends GET /api/quiz/{id}
      │
      ▼
Backend fetches specific quiz
      │
      ▼
Returns full quiz data
      │
      ▼
Frontend shows modal with quiz
```

## Technology Stack

```
┌───────────────────────────────────────────────────────┐
│                    FRONTEND                           │
│  • HTML5 / CSS3 / JavaScript (Vanilla)               │
│  • Responsive Design                                  │
│  • Fetch API for HTTP requests                       │
│  • No build tools needed!                            │
└───────────────────────────────────────────────────────┘
                        │
                        │ HTTP/JSON
                        │
┌───────────────────────────────────────────────────────┐
│                    BACKEND                            │
│  • FastAPI (Python web framework)                    │
│  • Uvicorn (ASGI server)                             │
│  • Pydantic (data validation)                        │
│  • SQLAlchemy (ORM)                                   │
│  • BeautifulSoup4 (web scraping)                     │
│  • LangChain (LLM framework)                         │
└───────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Wikipedia  │  │   Google    │  │ PostgreSQL  │
│   Articles  │  │   Gemini    │  │  Database   │
│             │  │     API     │  │             │
│ Data Source │  │   LLM AI    │  │   Storage   │
└─────────────┘  └─────────────┘  └─────────────┘
```

## Database Schema

```
Table: wiki_quizzes
┌────────────────┬──────────────┬──────────────────────────────┐
│     Column     │     Type     │         Description          │
├────────────────┼──────────────┼──────────────────────────────┤
│ id             │ INTEGER      │ Primary key (auto-increment) │
│ url            │ STRING       │ Wikipedia URL (unique)       │
│ title          │ STRING       │ Article title                │
│ summary        │ TEXT         │ Article summary              │
│ key_entities   │ JSON         │ {people, orgs, locations}    │
│ sections       │ JSON         │ Array of section names       │
│ quiz           │ JSON         │ Array of quiz questions      │
│ related_topics │ JSON         │ Array of related topics      │
│ raw_html       │ TEXT         │ Original HTML (optional)     │
│ created_at     │ DATETIME     │ Timestamp                    │
│ updated_at     │ DATETIME     │ Timestamp                    │
└────────────────┴──────────────┴──────────────────────────────┘
```

## API Request/Response Examples

### Generate Quiz Request
```http
POST http://localhost:8000/api/quiz/generate
Content-Type: application/json

{
  "url": "https://en.wikipedia.org/wiki/Alan_Turing"
}
```

### Generate Quiz Response
```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Alan_Turing",
  "title": "Alan Turing",
  "summary": "Alan Mathison Turing OBE FRS was an English mathematician...",
  "key_entities": {
    "people": ["Alan Turing", "Alonzo Church"],
    "organizations": ["University of Cambridge", "Bletchley Park"],
    "locations": ["United Kingdom", "Manchester"]
  },
  "sections": ["Early life", "World War II", "Legacy"],
  "quiz": [
    {
      "question": "Where did Alan Turing study?",
      "options": ["Harvard", "Cambridge", "Oxford", "Princeton"],
      "answer": "Cambridge",
      "difficulty": "easy",
      "explanation": "Mentioned in Early life section."
    }
  ],
  "related_topics": ["Cryptography", "Enigma machine"],
  "created_at": "2024-02-06T10:30:00"
}
```

## LLM Prompt Engineering

### Quiz Generation Prompt Structure

```
┌──────────────────────────────────────────────────┐
│         SYSTEM INSTRUCTION                       │
│  "You are an expert quiz creator..."            │
└──────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│         ARTICLE CONTEXT                          │
│  • Title: {title}                                │
│  • Content: {full_article_text}                  │
└──────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│         INSTRUCTIONS                             │
│  • Create {num_questions} questions              │
│  • Mix difficulty levels                         │
│  • Only use facts from article                   │
│  • Provide explanations                          │
└──────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│         OUTPUT FORMAT                            │
│  JSON structure with:                            │
│  • question, options, answer, difficulty,        │
│    explanation                                   │
└──────────────────────────────────────────────────┘
                    │
                    ▼
           Gemini LLM processes
                    │
                    ▼
           Structured quiz output
```

## Security & Best Practices

```
┌──────────────────────────────────────────────────┐
│  Security Measures                               │
├──────────────────────────────────────────────────┤
│  ✓ Environment variables for secrets            │
│  ✓ SQL injection protection (SQLAlchemy ORM)    │
│  ✓ CORS configuration for API access            │
│  ✓ URL validation before scraping               │
│  ✓ Rate limiting on Gemini API                  │
│  ✓ Error handling for failed requests           │
│  ✓ .gitignore for sensitive files               │
└──────────────────────────────────────────────────┘
```

## Performance Optimizations

```
┌──────────────────────────────────────────────────┐
│  Optimization Strategies                         │
├──────────────────────────────────────────────────┤
│  ✓ Database caching (prevent duplicate scrapes) │
│  ✓ Text truncation (limit LLM input tokens)     │
│  ✓ Async operations where possible              │
│  ✓ Connection pooling for database              │
│  ✓ Efficient BeautifulSoup parsing              │
│  ✓ Index on URL column for fast lookups         │
└──────────────────────────────────────────────────┘
```

## Scalability Considerations

For production deployment:

```
Current Setup (Development)
  └─ Single server
  └─ Local PostgreSQL
  └─ No caching layer

Production Recommendations
  ├─ Load Balancer
  ├─ Multiple API servers
  ├─ Redis for caching
  ├─ Managed PostgreSQL (AWS RDS, etc.)
  ├─ CDN for frontend
  └─ Background job queue for quiz generation
```
