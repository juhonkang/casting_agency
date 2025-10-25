"""
RBAC (Role-Based Access Control) Test Suite
Tests authentication and authorization for different user roles
"""

import os
import unittest
import json

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv

load_dotenv()

# Load test tokens from environment variables
TRIVIA_USER_TOKEN = os.environ.get('TRIVIA_USER_TOKEN')
TRIVIA_MANAGER_TOKEN = os.environ.get('TRIVIA_MANAGER_TOKEN')

# Database configuration
database_username = os.environ.get("test_database_username")
database_password = os.environ.get("test_database_password")
database_name = os.environ.get("test_database_name")


class TriviaRBACTestCase(unittest.TestCase):
    """Test case for RBAC functionality"""

    def setUp(self):
        """Set up test variables and initialize app"""
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            database_username, database_password, 'localhost:5432', database_name)
        self.app = create_app(self.database_path)
        self.client = self.app.test_client

        # Headers for different roles
        self.trivia_user_headers = {
            'Authorization': f'Bearer {TRIVIA_USER_TOKEN}'
        }
        self.trivia_manager_headers = {
            'Authorization': f'Bearer {TRIVIA_MANAGER_TOKEN}'
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    # -------------------------------------------------------------------------
    # Tests for Public Endpoints (No Authentication Required)
    # -------------------------------------------------------------------------

    def test_no_auth_get_categories_fails(self):
        """Test that GET /categories requires authentication"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertIn('code', data)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_no_auth_get_questions_fails(self):
        """Test that GET /questions requires authentication"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertIn('code', data)
        self.assertEqual(data['code'], 'authorization_header_missing')

    # -------------------------------------------------------------------------
    # Tests for Trivia User Role (get:questions, get:categories)
    # -------------------------------------------------------------------------

    def test_trivia_user_get_categories_success(self):
        """Test Trivia User can GET /categories"""
        res = self.client().get('/categories', headers=self.trivia_user_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_trivia_user_get_questions_success(self):
        """Test Trivia User can GET /questions"""
        res = self.client().get('/questions', headers=self.trivia_user_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_trivia_user_post_question_fails(self):
        """Test Trivia User CANNOT POST /questions (403 Forbidden)"""
        new_question = {
            'question': 'Unauthorized question',
            'answer': 'Should fail',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions',
                                  json=new_question,
                                  headers=self.trivia_user_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertIn('code', data)
        self.assertEqual(data['code'], 'unauthorized')

    def test_trivia_user_delete_question_fails(self):
        """Test Trivia User CANNOT DELETE /questions/<id> (403 Forbidden)"""
        res = self.client().delete('/questions/1',
                                     headers=self.trivia_user_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertIn('code', data)
        self.assertEqual(data['code'], 'unauthorized')

    # -------------------------------------------------------------------------
    # Tests for Trivia Manager Role (All Permissions)
    # -------------------------------------------------------------------------

    def test_trivia_manager_get_categories_success(self):
        """Test Trivia Manager can GET /categories"""
        res = self.client().get('/categories', headers=self.trivia_manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_trivia_manager_get_questions_success(self):
        """Test Trivia Manager can GET /questions"""
        res = self.client().get('/questions', headers=self.trivia_manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_trivia_manager_post_question_success(self):
        """Test Trivia Manager can POST /questions"""
        new_question = {
            'question': 'Manager test question',
            'answer': 'Manager test answer',
            'difficulty': 2,
            'category': 1
        }
        res = self.client().post('/questions',
                                  json=new_question,
                                  headers=self.trivia_manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_trivia_manager_delete_question_success(self):
        """Test Trivia Manager can DELETE /questions/<id>"""
        # First create a question to delete
        new_question = {
            'question': 'Question to delete',
            'answer': 'Will be deleted',
            'difficulty': 1,
            'category': 1
        }
        create_res = self.client().post('/questions',
                                         json=new_question,
                                         headers=self.trivia_manager_headers)
        create_data = json.loads(create_res.data)
        question_id = create_data['created']

        # Now delete it
        res = self.client().delete(f'/questions/{question_id}',
                                     headers=self.trivia_manager_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], str(question_id))

    # -------------------------------------------------------------------------
    # Tests for Invalid Tokens
    # -------------------------------------------------------------------------

    def test_invalid_token_fails(self):
        """Test that invalid token returns 401"""
        invalid_headers = {
            'Authorization': 'Bearer invalid.token.here'
        }
        res = self.client().get('/categories', headers=invalid_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertIn('code', data)

    def test_malformed_auth_header_fails(self):
        """Test that malformed Authorization header fails"""
        malformed_headers = {
            'Authorization': 'InvalidFormat'
        }
        res = self.client().get('/categories', headers=malformed_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertIn('code', data)
        self.assertEqual(data['code'], 'invalid_header')

    # -------------------------------------------------------------------------
    # Tests for Search and Quiz Endpoints (No Auth Required for backward compatibility)
    # -------------------------------------------------------------------------

    # Note: If you want to add auth to search and quizzes, uncomment below
    # and add the corresponding decorators to the endpoints

    # def test_trivia_user_search_questions_success(self):
    #     """Test Trivia User can search questions"""
    #     search_data = {'searchTerm': 'a'}
    #     res = self.client().post('/questions/search',
    #                               json=search_data,
    #                               headers=self.trivia_user_headers)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
