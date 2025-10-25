# Trivia API - Casting Agency Project

A full-stack trivia application that allows users to play quiz games, manage questions and categories. This project demonstrates modern web development practices with Flask backend and React frontend, featuring comprehensive API documentation, security features, and robust testing.

## 🌐 Live Deployment

**API Base URL:** https://trivia-api.onrender.com

**Status:** ✅ Live and Running

**Test the API:**
```bash
# Note: Protected endpoints require authentication
curl https://trivia-api.onrender.com/questions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Authentication & RBAC](#authentication--rbac)
  - [User Roles](#user-roles)
  - [Setup Auth0](#setup-auth0)
  - [Getting JWT Tokens](#getting-jwt-tokens)
- [API Documentation](#api-documentation)
- [Security Features](#security-features)
- [Testing](#testing)
- [Database Migrations](#database-migrations)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Functionality
- Browse and search trivia questions across multiple categories
- Add new questions with custom difficulty levels
- Delete existing questions
- Play quiz games by category or across all categories
- Paginated question listing (10 questions per page)
- Real-time search functionality

### Enhanced Features
- **Auth0 Authentication**: Industry-standard JWT token-based authentication
- **Role-Based Access Control (RBAC)**: Two-tier permission system (User/Manager)
- **Input Validation**: Comprehensive validation for all user inputs
- **Rate Limiting**: API rate limiting to prevent abuse (200 requests/day, 50 requests/hour per endpoint)
- **Logging System**: Detailed logging for debugging and monitoring
- **Error Handling**: Robust error handling with informative error messages
- **Database Constraints**: Data integrity with check constraints and validations
- **Security**: Input sanitization and protection against common vulnerabilities
- **Database Connection Pooling**: Optimized database connections with automatic ping and recycling
- **Production-Ready Deployment**: Configured for Heroku and Render with one-click deploy

## Technology Stack

### Backend
- **Flask 2.3.3** - Lightweight WSGI web application framework
- **SQLAlchemy 2.0.21** - SQL toolkit and ORM
- **Flask-SQLAlchemy 3.0.5** - Flask extension for SQLAlchemy
- **Flask-Migrate 4.0.5** - Database migration handling
- **Flask-CORS 4.0.0** - Cross-Origin Resource Sharing support
- **Flask-Limiter 3.5.0** - Rate limiting extension
- **Auth0 & python-jose 3.3.0** - JWT authentication and RBAC
- **PostgreSQL** - Relational database
- **Gunicorn 21.2.0** - Production WSGI server
- **Python 3.11+** - Programming language

### Frontend
- **React** - JavaScript library for building user interfaces
- **Node.js & npm** - JavaScript runtime and package manager

## Project Structure

```
casting_agency/
├── backend/
│   ├── flaskr/
│   │   └── __init__.py          # Main application file with routes
│   ├── models.py                 # Database models
│   ├── test_flaskr.py           # Unit tests
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example             # Environment variables template
│   ├── .gitignore               # Git ignore file
│   └── README.md                # Backend documentation
├── frontend/
│   ├── src/                     # React source files
│   ├── public/                  # Static files
│   ├── package.json             # Node dependencies
│   └── README.md                # Frontend documentation
└── README.md                    # This file
```

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Node.js 14 or higher
- PostgreSQL 12 or higher
- pip (Python package installer)
- npm (Node package manager)

### Backend Setup

#### 1. Navigate to the backend directory
```bash
cd backend
```

#### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set up environment variables
Create a `.env` file in the backend directory:
```bash
cp .env.example .env
```

Edit `.env` with your database credentials:
```
database_username=your_username
database_password=your_password
database_name=trivia

test_database_username=your_username
test_database_password=your_password
test_database_name=trivia_test
```

#### 5. Create databases
```bash
# Create production database
createdb trivia

# Create test database
createdb trivia_test
```

#### 6. Populate the database
```bash
psql trivia < trivia.psql
psql trivia_test < trivia.psql
```

#### 7. Run database migrations (optional)
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### 8. Run the development server
```bash
# Set environment variables
export FLASK_APP=flaskr
export FLASK_ENV=development

# Run the server
flask run --reload
```

The API will be available at `http://localhost:5000`

### Frontend Setup

#### 1. Navigate to the frontend directory
```bash
cd frontend
```

#### 2. Install dependencies
```bash
npm install
```

#### 3. Start the development server
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Authentication & RBAC

This API uses Auth0 for authentication and implements Role-Based Access Control (RBAC) with JWT tokens.

### User Roles

The application defines two roles with different permission levels:

| Role | Permissions | Description |
|------|-------------|-------------|
| **Trivia User** | `get:questions`<br>`get:categories` | Basic users who can view questions and categories |
| **Trivia Manager** | `get:questions`<br>`get:categories`<br>`post:questions`<br>`delete:questions` | Managers with full CRUD access to questions |

