import os
from sqlalchemy import Column, String, Integer, create_engine, CheckConstraint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from dotenv import load_dotenv
from datetime import datetime

# Check for Render's DATABASE_URL first (from environment variables)
# This takes priority over .env file
database_path = os.environ.get('DATABASE_URL')

# If not set, load from .env file for local development
if not database_path:
    load_dotenv()
    database_path = os.getenv('DATABASE_URL')

    # If still not set, try individual database credentials
    if not database_path:
        database_username = os.getenv("database_username")
        database_password = os.getenv("database_password")
        database_name = os.getenv("database_name")

        if database_username and database_password and database_name:
            database_path = 'postgresql://{}:{}@{}/{}'.format(
                database_username, database_password, 'localhost:5432', database_name
            )
        else:
            # Use SQLite as fallback for testing
            database_path = 'sqlite:///trivia.db'

db = SQLAlchemy()
migrate = Migrate()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()

"""
Question
Represents a trivia question with associated answer, category, and difficulty level
"""
class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String(500), nullable=False)
    answer = Column(String(500), nullable=False)
    category = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)

    # Add constraint to ensure difficulty is between 1 and 5
    __table_args__ = (
        CheckConstraint('difficulty >= 1 AND difficulty <= 5', name='check_difficulty_range'),
    )

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        """Insert a new question into the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update an existing question in the database"""
        db.session.commit()

    def delete(self):
        """Delete a question from the database"""
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """Format question data for JSON response"""
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }

    def __repr__(self):
        return f'<Question {self.id}: {self.question[:50]}>'

"""
Category
Represents a question category
"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String(100), unique=True, nullable=False)

    def __init__(self, type):
        self.type = type

    def insert(self):
        """Insert a new category into the database"""
        db.session.add(self)
        db.session.commit()

    def format(self):
        """Format category data for JSON response"""
        return {
            'id': self.id,
            'type': self.type
        }

    def __repr__(self):
        return f'<Category {self.id}: {self.type}>'
