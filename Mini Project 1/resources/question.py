from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import QuestionModel
from schemas import QuestionSchema, QuestionUpdateSchema

blp = Blueprint("Questions", "questions", description="Operation on stores")

@blp.route("/question/<int:question_id>")
class Question(MethodView):
    @blp.response(200, QuestionSchema)
    def get(self, question_id):
        question = QuestionModel.query.get_or_404(question_id)
        return question
    
    def delete(self, question_id):
        question = QuestionModel.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return {"message":"Question Was Deleate"}
    
    @blp.arguments(QuestionUpdateSchema)
    @blp.response(200, QuestionSchema)
    def put(self, question_data, question_id):
        question_ans = QuestionModel.query.get(question_id)
        if question_ans:
            question_ans.question = question_data["question"]
            question_ans.question_type = question_data["question_type"]
        else:
            question_ans = QuestionModel(id=question_ans, **question_data)

        db.session.add(question_ans)
        db.session.commit()

        return question_ans


@blp.route("/question")
class QuestionList(MethodView):
    @blp.response(200, QuestionSchema(many=True))
    def get(self):
        return QuestionModel.query.all()

    @blp.arguments(QuestionSchema)
    @blp.response(201, QuestionSchema)
    def post(self, question_data):
        question = QuestionModel(**question_data)
        try:
            db.session.add(question)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A question with that name alredy exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occured creating the question.")

        return question