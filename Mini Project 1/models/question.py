from db import db

class QuestionModel(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), unique=False, nullable=False)
    question_type = db.Column(db.String(80), unique=False, nullable=False)