# 📚 Wiki Quiz Generator

An intelligent quiz generation system that transforms Wikipedia articles into interactive quizzes using AI (Google Gemini).

## 🌟 Features

- **Automatic Quiz Generation**: Scrapes Wikipedia articles and generates quizzes using LLM
- **Smart Question Design**: Creates easy, medium, and hard difficulty questions
- **Entity Extraction**: Identifies key people, organizations, and locations
- **Related Topics**: Suggests related Wikipedia articles for further reading
- **Quiz History**: Stores all generated quizzes in PostgreSQL database
- **Caching**: Prevents duplicate scraping of the same URL
- **Clean UI**: Beautiful, responsive interface with tabs for generation and history

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python web framework)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- BeautifulSoup4 (Web scraping)
- LangChain + Google Gemini (LLM integration)

**Frontend:**
- HTML/CSS/JavaScript (Vanilla)
- Modern, responsive design

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your Mac:

1. **Python 3.8+**
   ```bash
   python3 --version
   ```

2. **PostgreSQL**
   ```bash
   # Install using Homebrew
   brew install postgresql@15
   
   # Start PostgreSQL
   brew services start postgresql@15
   ```

3. **VS Code** (or any code editor)
   - Download from: https://code.visualstudio.com/

4. **Google Gemini API Key** (Free)
   - Get from: https://makersuite.google.com/app/apikey
   - Sign in with Google account and create an API key

## 🚀 Installation & Setup

### Step 1: Clone/Download the Project

```bash
# Navigate to your projects folder
cd ~/Documents

# If using git
git clone <your-repo-url>
cd wiki-quiz-app

# OR if you have the zip file
unzip wiki-quiz-app.zip
cd wiki-quiz-app
```

### Step 2: Set Up PostgreSQL Database

```bash
# Start PostgreSQL service (if not already running)
brew services start postgresql@15

# Create database
psql postgres

# In the PostgreSQL prompt:
CREATE DATABASE wiki_quiz_db;
CREATE USER quiz_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE wiki_quiz_db TO quiz_user;
\q

# Test connection
psql -U quiz_user -d wiki_quiz_db -h localhost
# Enter password when prompted, then \q to exit
```

### Step 3: Set Up Backend

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# In the backend folder, copy the example env file
cp .env.example .env

# Edit the .env file
nano .env
# OR
code .env
```

Update the `.env` file with your actual values:

```env
# Database Configuration
DATABASE_URL=postgresql://quiz_user:your_secure_password@localhost:5432/wiki_quiz_db

# Google Gemini API Key
GOOGLE_API_KEY=your_actual_gemini_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**Important:** 
- Replace `your_secure_password` with the password you set in Step 2
- Replace `your_actual_gemini_api_key_here` with your Google Gemini API key

### Step 5: Initialize the Database

```bash
# Still in the backend folder with venv activated
python3 -c "from database import init_db; init_db()"
```

You should see: "Database initialized successfully!"

### Step 6: Start the Backend Server

```bash
# In the backend folder
python3 main.py
```

You should see:
```
╔══════════════════════════════════════════╗
║     Wiki Quiz API Server Starting       ║
╚══════════════════════════════════════════╝

🚀 Server: http://0.0.0.0:8000
📚 Docs: http://0.0.0.0:8000/docs
📖 ReDoc: http://0.0.0.0:8000/redoc
```

**Keep this terminal running!**

### Step 7: Open the Frontend

Open a new terminal window:

```bash
# Navigate to the frontend folder
cd ~/Documents/wiki-quiz-app/frontend

# Open the HTML file directly in your browser
open index.html

# OR serve it with Python's built-in server (recommended)
python3 -m http.server 3000
# Then visit: http://localhost:3000
```

## 🎯 Usage

### Generating a Quiz