### Permissions Breakdown

- **get:questions** - Retrieve and view trivia questions
- **get:categories** - Retrieve and view question categories
- **post:questions** - Create new trivia questions
- **delete:questions** - Delete existing trivia questions

### Setup Auth0

Follow these steps to configure Auth0 authentication:

1. **Complete Auth0 Setup**

   Follow the detailed guide in [AUTH0_SETUP.md](AUTH0_SETUP.md) which covers:
   - Creating an Auth0 account
   - Setting up the API and permissions
   - Creating roles and test users
   - Generating JWT tokens for testing

2. **Configure Environment Variables**

   Edit `backend/setup.sh` with your Auth0 credentials:
   ```bash
   export AUTH0_DOMAIN='your-tenant.us.auth0.com'
   export ALGORITHMS='["RS256"]'
   export API_AUDIENCE='trivia-api'
   export TRIVIA_USER_TOKEN='your-test-token-here'
   export TRIVIA_MANAGER_TOKEN='your-test-token-here'
   ```

3. **Load Environment Variables**
   ```bash
   cd backend
   source setup.sh
   ```

### Getting JWT Tokens

#### Method 1: Auth0 Dashboard (Quick)

1. Go to Auth0 Dashboard → APIs → Trivia API → Test tab
2. Copy the access token
3. Note: This token will have ALL permissions

#### Method 2: Authentication Flow (Role-Specific)

1. Create a test application in Auth0
2. Use the authorization URL:
   ```
   https://YOUR_DOMAIN/authorize?
     audience=trivia-api&
     response_type=token&
     client_id=YOUR_CLIENT_ID&
     redirect_uri=https://jwt.io
   ```
3. Login with your test user credentials
4. Copy the token from the redirect URL

See [AUTH0_SETUP.md](AUTH0_SETUP.md) for detailed instructions.

### Using Authentication in API Requests

All protected endpoints require a valid JWT token in the Authorization header:

```bash
curl http://localhost:5000/questions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Testing RBAC

Run the RBAC test suite to verify authentication and permissions:

```bash
cd backend
source setup.sh
python test_rbac.py
```

The test suite includes:
- Authentication requirement tests (no token = 401)
- Permission tests for Trivia User role
- Permission tests for Trivia Manager role
- Invalid token handling

## API Documentation

### Base URL
- Development: `http://localhost:5000`
- All responses are in JSON format

### Error Handling

The API returns standard HTTP status codes and JSON error responses:

```json
{
  "success": false,
  "error": 404,
  "message": "Resource Not Found"
}
```

#### Error Codes
- `400` - Bad Request (Invalid input)
- `404` - Resource Not Found
- `405` - Method Not Allowed
- `422` - Unprocessable Entity
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error

### Endpoints

#### GET /categories
Fetches all available categories.

**Authentication:** Required (`get:categories` permission)

**Rate Limit:** 100 requests per hour

**Request:**
```bash
curl http://localhost:5000/categories \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### GET /questions
Fetches paginated questions (10 per page).

**Authentication:** Required (`get:questions` permission)

**Rate Limit:** 100 requests per hour

**Query Parameters:**
- `page` (optional): Page number (default: 1)

**Request:**
```bash
curl http://localhost:5000/questions?page=1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": "3",
      "difficulty": 2
    }
  ],
  "total_questions": 50,
  "categories": {
    "1": "Science",
    "2": "Art"
  },
  "current_category": null
}
```

#### DELETE /questions/<question_id>
Deletes a question by ID.

**Authentication:** Required (`delete:questions` permission - Manager only)

**Rate Limit:** 50 requests per hour

**Request:**
```bash
curl -X DELETE http://localhost:5000/questions/5 \
  -H "Authorization: Bearer YOUR_MANAGER_TOKEN"
```

**Response:**
```json
{
  "success": true,
  "deleted": "5",
  "questions": [...],
  "total_questions": 49
}
```

#### POST /questions
Creates a new question.

**Authentication:** Required (`post:questions` permission - Manager only)

**Rate Limit:** 50 requests per hour

**Request Body:**
```json
{
  "question": "What is Python?",
  "answer": "A programming language",
  "category": "1",
  "difficulty": 2
}
```

**Validation Rules:**
- `question`: Required, non-empty string (max 500 chars)
- `answer`: Required, non-empty string (max 500 chars)
- `category`: Required, must be a valid category ID
- `difficulty`: Required, integer between 1-5

**Request:**
```bash
curl -X POST http://localhost:5000/questions \
  -H "Authorization: Bearer YOUR_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Python?","answer":"A programming language","category":"1","difficulty":2}'
