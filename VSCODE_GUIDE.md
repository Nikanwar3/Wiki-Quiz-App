# 💻 VS Code Setup Guide

Step-by-step instructions to run the Wiki Quiz App in VS Code on Mac.

## Initial Setup

### 1. Open Project in VS Code

```bash
# Navigate to project
cd ~/Downloads/wiki-quiz-app  # or wherever you extracted it

# Open in VS Code
code .
```

### 2. Install Recommended Extensions

Click on Extensions icon (or press `Cmd+Shift+X`) and install:

1. **Python** (by Microsoft) - Essential for Python development
2. **Pylance** - Python language server
3. **PostgreSQL** (by Chris Kolkman) - For database management
4. **Thunder Client** - For testing API endpoints (optional)

### 3. Configure Python Interpreter

1. Open Command Palette: `Cmd+Shift+P`
2. Type: `Python: Select Interpreter`
3. If virtual environment exists: Choose `./backend/venv/bin/python`
4. If not, we'll create it in the next step

## Backend Setup in VS Code

### 1. Open Integrated Terminal

- Press `Ctrl+` (backtick) OR
- Menu: Terminal → New Terminal

### 2. Navigate to Backend

```bash
cd backend
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
```

### 4. Activate Virtual Environment

```bash
source venv/bin/activate
```

Your terminal prompt should now show `(venv)` at the beginning.

### 5. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will take 1-2 minutes. You'll see packages being installed.

### 6. Configure Environment Variables

1. In VS Code Explorer, find `backend/.env.example`
2. Right-click → Duplicate
3. Rename the copy to `.env`
4. Click on `.env` to open it
5. Update with your values:

```env
DATABASE_URL=postgresql://quiz_user:yourpassword@localhost:5432/wiki_quiz_db
GOOGLE_API_KEY=your_actual_gemini_api_key
HOST=0.0.0.0
PORT=8000
```

**Getting Gemini API Key:**
- Visit: https://makersuite.google.com/app/apikey
- Sign in with Google
- Click "Create API Key"
- Copy and paste into `.env`

### 7. Initialize Database

