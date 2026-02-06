# 🚀 Quick Start Guide (macOS)

This guide will help you get the Wiki Quiz App running on your Mac in under 10 minutes!

## Prerequisites Check

Open Terminal and run these commands to check what you need:

```bash
# Check Python (need 3.8+)
python3 --version

# Check PostgreSQL (need 12+)
psql --version

# Check Homebrew (package manager)
brew --version
```

## Installation Steps

### Option 1: Automated Setup (Recommended) ⚡

```bash
# 1. Open Terminal and navigate to the project
cd /path/to/wiki-quiz-app

# 2. Run the setup script
./setup_mac.sh

# 3. Follow the prompts:
#    - Database name (press Enter for default)
#    - Database user (press Enter for default)
#    - Database password (choose a secure password)
#    - Gemini API key (get from https://makersuite.google.com/app/apikey)

# 4. Start the app
./start_all.sh

# 5. Open browser to http://localhost:3000
```

### Option 2: Manual Setup 🔧

#### Step 1: Install PostgreSQL (if not installed)
```bash
brew install postgresql@15
brew services start postgresql@15
```

#### Step 2: Create Database
```bash
# Open PostgreSQL prompt
psql postgres

# Create database and user (in psql prompt)
CREATE DATABASE wiki_quiz_db;
CREATE USER quiz_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE wiki_quiz_db TO quiz_user;
\q
```

#### Step 3: Setup Backend
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Update `.env`:
```env
DATABASE_URL=postgresql://quiz_user:yourpassword@localhost:5432/wiki_quiz_db
GOOGLE_API_KEY=your_gemini_api_key_here
HOST=0.0.0.0
PORT=8000
```

#### Step 4: Initialize Database
```bash
# Still in backend folder with venv activated
python3 -c "from database import init_db; init_db()"
```

#### Step 5: Start Backend
```bash
python3 main.py
```

Keep this terminal open!

#### Step 6: Start Frontend
Open a new terminal:
```bash
cd frontend
python3 -m http.server 3000
```

#### Step 7: Open Browser
```
http://localhost:3000
```

## Testing the App

1. **Try the default URL** (Alan Turing)
   - The input field is pre-filled
   - Click "Generate Quiz"
   - Wait 20-30 seconds
   - View the generated quiz!

2. **Try more URLs** from `sample_data/test_urls.txt`

3. **Check History**
   - Click "Quiz History" tab
   - View all generated quizzes
   - Click "View Details" to see a quiz

## Troubleshooting

### PostgreSQL won't start
```bash
brew services restart postgresql@15
```

### Python module errors
```bash
# Make sure venv is activated
source backend/venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

### Can't connect to backend
```bash
# Test if backend is running
curl http://localhost:8000

# Should see: {"message": "Wiki Quiz API is running!", ...}
```

### Gemini API errors
- Check your API key in `.env`
- Verify at: https://makersuite.google.com/app/apikey
- Ensure you're within free tier limits

## VS Code Setup (Optional)

```bash
# Open in VS Code
code .

# Then:
# 1. Install Python extension
# 2. Cmd+Shift+P → "Python: Select Interpreter"
# 3. Choose backend/venv/bin/python
```

## Stopping the App

```bash
# Press Ctrl+C in both terminal windows
# OR if using start_all.sh, just Ctrl+C once
```

## Next Steps

- Check out the full README.md for detailed documentation
- Explore the API at http://localhost:8000/docs
- Modify quiz generation parameters in `backend/quiz_generator.py`
- Customize the UI in `frontend/index.html`

## Common Issues

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | Change PORT in .env or kill the process |
| Port 3000 already in use | Use different port: `python3 -m http.server 8080` |
| Database connection failed | Check PostgreSQL is running: `brew services list` |
| CORS errors | Ensure backend is on localhost:8000 |
| No questions generated | Check Gemini API key and quota |

## Need Help?

1. Check the Troubleshooting section in README.md
2. Look at backend logs in the terminal
3. Check browser console (F12) for frontend errors
4. Verify all environment variables are set correctly

---

**Happy Quiz Generating! 📚✨**