```

**Response:**
```json
{
  "success": true,
  "created": 51
}
```

#### POST /questions/search
Searches for questions containing the search term.

**Rate Limit:** 100 requests per hour

**Request Body:**
```json
{
  "searchTerm": "title"
}
```

**Request:**
```bash
curl -X POST http://localhost:5000/questions/search \
  -H "Content-Type: application/json" \
  -d '{"searchTerm":"title"}'
```

**Response:**
```json
{
  "success": true,
  "questions": [
    {
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2
    }
  ],
  "total_questions": 1,
  "current_category": null
}
```

#### GET /categories/<category_id>/questions
Fetches questions for a specific category.

**Rate Limit:** 100 requests per hour

**Request:**
```bash
curl http://localhost:5000/categories/1/questions
```

**Response:**
```json
{
  "success": true,
  "questions": [...],
  "total_questions": 10,
  "current_category": 1
}
```

#### POST /quizzes
Gets a random question for the quiz game.

**Rate Limit:** 100 requests per hour

**Request Body:**
```json
{
  "previous_questions": [1, 2, 3],
  "quiz_category": {
    "id": "1",
    "type": "Science"
  }
}
```

**Notes:**
- `previous_questions`: Array of question IDs already asked
- `quiz_category.id`: Use `0` for all categories, or specific category ID
- Returns `null` when no more questions available

**Request:**
```bash
curl -X POST http://localhost:5000/quizzes \
  -H "Content-Type: application/json" \
  -d '{"previous_questions":[],"quiz_category":{"id":"1","type":"Science"}}'
```

**Response:**
```json
{
  "success": true,
  "question": {
    "id": 20,
    "question": "What is the heaviest organ in the human body?",
    "answer": "The Liver",
    "category": "1",
    "difficulty": 4
  }
}
```

## Security Features

### Input Validation
- All user inputs are validated before processing
- String inputs are sanitized and trimmed
- Numeric inputs are type-checked and range-validated
- Foreign key constraints verified before operations

### Rate Limiting
- Default: 200 requests/day, 50 requests/hour per IP
- Read endpoints: 100 requests/hour
- Write endpoints: 50 requests/hour
- Rate limit headers included in responses

### Database Security
- Parameterized queries prevent SQL injection
- Database constraints enforce data integrity
- Connection pooling with automatic health checks
- Prepared statements for all queries

### Error Handling
- Detailed logging for administrators
- Generic error messages for clients
- No sensitive information in error responses
- Exception handling at all levels

## Testing

### Run all tests
```bash
cd backend
python test_flaskr.py
```

### Test Coverage
The test suite includes:
- ✅ Category retrieval (success & failure)
- ✅ Question listing with pagination
- ✅ Question creation with validation
- ✅ Question deletion
- ✅ Question search
- ✅ Category-filtered questions
- ✅ Quiz game functionality
- ✅ Error handling for all endpoints

### Reset test database
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Database Migrations

This project uses Flask-Migrate for database version control.

### Initialize migrations (first time only)
```bash
flask db init
```

### Create a migration
```bash
flask db migrate -m "Description of changes"
```

### Apply migrations
```bash
flask db upgrade
```

### Rollback migration
```bash
flask db downgrade
```

## Deployment

### Environment Configuration
1. Set `FLASK_ENV=production`
2. Use environment variables for sensitive data
3. Configure production database credentials
4. Set up a proper WSGI server (e.g., Gunicorn)

### Production Checklist
- [ ] Set strong SECRET_KEY
- [ ] Configure CORS for specific origins
- [ ] Set up SSL/TLS certificates
- [ ] Configure database backups
- [ ] Set up monitoring and logging
- [ ] Use Redis for rate limiting storage
- [ ] Configure reverse proxy (nginx/Apache)

### Example Production Server
```bash
pip install gunicorn
gunicorn -b 0.0.0.0:5000 flaskr:app
```

## Performance Optimizations

- Database connection pooling with pre-ping
- Paginated results to reduce payload size
- Indexed database columns for faster queries
- Rate limiting to prevent server overload
- Efficient SQLAlchemy queries

## Troubleshooting

### Common Issues

**Database connection errors:**
- Verify PostgreSQL is running
- Check credentials in `.env` file
- Ensure databases exist

**Import errors:**
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

**Rate limit exceeded:**
- Wait for rate limit window to reset
- Configure higher limits in production

**CORS errors:**
- Verify frontend URL in CORS configuration
- Check browser console for specific errors

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is part of the Udacity Full Stack Web Developer Nanodegree program.

## Acknowledgments

- Udacity for the project template and requirements
- Flask and React communities for excellent documentation
- Contributors and reviewers

## Support

For issues, questions, or contributions, please open an issue in the repository.

---

**Built with ❤️ as part of Udacity's Full Stack Web Developer Nanodegree**