In the terminal (make sure you're in `backend` folder with venv activated):

```bash
python3 -c "from database import init_db; init_db()"
```

You should see: "Database initialized successfully!"

## Running the Application

### Option 1: Using VS Code Terminal (Recommended for Beginners)

#### Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
python3 main.py
```

Keep this running! You should see:
```
🚀 Server: http://0.0.0.0:8000
📚 Docs: http://0.0.0.0:8000/docs
```

#### Terminal 2 - Frontend:
1. Click the `+` icon in terminal to open a new terminal
2. Run:
```bash
cd frontend
python3 -m http.server 3000
```

Keep this running too!

#### Open Browser:
- Visit: http://localhost:3000

### Option 2: Using VS Code Debug Configuration (Advanced)

1. Create `.vscode` folder in project root (if it doesn't exist)
2. Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI Backend",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      },
      "console": "integratedTerminal"
    }
  ]
}
```

3. Press `F5` or click Run → Start Debugging
4. In separate terminal, run frontend:
```bash
cd frontend && python3 -m http.server 3000
```

## Testing the API

### Using VS Code REST Client

1. Install "Thunder Client" extension
2. Create new request:
   - Method: POST
   - URL: http://localhost:8000/api/quiz/generate
   - Body (JSON):
```json
{
  "url": "https://en.wikipedia.org/wiki/Alan_Turing"
}
```
3. Click "Send"

### Using Built-in API Documentation

Visit: http://localhost:8000/docs

This opens FastAPI's interactive API documentation where you can test all endpoints.

## Useful VS Code Features

### 1. Integrated Terminal Management

- **New Terminal**: `Ctrl+Shift+` (backtick)
- **Split Terminal**: Click split icon in terminal
- **Kill Terminal**: Click trash icon
- **Switch Terminals**: Use dropdown menu

### 2. File Navigation

- **Quick Open File**: `Cmd+P`
- **Go to Symbol**: `Cmd+Shift+O`
- **Search in Files**: `Cmd+Shift+F`

### 3. Code Editing

- **Format Document**: `Shift+Option+F`
- **Go to Definition**: `F12`
- **Find All References**: `Shift+F12`

### 4. Debugging

- **Toggle Breakpoint**: `F9`
- **Start Debugging**: `F5`
- **Step Over**: `F10`
- **Step Into**: `F11`

## Project Structure in VS Code

```
wiki-quiz-app/
├── .vscode/              # VS Code settings (create this)
│   └── launch.json       # Debug configuration
├── backend/
│   ├── venv/            # Virtual environment (created)
│   ├── .env             # Your secrets (create from .env.example)
│   ├── main.py          # Main API file
│   ├── database.py      # Database models
│   ├── scraper.py       # Wikipedia scraper
│   ├── quiz_generator.py # LLM quiz generation
│   └── requirements.txt # Python packages
├── frontend/
│   └── index.html       # Frontend UI
├── sample_data/
│   ├── test_urls.txt    # Sample URLs
│   └── alan_turing_sample.json
└── README.md
```

## Common VS Code Tasks

### View Database in VS Code

1. Install PostgreSQL extension
2. Click PostgreSQL icon in sidebar
3. Add connection:
   - Host: localhost
   - Port: 5432
   - Database: wiki_quiz_db
   - Username: quiz_user
   - Password: (your password)
4. Browse tables and data

### Format Python Code

1. Install Python extension
2. Open any `.py` file
3. Press `Shift+Option+F`
4. Code will auto-format

### View API Logs

When backend is running, all logs appear in the integrated terminal.
Look for:
- Request logs
- Error messages
- Database queries

## Troubleshooting in VS Code

### Python Interpreter Not Found

1. `Cmd+Shift+P`
2. Type: `Python: Select Interpreter`
3. Choose `backend/venv/bin/python`
4. If not listed, reload VS Code

### Import Errors (Red Squiggles)

1. Make sure correct Python interpreter is selected
2. Check that venv is activated in terminal
3. Try: `Cmd+Shift+P` → `Python: Restart Language Server`

### Environment Variables Not Loading

1. Verify `.env` file exists in `backend/` folder
2. Check no extra spaces in variable names
3. Restart the backend server

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use a different port in .env
PORT=8001
```

## Keyboard Shortcuts Cheat Sheet

| Action | Shortcut |
|--------|----------|
| Command Palette | `Cmd+Shift+P` |
| Quick Open File | `Cmd+P` |
| Toggle Terminal | `Ctrl+` ` |
| New Terminal | `Ctrl+Shift+` ` |
| Split Editor | `Cmd+\` |
| Toggle Sidebar | `Cmd+B` |
| Search Files | `Cmd+Shift+F` |
| Format Document | `Shift+Option+F` |
| Save All | `Cmd+Option+S` |
| Close Editor | `Cmd+W` |

## Next Steps

1. ✅ Backend running on http://localhost:8000
2. ✅ Frontend running on http://localhost:3000
3. ✅ Test with sample URLs
4. ✅ Check API docs at http://localhost:8000/docs
5. ✅ Modify code and see changes (auto-reload enabled)

## Tips for Development

1. **Keep terminals organized**: 
   - Terminal 1: Backend (stays running)
   - Terminal 2: Frontend (stays running)
   - Terminal 3: Database commands, testing, etc.

2. **Use breakpoints**: 
   - Click left of line numbers to add breakpoint
   - Run in debug mode to inspect variables

3. **Check logs**: 
   - Backend logs show all requests
   - Browser console (F12) shows frontend errors

4. **Test frequently**: 
   - Use API docs to test endpoints
   - Check database with PostgreSQL extension

---

**You're all set! Happy coding! 🚀**
