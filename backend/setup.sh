#!/bin/bash

# Auth0 Configuration
# Replace these values with your Auth0 tenant information
export AUTH0_DOMAIN='your-tenant.us.auth0.com'
export ALGORITHMS='["RS256"]'
export API_AUDIENCE='trivia-api'

# JWT Tokens for Testing
# Replace these with actual tokens from Auth0
# To generate tokens:
# 1. Go to Auth0 Dashboard > Applications > APIs > Trivia API > Test
# 2. Or use the provided test users to login and get tokens

# Trivia User Token (Permissions: get:questions, get:categories)
export TRIVIA_USER_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjEyMzQ1Njc4OTAifQ.eyJpc3MiOiJodHRwczovL3lvdXItdGVuYW50LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTIzNDU2Nzg5IiwiYXVkIjoidHJpdmlhLWFwaSIsImlhdCI6MTYzMDAwMDAwMCwiZXhwIjoxNjMwMDg2NDAwLCJhenAiOiJ5b3VyLWNsaWVudC1pZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OnF1ZXN0aW9ucyIsImdldDpjYXRlZ29yaWVzIl19.REPLACE_WITH_ACTUAL_TOKEN'

# Trivia Manager Token (Permissions: get:questions, get:categories, post:questions, delete:questions)
export TRIVIA_MANAGER_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjEyMzQ1Njc4OTAifQ.eyJpc3MiOiJodHRwczovL3lvdXItdGVuYW50LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw5ODc2NTQzMjEwIiwiYXVkIjoidHJpdmlhLWFwaSIsImlhdCI6MTYzMDAwMDAwMCwiZXhwIjoxNjMwMDg2NDAwLCJhenAiOiJ5b3VyLWNsaWVudC1pZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OnF1ZXN0aW9ucyIsImdldDpjYXRlZ29yaWVzIiwicG9zdDpxdWVzdGlvbnMiLCJkZWxldGU6cXVlc3Rpb25zIl19.REPLACE_WITH_ACTUAL_TOKEN'

# Database Configuration (if not already in .env)
export database_username='your_username'
export database_password='your_password'
export database_name='trivia'

# Test Database
export test_database_username='your_username'
export test_database_password='your_password'
export test_database_name='trivia_test'

# Flask Configuration
export FLASK_APP=flaskr
export FLASK_ENV=development

echo "Environment variables set successfully!"
echo "Auth0 Domain: $AUTH0_DOMAIN"
echo "API Audience: $API_AUDIENCE"
echo ""
echo "To use these variables, run: source setup.sh"
echo ""
echo "IMPORTANT: Replace the placeholder tokens with actual JWT tokens from Auth0"
