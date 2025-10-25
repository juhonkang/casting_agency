import os
import logging
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random

from models import setup_db, Question, Category
from auth import AuthError, requires_auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, data):
    page = request.args.get('page', 1, type=int)
    start = (page -1 ) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    data = [item.format() for item in data]
    return data[start:end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        # database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=test_config)

    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    @limiter.limit("100 per hour")
    @requires_auth('get:categories')
    def get_categories(payload):
        try:
            logger.info("Fetching all categories")
            allCategories = Category.query.all()
            if len(allCategories) == 0:
                logger.warning("No categories found in database")
                abort(404)

            logger.info(f"Successfully retrieved {len(allCategories)} categories")
            return jsonify({
                'success': True,
                'categories': {category.id: category.type for category in allCategories}
            })
        except Exception as e:
            logger.error(f"Error fetching categories: {str(e)}")
            abort(500)


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    @limiter.limit("100 per hour")
    @requires_auth('get:questions')
    def get_questions(payload):
        page = request.args.get('page', 1, type=int)
        try:
            logger.info(f"Fetching questions for page {page}")

            # Validate page number
            if page < 1:
                logger.warning(f"Invalid page number: {page}")
                abort(400)

            questions = Question.query.all()
            allCategories = Category.query.all()

            if len(questions) == 0:
                logger.warning("No questions found in database")
                abort(404)
            if len(allCategories) == 0:
                logger.warning("No categories found in database")
                abort(404)

            paginated_questions = paginate_questions(request, questions)
            logger.info(f"Successfully retrieved {len(paginated_questions)} questions for page {page}")

            return jsonify({
                'questions': paginated_questions,
                'total_questions': len(questions),
                'categories': {category.id: category.type for category in allCategories},
                'current_category': None,
                'success': True,
            })

        except Exception as e:
            logger.error(f"Error fetching questions: {str(e)}")
            abort(500)
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<question_id>", methods=['DELETE'])
    @limiter.limit("50 per hour")
    @requires_auth('delete:questions')
    def delete_question(payload, question_id):
        try:
            logger.info(f"Attempting to delete question with ID: {question_id}")

            # Validate question_id is numeric
            try:
                question_id_int = int(question_id)
            except ValueError:
                logger.warning(f"Invalid question ID format: {question_id}")
                abort(400)

            question = Question.query.get(question_id_int)
            if question:
                question.delete()
                logger.info(f"Successfully deleted question with ID: {question_id}")

                # Get remaining questions for response
                questions = Question.query.all()
                return jsonify({
                    'success': True,
                    'deleted': question_id,
                    'questions': paginate_questions(request, questions),
                    'total_questions': len(questions)
                })
            else:
                logger.warning(f"Question with ID {question_id} not found")
                return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "Resource Not Found"
                }), 404

        except Exception as e:
            logger.error(f"Error deleting question: {str(e)}")
            abort(500)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    @limiter.limit("100 per hour")
    def search_questions():
        try:
            body = request.get_json()

            # Validate request body
            if not body:
                logger.warning("Empty request body for search")
                abort(400)

            search_term = body.get('searchTerm', None)

            if search_term:
                # Sanitize search term
                search_term = search_term.strip()
                logger.info(f"Searching questions with term: {search_term}")

                search_results = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')).all()

                if len(search_results) == 0:
                    logger.info(f"No results found for search term: {search_term}")
                    return jsonify({
                        "success": False,
                        "error": 404,
                        "message": "Resource Not Found"
                    }), 404

                logger.info(f"Found {len(search_results)} results for search term: {search_term}")
                return jsonify({
                    'success': True,
                    'questions': [question.format() for question in search_results],
                    'total_questions': len(search_results),
                    'current_category': None
                })

            logger.warning("Search term not provided")
            abort(400)

        except Exception as e:
            logger.error(f"Error searching questions: {str(e)}")
            abort(500)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=['POST'])
    @limiter.limit("50 per hour")
    @requires_auth('post:questions')
    def post_question(payload):
        try:
            body = request.get_json()

            # Validate request body
            if not body:
                logger.warning("Empty request body for creating question")
                abort(400)

            question_text = body.get('question')
            answer = body.get('answer')
            difficulty = body.get('difficulty')
            category = body.get('category')

            # Validate required fields
            if not all([question_text, answer, difficulty, category]):
                logger.warning("Missing required fields for creating question")
                abort(400)

            # Validate field types and values
            if not isinstance(question_text, str) or not question_text.strip():
                logger.warning("Invalid question text")
                abort(400)

            if not isinstance(answer, str) or not answer.strip():
                logger.warning("Invalid answer text")
                abort(400)

            try:
                difficulty = int(difficulty)
                if difficulty < 1 or difficulty > 5:
                    logger.warning(f"Difficulty out of range: {difficulty}")
                    abort(400)
            except (ValueError, TypeError):
                logger.warning(f"Invalid difficulty value: {difficulty}")
                abort(400)

            try:
                category = int(category)
            except (ValueError, TypeError):
                logger.warning(f"Invalid category value: {category}")
                abort(400)

            # Verify category exists
            category_obj = Category.query.get(category)
            if not category_obj:
                logger.warning(f"Category {category} does not exist")
                abort(400)

            try:
                logger.info("Creating new question")
                new_question = Question(
                    question=question_text.strip(),
                    answer=answer.strip(),
                    difficulty=difficulty,
                    category=category
                )
                new_question.insert()

                logger.info(f"Successfully created question with ID: {new_question.id}")
                return jsonify({
                    'success': True,
                    'created': new_question.id,
                })

            except Exception as e:
                logger.error(f"Database error creating question: {str(e)}")
                abort(422)

        except Exception as e:
            logger.error(f"Error creating question: {str(e)}")
            abort(500)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    @limiter.limit("100 per hour")
    def get_questions_by_category(category_id):
        try:
            logger.info(f"Fetching questions for category ID: {category_id}")

            category = Category.query.get(category_id)
            if category is None:
                logger.warning(f"Category {category_id} not found")
                return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "Resource Not Found"
                }), 404

            questions = Question.query.filter(Question.category == str(category_id)).all()

            logger.info(f"Found {len(questions)} questions for category {category_id}")
            return jsonify({
                'success': True,
                'questions': paginate_questions(request, questions),
                'total_questions': len(questions),
                'current_category': category_id
            })

        except Exception as e:
            logger.error(f"Error fetching questions by category: {str(e)}")
            abort(500)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    @limiter.limit("100 per hour")
    def get_quizzes():
        try:
            body = request.get_json()

            # Validate request body
            if not body:
                logger.warning("Empty request body for quiz")
                abort(400)

            prev_questions = body.get('previous_questions', [])
            quiz_category = body.get('quiz_category', None)

            # Validate quiz_category
            if not quiz_category or 'id' not in quiz_category:
                logger.warning("Invalid quiz category")
                abort(400)

            # Ensure prev_questions is a list
            if not isinstance(prev_questions, list):
                logger.warning("Invalid previous_questions format")
                abort(400)

            logger.info(f"Fetching quiz question for category: {quiz_category}")

            questions = []
            quiz_question = None

            if quiz_category['id'] == 0:
                # All categories
                questions = Question.query.filter(
                    Question.id.notin_(prev_questions)).all()
            else:
                # Specific category
                selected_category = Category.query.filter(
                    Category.type == str(quiz_category['type'])).one_or_none()

                if not selected_category:
                    logger.warning(f"Category not found: {quiz_category['type']}")
                    abort(404)

                category_id = selected_category.id
                questions = Question.query.filter(
                    Question.id.notin_(prev_questions),
                    Question.category == str(category_id)).all()

            if len(questions) > 0:
                question = random.choice(questions)
                quiz_question = question.format()
                logger.info(f"Selected quiz question ID: {question.id}")
            else:
                logger.info("No more questions available for quiz")

            return jsonify({
                'question': quiz_question,
                'success': True
            })

        except Exception as e:
            logger.error(f"Error generating quiz question: {str(e)}")
            abort(500)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        logger.error(f"Bad request error: {error}")
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        logger.error(f"Not found error: {error}")
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        logger.error(f"Method not allowed error: {error}")
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def not_processable(error):
        logger.error(f"Unprocessable entity error: {error}")
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Not Processable"
        }), 422

    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        logger.warning(f"Rate limit exceeded: {error}")
        return jsonify({
            "success": False,
            "error": 429,
            "message": "Rate limit exceeded"
        }), 429

    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Handle authentication errors from Auth0
        """
        logger.error(f"Authentication error: {ex.error}")
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response


    return app

