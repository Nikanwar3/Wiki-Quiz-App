#!/bin/bash

# Wiki Quiz App - Mac Setup Script
# This script automates the setup process on macOS

set -e  # Exit on error

echo "╔══════════════════════════════════════════╗"
echo "║   Wiki Quiz App - Setup Script          ║"
echo "║   For macOS                              ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS only!"
    exit 1
fi

print_success "Running on macOS"

# Check Python installation
print_info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is not installed!"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

# Check PostgreSQL installation
print_info "Checking PostgreSQL installation..."
if command -v psql &> /dev/null; then
    PG_VERSION=$(psql --version | cut -d ' ' -f 3)
    print_success "PostgreSQL $PG_VERSION found"
else
    print_error "PostgreSQL is not installed!"
    echo "Installing PostgreSQL via Homebrew..."
    
    if command -v brew &> /dev/null; then
        brew install postgresql@15
        brew services start postgresql@15
        print_success "PostgreSQL installed and started"
    else
        print_error "Homebrew not found!"
        echo "Please install Homebrew from https://brew.sh/"
        echo "Then run: brew install postgresql@15"
        exit 1
    fi
fi

# Get project directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"

echo ""
print_info "Project directory: $PROJECT_DIR"
echo ""

# Database setup
print_info "Setting up database..."
read -p "Enter database name (default: wiki_quiz_db): " DB_NAME
DB_NAME=${DB_NAME:-wiki_quiz_db}

read -p "Enter database user (default: quiz_user): " DB_USER
DB_USER=${DB_USER:-quiz_user}

read -sp "Enter database password: " DB_PASSWORD
echo ""

# Create database
print_info "Creating PostgreSQL database..."
psql postgres -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || print_info "Database may already exist"
psql postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || print_info "User may already exist"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
print_success "Database configured"

# Get Gemini API key
echo ""
print_info "You need a Google Gemini API key (free)"
echo "Get one from: https://makersuite.google.com/app/apikey"
read -p "Enter your Gemini API key: " GEMINI_KEY

# Create virtual environment
print_info "Creating Python virtual environment..."
cd "$BACKEND_DIR"
python3 -m venv venv
print_success "Virtual environment created"

# Activate virtual environment and install dependencies
print_info "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
print_success "Dependencies installed"

# Create .env file
print_info "Creating .env file..."
cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME

# Google Gemini API Key
GOOGLE_API_KEY=$GEMINI_KEY

# Server Configuration
HOST=0.0.0.0
PORT=8000
EOF
print_success ".env file created"

# Initialize database
print_info "Initializing database tables..."
python3 -c "from database import init_db; init_db()"
print_success "Database initialized"

# Create launch scripts
print_info "Creating launch scripts..."

# Backend launcher
cat > "$PROJECT_DIR/start_backend.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/backend"
source venv/bin/activate
python3 main.py
EOF
chmod +x "$PROJECT_DIR/start_backend.sh"

# Frontend launcher
cat > "$PROJECT_DIR/start_frontend.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/frontend"
python3 -m http.server 3000
EOF
chmod +x "$PROJECT_DIR/start_frontend.sh"

# Combined launcher
cat > "$PROJECT_DIR/start_all.sh" << 'EOF'
#!/bin/bash
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Starting Wiki Quiz App..."
echo ""

# Start backend in background
echo "Starting backend server..."
cd "$PROJECT_DIR/backend"
source venv/bin/activate
python3 main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend server..."
cd "$PROJECT_DIR/frontend"
python3 -m http.server 3000 &
FRONTEND_PID=$!

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║     Wiki Quiz App is Running!            ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF
chmod +x "$PROJECT_DIR/start_all.sh"

print_success "Launch scripts created"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║     Setup Complete! 🎉                   ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "To start the application:"
echo ""
echo "Option 1 - Start everything at once:"
echo "  ./start_all.sh"
echo ""
echo "Option 2 - Start separately:"
echo "  Terminal 1: ./start_backend.sh"
echo "  Terminal 2: ./start_frontend.sh"
echo ""
echo "Then open: http://localhost:3000"
echo ""
print_success "Setup completed successfully!"
