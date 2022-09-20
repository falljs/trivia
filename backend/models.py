import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
#import json
import json as json
from flask_migrate import Migrate
from flask import Flask

database_name = 'trivia'
database_path = 'postgresql://postgres:070017@localhost:5432/'+database_name
db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

"""
Question
"""
class Question(db.Model):
    __tablename__ = 'questions'
    id = Column(db.Integer, primary_key=True)
    question = Column(db.String(100))
    answer = Column(db.String(100))
    difficulty = Column(db.Integer)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    def __init__(self, question, answer, difficulty, category):
        self.question = question
        self.answer = answer
        self.difficulty = difficulty
        self.category = category

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'difficulty': self.difficulty,
            'category': self.category
            }

"""
Category
"""
class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(db.Integer, primary_key=True)
    type = Column(db.String(100))
    questions = db.relationship('Question', backref='category', lazy=True)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }