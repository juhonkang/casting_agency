#!/bin/bash

echo "=========================================="
echo "🧪 LOCAL TESTING SCRIPT"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check if virtual environment exists
echo "📋 Step 1: Checking virtual environment..."
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ Virtual environment found${NC}"
else
    echo -e "${YELLOW}⚠ Creating virtual environment...${NC}"
    python -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Step 2: Activate virtual environment
echo ""
echo "📋 Step 2: Activating virtual environment..."
source venv/Scripts/activate || source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo "   Python: $(which python)"
echo "   Version: $(python --version)"

# Step 3: Install/Upgrade dependencies
echo ""
echo "📋 Step 3: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

# Step 4: Check environment variables
echo ""
echo "📋 Step 4: Checking environment variables..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env file found${NC}"
    source .env
else
    echo -e "${YELLOW}⚠ .env file not found${NC}"
    echo "   Using setup.sh instead..."
    if [ -f "setup.sh" ]; then
        source setup.sh
        echo -e "${GREEN}✓ setup.sh loaded${NC}"
    else
        echo -e "${RED}✗ No environment configuration found${NC}"
        echo "   Please create .env or setup.sh"
        exit 1
    fi
fi

# Step 5: Check database connection
echo ""
echo "📋 Step 5: Testing database connection..."
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv('database_username')
db_pass = os.getenv('database_password')
db_name = os.getenv('database_name')

if db_user and db_pass and db_name:
    print('✓ Database credentials found')
    print(f'  User: {db_user}')
    print(f'  Database: {db_name}')
else:
    print('✗ Database credentials missing')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Database configuration incomplete${NC}"
    exit 1
fi

# Step 6: Test Python imports
echo ""
echo "📋 Step 6: Testing Python imports..."
python -c "
try:
    import flask
    print(f'✓ Flask {flask.__version__}')

    import sqlalchemy
    print(f'✓ SQLAlchemy {sqlalchemy.__version__}')

    import flask_sqlalchemy
    print(f'✓ Flask-SQLAlchemy {flask_sqlalchemy.__version__}')

    import gunicorn
    print(f'✓ Gunicorn {gunicorn.__version__}')

    from jose import jwt
    print('✓ python-jose')

    import flask_limiter
    print('✓ Flask-Limiter')

    print('\n✓ All imports successful!')
except ImportError as e:
    print(f'✗ Import error: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Import test failed${NC}"
    exit 1
fi

# Step 7: Test models import
echo ""
echo "📋 Step 7: Testing models import..."
python -c "
import sys
sys.path.insert(0, '.')
try:
    from models import setup_db, Question, Category
    print('✓ Models imported successfully')
except Exception as e:
    print(f'✗ Model import error: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Models test failed${NC}"
    exit 1
fi

# Step 8: Test auth import
echo ""
echo "📋 Step 8: Testing auth import..."
python -c "
import sys
sys.path.insert(0, '.')
try:
    from auth import AuthError, requires_auth
    print('✓ Auth module imported successfully')
except Exception as e:
    print(f'✗ Auth import error: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Auth test failed${NC}"
    exit 1
fi

# Step 9: Test Flask app creation
echo ""
echo "📋 Step 9: Testing Flask app creation..."
python -c "
import sys
sys.path.insert(0, '.')
try:
    from flaskr import create_app
    app = create_app()
    print('✓ Flask app created successfully')
    print(f'  App name: {app.name}')
except Exception as e:
    print(f'✗ App creation error: {e}')
    import traceback
    traceback.print_exc()
    exit(1)
"

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Flask app creation failed${NC}"
    exit 1
fi

# Step 10: Run unit tests
echo ""
echo "📋 Step 10: Running unit tests..."
echo -e "${YELLOW}Running test_flaskr.py...${NC}"
python test_flaskr.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Unit tests passed${NC}"
else
    echo -e "${RED}✗ Unit tests failed${NC}"
    exit 1
fi

# Step 11: Summary
echo ""
echo "=========================================="
echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
echo "=========================================="
echo ""
echo "🚀 You can now start the server with:"
echo "   flask run --reload"
echo ""
echo "Or run with gunicorn:"
echo "   gunicorn 'flaskr:create_app()'"
echo ""
echo "=========================================="