1. Open the frontend in your browser (http://localhost:3000 or the direct file)
2. On the "Generate Quiz" tab:
   - Enter a Wikipedia URL (e.g., `https://en.wikipedia.org/wiki/Alan_Turing`)
   - Click "Generate Quiz"
   - Wait 20-30 seconds for the AI to generate the quiz
3. View the generated quiz with:
   - Article summary
   - Key entities (people, organizations, locations)
   - Quiz questions with difficulty levels
   - Related topics for further reading

### Viewing Quiz History

1. Click the "Quiz History" tab
2. See all previously generated quizzes
3. Click "View Details" to see the full quiz in a modal

## 📡 API Endpoints

### 1. Generate Quiz
```http
POST /api/quiz/generate
Content-Type: application/json

{
  "url": "https://en.wikipedia.org/wiki/Alan_Turing"
}
```

### 2. Get Quiz History
```http
GET /api/quiz/history
```

### 3. Get Quiz by ID
```http
GET /api/quiz/{quiz_id}
```

### 4. Delete Quiz (Optional)
```http
DELETE /api/quiz/{quiz_id}
```

## 🧪 Testing

### Test with Sample URLs

Use the URLs provided in `sample_data/test_urls.txt`:

1. **Alan Turing** (Computer Science)
   ```
   https://en.wikipedia.org/wiki/Alan_Turing
   ```

2. **Marie Curie** (Science)
   ```
   https://en.wikipedia.org/wiki/Marie_Curie
   ```

3. **Python Programming** (Technology)
   ```
   https://en.wikipedia.org/wiki/Python_(programming_language)
   ```

### View Sample Output

Check `sample_data/alan_turing_sample.json` for expected output format.

## 📸 Screenshots

After running the application, take screenshots of:

1. **Quiz Generation Page** - After generating a quiz
2. **History View** - The table showing all quizzes
3. **Details Modal** - Clicking "View Details" on a history item

## 🔧 VS Code Setup (Optional but Recommended)

### 1. Open Project in VS Code

```bash
cd ~/Documents/wiki-quiz-app
code .
```

### 2. Install Recommended Extensions

- Python (Microsoft)
- Pylance
- PostgreSQL (Chris Kolkman)
- REST Client (for testing API)

### 3. Set Up Python Interpreter

1. Press `Cmd+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose the one in `backend/venv/bin/python`

### 4. Create Debug Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      }
    }
  ]
}
```

## 🔍 Troubleshooting

### Issue: PostgreSQL won't start

```bash
# Check status
brew services list

# Restart
brew services restart postgresql@15

# Check logs
tail -f /opt/homebrew/var/log/postgresql@15.log
```

### Issue: Module not found errors

```bash
# Make sure virtual environment is activated
source backend/venv/bin/activate

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Issue: Database connection error

```bash
# Test connection
psql -U quiz_user -d wiki_quiz_db -h localhost

# Check your .env file has correct credentials
cat backend/.env
```

### Issue: Gemini API errors

- Verify your API key is correct in `.env`
- Check you haven't exceeded the free tier quota
- Visit: https://makersuite.google.com/app/apikey

### Issue: CORS errors in browser

- Make sure the backend server is running on `http://localhost:8000`
- Check browser console for specific errors
- Ensure CORS middleware is enabled in `main.py`

### Issue: Frontend can't connect to backend

```bash
# Check backend is running
curl http://localhost:8000

# Should return: {"message": "Wiki Quiz API is running!", ...}
```

## 📝 LangChain Prompt Templates

### Quiz Generation Prompt

Located in: `backend/quiz_generator.py` - `_create_quiz_prompt()`

**Key Features:**
- Grounds questions strictly in article content
- Minimizes hallucination by requiring citations
- Requests varying difficulty levels
- Ensures plausible but incorrect options
- Outputs structured JSON

### Related Topics Prompt

Located in: `backend/quiz_generator.py` - `_create_related_topics_prompt()`

**Key Features:**
- Suggests relevant Wikipedia topics
- Covers different aspects (people, events, concepts)
- Encourages diverse recommendations

## 🎨 Bonus Features Implemented

✅ **Caching**: Duplicate URLs are served from database  
✅ **Raw HTML Storage**: Stores original HTML for reference  
✅ **URL Validation**: Validates Wikipedia URLs before processing  
✅ **Error Handling**: Graceful handling of network/scraping errors  
✅ **Responsive UI**: Works on desktop and mobile  
✅ **Loading States**: Clear feedback during quiz generation  

## 📂 Project Structure

```
wiki-quiz-app/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database models & connection
│   ├── scraper.py           # Wikipedia scraping logic
│   ├── quiz_generator.py   # LLM quiz generation
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── .env                 # Your actual config (gitignored)
├── frontend/
│   └── index.html           # Complete frontend UI
├── sample_data/
│   ├── test_urls.txt        # Sample Wikipedia URLs
│   └── alan_turing_sample.json  # Example API output
└── README.md                # This file
```

## 🚦 Quick Start Checklist

- [ ] PostgreSQL installed and running
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database created (`wiki_quiz_db`)
- [ ] `.env` file configured with database credentials and Gemini API key
- [ ] Database initialized (`python3 -c "from database import init_db; init_db()"`)
- [ ] Backend server running (`python3 main.py`)
- [ ] Frontend opened in browser
- [ ] Test quiz generated successfully

## 🤝 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure environment variables are set correctly
4. Check backend logs in the terminal
5. Inspect browser console for frontend errors

## 📄 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Wikipedia for providing free knowledge
- Google Gemini for LLM capabilities
- FastAPI for the excellent web framework
- BeautifulSoup for web scraping
