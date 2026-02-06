# 🎯 GETTING STARTED - Wiki Quiz App

Welcome! This is your complete guide to setting up and running the Wiki Quiz App on your Mac.

## 📦 What You Have

A complete, production-ready web application that:
- Scrapes Wikipedia articles
- Generates AI-powered quizzes using Google Gemini
- Stores everything in PostgreSQL
- Beautiful, responsive web interface
- Complete history tracking

## 🚀 Three Ways to Get Started

### 1️⃣ SUPER QUICK START (5 minutes)

**For users who already have Python and PostgreSQL installed:**

```bash
# 1. Extract the zip and navigate to it
cd /path/to/wiki-quiz-app

# 2. Run the automated setup
chmod +x setup_mac.sh
./setup_mac.sh

# 3. Start everything
./start_all.sh

# 4. Open browser to http://localhost:3000
```

That's it! 🎉

### 2️⃣ BEGINNER-FRIENDLY START (15 minutes)

**For users new to development:**

Follow the **QUICKSTART.md** guide which includes:
- Installing prerequisites
- Step-by-step terminal commands
- Explanations for each step
- Troubleshooting tips

### 3️⃣ VS CODE START (20 minutes)

**For users who want to use VS Code:**

Follow the **VSCODE_GUIDE.md** which includes:
- VS Code setup
- Debugging configuration
- Extension recommendations
- Keyboard shortcuts

## 📋 What You Need

Before starting, make sure you have:

1. **macOS** (this is Mac-specific)
2. **Python 3.8+** (check: `python3 --version`)
3. **PostgreSQL 12+** (check: `psql --version`)
4. **Google Gemini API Key** (free from https://makersuite.google.com/app/apikey)

Don't have these? See the installation section in README.md

## 📁 Project Structure

```
wiki-quiz-app/
├── 📖 README.md              # Complete documentation
├── ⚡ QUICKSTART.md          # Quick start guide
├── 💻 VSCODE_GUIDE.md        # VS Code specific guide
├── 🔧 setup_mac.sh           # Automated setup script
├── 🚀 start_all.sh           # Start backend + frontend
│
├── backend/                  # Python FastAPI application
│   ├── main.py              # API endpoints
│   ├── database.py          # Database models
│   ├── scraper.py           # Wikipedia scraper
│   ├── quiz_generator.py   # LLM quiz generation
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment template
│
├── frontend/                 # Web interface
│   └── index.html           # Complete UI (no build needed!)
│
└── sample_data/             # Test data
    ├── test_urls.txt        # Sample Wikipedia URLs
    └── alan_turing_sample.json  # Example output
```

## ⚙️ Quick Setup (Manual Way)

If automated setup doesn't work, here's the manual process:

### Step 1: Install PostgreSQL
```bash
brew install postgresql@15
brew services start postgresql@15
```

### Step 2: Create Database
```bash
psql postgres
```
In PostgreSQL prompt:
```sql
CREATE DATABASE wiki_quiz_db;
CREATE USER quiz_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE wiki_quiz_db TO quiz_user;
\q
```

### Step 3: Setup Python Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

Add:
```env
DATABASE_URL=postgresql://quiz_user:yourpassword@localhost:5432/wiki_quiz_db
GOOGLE_API_KEY=your_gemini_key_here
```

### Step 5: Initialize Database
```bash
python3 -c "from database import init_db; init_db()"
```

### Step 6: Run Application
Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate
python3 main.py
```

Terminal 2 (Frontend):
```bash
cd frontend
python3 -m http.server 3000
```

Browser:
```
http://localhost:3000
```

## ✅ Verify It's Working

1. Backend check:
   ```bash
   curl http://localhost:8000
   ```
   Should return JSON with "Wiki Quiz API is running!"

2. Frontend check:
   - Open http://localhost:3000
   - Should see "Wiki Quiz Generator" interface

3. Generate a quiz:
   - Use the pre-filled Alan Turing URL
   - Click "Generate Quiz"
   - Wait 20-30 seconds
   - Should see quiz questions!

## 🎓 First Time Using It?

1. **Generate Your First Quiz**:
   - URL is pre-filled with Alan Turing
   - Just click "Generate Quiz"
   - Wait for AI to work its magic
   - Explore the results!

2. **Try More Topics**:
   - Check `sample_data/test_urls.txt` for ideas
   - Try: Marie Curie, Python programming, Paris, etc.

3. **View History**:
   - Click "Quiz History" tab
   - See all your generated quizzes
   - Click "View Details" to review

## 🐛 Something Not Working?

### Quick Fixes:

**PostgreSQL not starting:**
```bash
brew services restart postgresql@15
```

**Python errors:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Port already in use:**
```bash
# For port 8000
lsof -i :8000
kill -9 <PID>

# For port 3000
lsof -i :3000
kill -9 <PID>
```

**Gemini API errors:**
- Check your API key at https://makersuite.google.com/app/apikey
- Verify it's correctly in `.env`
- Check you haven't exceeded free tier

### Still stuck?
Check the full troubleshooting section in README.md

## 📚 Where to Learn More

| Document | What's Inside |
|----------|---------------|
| **README.md** | Complete documentation, API endpoints, architecture |
| **QUICKSTART.md** | Step-by-step beginner guide |
| **VSCODE_GUIDE.md** | VS Code setup and debugging |
| **sample_data/** | Test URLs and example outputs |

## 🎯 What to Do Next

Once you have it running:

1. ✅ Generate quizzes from different Wikipedia topics
2. ✅ Explore the API at http://localhost:8000/docs
3. ✅ Customize the quiz generation (edit `quiz_generator.py`)
4. ✅ Modify the UI (edit `frontend/index.html`)
5. ✅ Add more features (see "Bonus Points" in requirements)

## 💡 Pro Tips

- **Use the API docs**: http://localhost:8000/docs shows all endpoints and lets you test them
- **Check logs**: Backend terminal shows all requests and errors
- **Browser console**: Press F12 to see frontend errors
- **Database viewer**: Use a tool like Postico or DBeaver to view stored data
- **VS Code**: Best experience for development and debugging

## 📞 Need Help?

1. Check README.md troubleshooting section
2. Look at browser console (F12)
3. Check backend terminal logs
4. Verify all environment variables are set
5. Make sure PostgreSQL is running: `brew services list`

## 🎉 You're Ready!

Pick one of the three getting started methods above and you'll be generating AI-powered quizzes in minutes!

**Recommended path:**
- Complete beginners → QUICKSTART.md
- Developers → VSCODE_GUIDE.md  
- Quick setup → Run setup_mac.sh

---

**Happy learning! 📚✨**
